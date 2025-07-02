# RAG Demo - Local Setup with Supabase + pgvector

This is a demo of a RAG (Retrieval-Augmented Generation) application using Next.js, FastAPI, Supabase + pgvector, and Ollama.

## Prerequisites

- Docker and Docker Compose
- Git
- Supabase account (for vector database)

## Setup Instructions

### 1. Supabase Setup

First, create a new Supabase project:

1. Go to [Supabase](https://supabase.com) and create a new project
2. Wait for your project to be ready
3. Go to the SQL Editor in your Supabase dashboard
4. Run the SQL script from `supabase_setup.sql` to set up the database schema and pgvector extension

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your Supabase credentials
```

Update the `.env` file with your Supabase project details:
- `SUPABASE_URL`: Found in Project Settings > API
- `SUPABASE_ANON_KEY`: Found in Project Settings > API

### 3. Clone and Start Services

```bash
# Clone the repository
git clone <your-repo-url>
cd rag-demo

# Build the images (required for first time and after dependency changes)
docker-compose build

# Start all services
docker-compose up -d
```

### 4. Setup Ollama with llama3.2:1b Model

After the containers are running, you need to pull the llama3.2:1b model:

**On Windows:**
```cmd
setup-ollama.bat
```

**On Linux/Mac:**
```bash
chmod +x setup-ollama.sh
./setup-ollama.sh
```

**Or manually:**
```bash
# Wait for Ollama to start (about 10 seconds)
docker exec rag-demo-ollama-1 ollama pull llama3.2:1b
```

### 5. Ingest Sample Data (Optional)

You can ingest the sample document via API or use the web interface:

**Option A: Via Web Interface (Recommended)**
1. Open http://localhost:3000
2. Use the "Upload Document" section to upload any text file
3. The file will be automatically processed and ready for questions

**Option B: Via API**
```bash
curl -X POST -F 'file=@backend/example.txt' http://localhost:8000/api/ingest
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Supabase Dashboard**: Your Supabase project URL

## Usage

1. Open http://localhost:3000 in your browser
2. **Upload Documents**: Use the left panel to upload text files (.txt, .md, .doc, .docx)
3. **Ask Questions**: Use the right panel to ask questions about uploaded content
3. Get AI-powered responses based on the document context stored in Supabase

### Web Interface Features
- **File Upload**: Drag and drop or select files to upload
- **Real-time Processing**: See upload progress and status
- **Question Interface**: Clean textarea for multi-line questions
- **Response Display**: Formatted AI responses with context

### 🎯 Enterprise Evaluation System
For technical stakeholders and portfolio reviewers, this project includes a comprehensive **RAG Pipeline Evaluation Framework**:

- **📊 Interactive Dashboard**: Professional evaluation metrics visualization
- **🔍 Quality Metrics**: ROUGE scores, faithfulness, answer relevance testing
- **⚡ Performance Testing**: Response time, throughput, and reliability analysis
- **🎯 Business KPIs**: Accuracy, user satisfaction, and system effectiveness

**Quick Demo**: Run `demo_evaluation_for_review.bat` or view `evaluation_dashboard.html`

**Full Documentation**: See `EVALUATION_FRAMEWORK.md` for complete details

## API Endpoints

- `POST /api/ingest` - Upload and ingest text files
- `POST /api/prompt` - Ask questions about ingested content
- `GET /` - Health check

## Architecture

- **Frontend**: Next.js with Tailwind CSS
- **Backend**: FastAPI with LangChain
- **Vector Database**: Supabase with pgvector extension for storing embeddings
- **LLM**: Ollama running llama3.2:1b locally
- **Embeddings**: FastEmbed for document vectorization
- **Observability**: LangSmith for LLM monitoring and tracing

### 🔍 LLM Observability & Monitoring

This project includes **enterprise-grade observability** with industry-standard monitoring platforms:

- **🔗 LangSmith Integration**: Automatic request tracing and debugging
- **📊 LangSmith Analytics**: Performance metrics and cost tracking
- **📝 Structured Logging**: JSON logs for monitoring and alerting
- **⚡ Real-time Metrics**: Response time, token usage, quality scores
- **🎯 Production Monitoring**: Error tracking and system health

**Setup Observability**:
1. Copy the contents from `.env.observability.example` to `.env`
2. Add your LangSmith API key
3. Restart the system to enable monitoring

**Documentation**: See `OBSERVABILITY_FRAMEWORK.md` for complete setup and features

## Troubleshooting

### Ollama Model Issues
If you get Ollama connection errors:
```bash
# Check if llama3.2:1b model is available
docker exec rag-demo-ollama-1 ollama list

# If not listed, pull it again
docker exec rag-demo-ollama-1 ollama pull llama3.2:1b
```

### Container Issues
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs [service-name]

# Rebuild specific service after code/dependency changes
docker-compose build backend
docker-compose build frontend

# Restart services
docker-compose restart

# Full rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

### Data Persistence
- Document data is persisted in your Supabase database
- Ollama models are persisted in `ollama_data` volume

### Supabase Issues
If you encounter database connection issues:
```bash
# Check your environment variables
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY

# Verify your Supabase project is active
# Check the database schema in Supabase dashboard
```

### File Upload Issues
If you get "❌ Error uploading file" messages:

**1. Vector Dimension Mismatch Error**
If you see `'expected 768 dimensions, not 384'` in the logs:
```sql
-- This is the most common issue after migration
-- Run this SQL in your Supabase dashboard to fix the table:
-- Copy and paste the content from supabase_fix_dimensions.sql
```

**2. Other Troubleshooting Steps**
```bash
# Check if Supabase credentials are properly set
docker-compose exec backend env | grep SUPABASE

# Verify the backend container logs for detailed errors
docker-compose logs backend

# Test the backend API directly
curl -X GET http://localhost:8000/

# Check if the documents table exists in Supabase
# Go to your Supabase dashboard > Table Editor
# Verify the 'documents' table is created with vector(384) schema

# Test Supabase connection manually
docker-compose exec backend python -c "
from supabase import create_client
import os
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_ANON_KEY')
print(f'URL: {url}')
print(f'Key: {key[:10]}...' if key else 'Key: None')
try:
    client = create_client(url, key)
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
"
```

**Common causes:**
- ❌ **Vector dimension mismatch** (768 vs 384) - Use `supabase_fix_dimensions.sql`
- ❌ **File encoding issues** (UnicodeDecodeError) - Backend now supports multiple encodings
- Missing or incorrect Supabase credentials in `.env` file
- Database schema not properly set up (run `supabase_setup.sql`)
- Network connectivity issues to Supabase
- Missing dependencies in the backend container

**File format support:**
- ✅ Plain text files (.txt, .md)
- ✅ Multiple encodings (UTF-8, UTF-16, Latin-1, etc.)
- ✅ Large documents (intelligent chunking with 1000 char limit)
- ✅ Documents with metadata (filename tracking)
- ✅ Smart text splitting (respects paragraphs, sentences, words)
- ❌ Binary files (images, PDFs) - use text extraction tools first

### Performance Issues
If you experience slow response times (>30 seconds):

**1. Check Chunk Sizes**
```bash
# Monitor backend logs for oversized chunks
docker-compose logs backend --tail=20

# Look for warnings like "Created a chunk of size X, which is longer than 1000"
```

**2. Ollama Performance**
```bash
# Check Ollama response times
docker-compose logs ollama --tail=10

# Should see generation times under 10 seconds for simple queries
# If consistently over 20 seconds, consider:
# - Using a smaller model context (already optimized to 2048)
# - Reducing num_predict parameter (already set to 256)
```

**3. Optimize for Your Hardware**
- **Low RAM (< 8GB)**: Current settings are optimized for this
- **High RAM (> 16GB)**: You can increase chunk_size to 1500 and num_ctx to 4096 in main.py
- **CPU-only**: Response times of 10-20 seconds are normal for llama3.2:1b

**4. Quick Performance Test**
```bash
# Test backend directly (should respond in <1 second)
curl -X GET http://localhost:8000/

# Test simple prompt (should complete in 5-15 seconds)
curl -X POST http://localhost:8000/api/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

## Development

To run in development mode with hot reload:

```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development  
cd frontend
npm install
npm run dev
```
