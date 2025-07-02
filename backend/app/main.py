from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from supabase import create_client, Client
import os
import time
import json
import uuid
from typing import Dict, Any, Optional
import structlog

# LLM Observability imports
try:
    from langsmith import Client as LangSmithClient
    from langsmith.wrappers import wrap_openai
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

# Import Document and PromptTemplate with fallbacks for compatibility
try:
    from langchain_core.documents import Document
    from langchain_core.prompts import PromptTemplate
except ImportError:
    from langchain.schema import Document
    from langchain.prompts import PromptTemplate

# Setup structured logging
logger = structlog.get_logger()

# Initialize observability clients
observability_clients = {}

def initialize_observability():
    """Initialize LLM observability frameworks"""
    global observability_clients
    
    # LangSmith setup
    if LANGSMITH_AVAILABLE and os.environ.get("LANGCHAIN_API_KEY"):
        try:
            observability_clients["langsmith"] = LangSmithClient(
                api_url=os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"),
                api_key=os.environ.get("LANGCHAIN_API_KEY")
            )
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT", "rag-demo")
            logger.info("LangSmith observability initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize LangSmith: {e}")

def create_trace_context(query: str, trace_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a trace context for observability"""
    trace_id = trace_id or str(uuid.uuid4())
    return {
        "trace_id": trace_id,
        "query": query,
        "timestamp": time.time(),
        "session_id": str(uuid.uuid4())[:8]
    }

def log_rag_metrics(trace_context: Dict[str, Any], retrieval_docs: list, response: str, 
                   response_time: float, token_count: Optional[int] = None):
    """Log comprehensive RAG metrics to observability platforms"""
    
    metrics = {
        "trace_id": trace_context["trace_id"],
        "query": trace_context["query"],
        "response_time_ms": response_time * 1000,
        "retrieved_docs_count": len(retrieval_docs),
        "response_length": len(response),
        "token_count": token_count or estimate_tokens(response),
        "timestamp": trace_context["timestamp"]
    }
    
    # Log to LangSmith
    if "langsmith" in observability_clients:
        try:
            client = observability_clients["langsmith"]
            # LangSmith tracing is handled automatically via environment variables
            logger.info("Metrics logged to LangSmith", **metrics)
        except Exception as e:
            logger.error(f"Failed to log to LangSmith: {e}")
    
    # Structure log for local monitoring
    logger.info("RAG query completed", **metrics)

def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token for English)"""
    return len(text) // 4

# Initialize observability on startup
initialize_observability()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Query(BaseModel):
    prompt: str

@app.post("/api/prompt")
def prompt(query: Query):
    # Create trace context for observability
    trace_context = create_trace_context(query.prompt)
    start_time = time.time()
    
    try:
        # Initialize Supabase client
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            return {"error": "Supabase credentials not configured. Please check your .env file."}
        
        supabase: Client = create_client(supabase_url, supabase_key)
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")  # Faster, smaller model

        # Initialize Supabase vector store
        doc_store = SupabaseVectorStore(
            client=supabase,
            embedding=embeddings,
            table_name="documents",
            query_name="match_documents"
        )

        # Setup LLM with observability callbacks
        llm = Ollama(
            base_url=os.environ.get("OLLAMA_URL", "http://ollama:11434"), 
            model="llama3.2:1b",
            temperature=0.7,
            num_predict=256,  # Limit response length for faster generation
            num_ctx=2048,     # Reduced context size for speed
        )

        template = """
        You are a helpful AI assistant. You will answer the question based on the context provided.

        {context}

        Question: {question}
        """

        prompt_template = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=doc_store.as_retriever(search_kwargs={"k": 3}),  # Limit to 3 most relevant chunks
            chain_type_kwargs={"prompt": prompt_template}
        )
        
        # Get retrieval docs for logging
        retriever = doc_store.as_retriever(search_kwargs={"k": 3})
        retrieved_docs = retriever.get_relevant_documents(query.prompt)
        
        response = qa.run(query.prompt)
        response_time = time.time() - start_time
        
        # Log comprehensive metrics to observability platforms
        log_rag_metrics(trace_context, retrieved_docs, response, response_time)
        
        return {
            "response": response,
            "trace_id": trace_context["trace_id"],
            "response_time_ms": response_time * 1000,
            "retrieved_docs_count": len(retrieved_docs)
        }
        
    except Exception as e:
        error_time = time.time() - start_time
        logger.error("RAG query failed", 
                    trace_id=trace_context["trace_id"], 
                    error=str(e), 
                    response_time_ms=error_time * 1000)
        return {"error": f"Failed to process query: {str(e)}"}

@app.post("/api/ingest")
async def ingest_file(file: UploadFile = File(...)):
    """Ingest a file with observability tracking"""
    trace_context = create_trace_context(f"ingest_file_{file.filename}")
    start_time = time.time()
    
    try:
        # Initialize Supabase client
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            return {"error": "Supabase credentials not configured"}

        supabase: Client = create_client(supabase_url, supabase_key)
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        # Smart chunking
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        texts = text_splitter.split_text(text)
        docs = [Document(page_content=t, metadata={"source": file.filename}) for t in texts]
        
        # Initialize vector store and add documents
        doc_store = SupabaseVectorStore(
            client=supabase,
            embedding=embeddings,
            table_name="documents",
            query_name="match_documents"
        )
        
        doc_store.add_documents(docs)
        
        processing_time = time.time() - start_time
        
        # Log ingestion metrics
        logger.info("File ingestion completed",
                   trace_id=trace_context["trace_id"],
                   filename=file.filename,
                   chunks_created=len(docs),
                   processing_time_ms=processing_time * 1000)
        
        return {
            "message": f"Successfully ingested {file.filename}",
            "chunks_created": len(docs),
            "processing_time_ms": processing_time * 1000,
            "trace_id": trace_context["trace_id"]
        }
        
    except Exception as e:
        error_time = time.time() - start_time
        logger.error("File ingestion failed",
                    trace_id=trace_context["trace_id"],
                    filename=file.filename,
                    error=str(e),
                    processing_time_ms=error_time * 1000)
        return {"error": f"Failed to ingest file: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "RAG Backend Running", "observability": {
        "langsmith": "langsmith" in observability_clients
    }}

@app.get("/status")
def detailed_status():
    """Detailed status endpoint for debugging"""
    return {
        "backend": "running",
        "observability": {
            "langsmith": "langsmith" in observability_clients,
            "langsmith_available": LANGSMITH_AVAILABLE,
            "env_vars": {
                "langchain_api_key": bool(os.environ.get("LANGCHAIN_API_KEY"))
            }
        }
    }
