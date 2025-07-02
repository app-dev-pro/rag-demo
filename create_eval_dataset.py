#!/usr/bin/env python3
"""
RAG Evaluation Dataset Creator

This script creates a comprehensive evaluation dataset for the RAG system,
including questions, reference answers, and ground truth data for measuring
retrieval quality, generation quality, and end-to-end performance.

"""

import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class EvaluationDatasetCreator:
    """Creates evaluation datasets for RAG system testing"""
    
    def __init__(self, output_dir: str = "evaluation_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Sample documents that might be in the RAG system
        self.sample_documents = [
            {
                "id": "doc_001",
                "title": "Introduction to Large Language Models",
                "content": "Large Language Models (LLMs) are neural networks trained on vast amounts of text data. They can understand and generate human-like text across various domains. Modern LLMs like GPT, BERT, and T5 have revolutionized natural language processing.",
                "metadata": {"category": "AI/ML", "difficulty": "beginner"}
            },
            {
                "id": "doc_002", 
                "title": "RAG System Architecture",
                "content": "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. The system first retrieves relevant documents from a knowledge base, then uses this context to generate accurate, grounded responses. Key components include document embedding, vector storage, and LLM integration.",
                "metadata": {"category": "AI/ML", "difficulty": "intermediate"}
            },
            {
                "id": "doc_003",
                "title": "Vector Databases and Embeddings",
                "content": "Vector databases store high-dimensional embeddings that represent semantic meaning of text. Popular options include Pinecone, Weaviate, and pgvector. Embeddings are created using models like OpenAI's text-embedding-ada-002 or open-source alternatives like FastEmbed.",
                "metadata": {"category": "Infrastructure", "difficulty": "intermediate"}
            },
            {
                "id": "doc_004",
                "title": "LLM Fine-tuning Techniques",
                "content": "Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA and QLoRA allow adaptation of large models with minimal computational resources. The Unsloth framework provides 2x faster training and 70% memory reduction. Techniques include DPO and ORPO for preference optimization.",
                "metadata": {"category": "AI/ML", "difficulty": "advanced"}
            },
            {
                "id": "doc_005",
                "title": "Docker and Containerization",
                "content": "Docker containers provide consistent deployment environments across development and production. Docker Compose orchestrates multi-service applications. Best practices include multi-stage builds, image optimization, and proper secret management.",
                "metadata": {"category": "DevOps", "difficulty": "intermediate"}
            },
            {
                "id": "doc_006",
                "title": "LangSmith Observability",
                "content": "LangSmith provides comprehensive observability for LLM applications. Features include request tracing, performance monitoring, debugging workflows, and analytics. Integration with LangChain enables automatic instrumentation and detailed insights into AI system behavior.",
                "metadata": {"category": "Monitoring", "difficulty": "intermediate"}
            },
            {
                "id": "doc_007",
                "title": "Next.js and React Development",
                "content": "Next.js 13+ introduces the App Router with server components, enabling better performance and developer experience. Features include automatic code splitting, image optimization, and built-in CSS support. Tailwind CSS provides utility-first styling for rapid UI development.",
                "metadata": {"category": "Frontend", "difficulty": "intermediate"}
            },
            {
                "id": "doc_008",
                "title": "FastAPI Backend Development",
                "content": "FastAPI is a modern Python web framework for building APIs with automatic documentation. It provides async/await support, type hints validation, and OpenAPI schema generation. Integration with Pydantic ensures data validation and serialization.",
                "metadata": {"category": "Backend", "difficulty": "intermediate"}
            }
        ]
        
    def create_question_answer_pairs(self) -> List[Dict[str, Any]]:
        """Generate question-answer pairs from sample documents"""
        qa_pairs = []
        
        # Generate QA pairs for each document
        for doc in self.sample_documents:
            title = doc["title"]
            doc_id = doc["id"]
            
            # Extract key concepts for question generation
            if "Large Language Models" in title:
                qa_pairs.extend([
                    {
                        "question": "What are Large Language Models?",
                        "reference_answer": "Large Language Models (LLMs) are neural networks trained on vast amounts of text data. They can understand and generate human-like text across various domains.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "beginner",
                        "category": "AI/ML",
                        "evaluation_aspects": ["factual_accuracy", "completeness"]
                    },
                    {
                        "question": "Which models are examples of modern LLMs?",
                        "reference_answer": "Modern LLMs include GPT, BERT, and T5, which have revolutionized natural language processing.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "beginner", 
                        "category": "AI/ML",
                        "evaluation_aspects": ["factual_accuracy", "specific_knowledge"]
                    }
                ])
                
            elif "RAG" in title:
                qa_pairs.extend([
                    {
                        "question": "What is Retrieval-Augmented Generation?",
                        "reference_answer": "Retrieval-Augmented Generation (RAG) combines information retrieval with text generation. The system first retrieves relevant documents from a knowledge base, then uses this context to generate accurate, grounded responses.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "AI/ML",
                        "evaluation_aspects": ["conceptual_understanding", "technical_accuracy"]
                    },
                    {
                        "question": "What are the key components of a RAG system?",
                        "reference_answer": "Key components of a RAG system include document embedding, vector storage, and LLM integration.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "AI/ML",
                        "evaluation_aspects": ["completeness", "technical_detail"]
                    }
                ])
                
            elif "Vector" in title:
                qa_pairs.extend([
                    {
                        "question": "What are vector databases used for?",
                        "reference_answer": "Vector databases store high-dimensional embeddings that represent semantic meaning of text.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "Infrastructure",
                        "evaluation_aspects": ["technical_accuracy", "clarity"]
                    },
                    {
                        "question": "What are some popular vector database options?",
                        "reference_answer": "Popular vector database options include Pinecone, Weaviate, and pgvector.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "Infrastructure",
                        "evaluation_aspects": ["factual_accuracy", "specific_knowledge"]
                    }
                ])
                
            elif "Fine-tuning" in title:
                qa_pairs.extend([
                    {
                        "question": "What is Parameter-Efficient Fine-Tuning?",
                        "reference_answer": "Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA and QLoRA allow adaptation of large models with minimal computational resources.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "advanced",
                        "category": "AI/ML",
                        "evaluation_aspects": ["technical_accuracy", "conceptual_understanding"]
                    },
                    {
                        "question": "What benefits does the Unsloth framework provide?",
                        "reference_answer": "The Unsloth framework provides 2x faster training and 70% memory reduction for LLM fine-tuning.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "advanced",
                        "category": "AI/ML",
                        "evaluation_aspects": ["specific_knowledge", "quantitative_accuracy"]
                    }
                ])
                
            elif "Docker" in title:
                qa_pairs.extend([
                    {
                        "question": "What are the benefits of using Docker containers?",
                        "reference_answer": "Docker containers provide consistent deployment environments across development and production.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "DevOps",
                        "evaluation_aspects": ["practical_understanding", "clarity"]
                    },
                    {
                        "question": "What is Docker Compose used for?",
                        "reference_answer": "Docker Compose orchestrates multi-service applications.",
                        "relevant_doc_ids": [doc_id],
                        "difficulty": "intermediate",
                        "category": "DevOps",
                        "evaluation_aspects": ["technical_accuracy", "conciseness"]
                    }
                ])
        
        # Add multi-document questions that require synthesizing information
        multi_doc_questions = [
            {
                "question": "How do vector databases and embeddings work together in RAG systems?",
                "reference_answer": "Vector databases store high-dimensional embeddings that represent semantic meaning of text. In RAG systems, these embeddings enable efficient retrieval of relevant documents from the knowledge base, which are then used as context for text generation.",
                "relevant_doc_ids": ["doc_002", "doc_003"],
                "difficulty": "advanced",
                "category": "AI/ML",
                "evaluation_aspects": ["synthesis", "cross_document_reasoning", "technical_accuracy"]
            },
            {
                "question": "What technologies are needed for a complete RAG implementation?",
                "reference_answer": "A complete RAG implementation requires vector databases for storing embeddings, LLM frameworks for generation, containerization with Docker for deployment, and observability tools like LangSmith for monitoring. Frontend frameworks like Next.js and backend APIs with FastAPI complete the full-stack solution.",
                "relevant_doc_ids": ["doc_002", "doc_003", "doc_005", "doc_006", "doc_007", "doc_008"],
                "difficulty": "advanced",
                "category": "AI/ML",
                "evaluation_aspects": ["comprehensive_understanding", "integration_knowledge", "system_thinking"]
            }
        ]
        
        qa_pairs.extend(multi_doc_questions)
        
        # Add unique IDs and timestamps
        for i, qa in enumerate(qa_pairs):
            qa["id"] = f"qa_{i+1:03d}"
            qa["created_at"] = datetime.now().isoformat()
            
        return qa_pairs
    
    def create_retrieval_test_cases(self) -> List[Dict[str, Any]]:
        """Create test cases specifically for retrieval evaluation"""
        test_cases = []
        
        # Positive test cases - queries that should retrieve specific documents
        positive_cases = [
            {
                "query": "large language models neural networks",
                "expected_doc_ids": ["doc_001"],
                "test_type": "exact_match",
                "description": "Direct keyword match should retrieve LLM document"
            },
            {
                "query": "RAG retrieval augmented generation",
                "expected_doc_ids": ["doc_002"],
                "test_type": "exact_match", 
                "description": "RAG terminology should retrieve RAG architecture document"
            },
            {
                "query": "LoRA QLoRA fine-tuning",
                "expected_doc_ids": ["doc_004"],
                "test_type": "exact_match",
                "description": "Fine-tuning terms should retrieve fine-tuning document"
            },
            {
                "query": "semantic meaning embeddings",
                "expected_doc_ids": ["doc_003"],
                "test_type": "semantic_match",
                "description": "Semantic concepts should retrieve vector database document"
            }
        ]
        
        # Negative test cases - queries that should not retrieve certain documents
        negative_cases = [
            {
                "query": "machine learning algorithms",
                "unexpected_doc_ids": ["doc_005", "doc_007", "doc_008"],
                "test_type": "negative_match",
                "description": "General ML query should not retrieve DevOps/Frontend docs"
            },
            {
                "query": "web development frameworks",
                "unexpected_doc_ids": ["doc_001", "doc_004"],
                "test_type": "negative_match",
                "description": "Web dev query should not retrieve AI/ML specific docs"
            }
        ]
        
        # Multi-document retrieval cases
        multi_doc_cases = [
            {
                "query": "AI system deployment and monitoring",
                "expected_doc_ids": ["doc_005", "doc_006"],
                "min_retrieved": 2,
                "test_type": "multi_document",
                "description": "Should retrieve both Docker and LangSmith documents"
            },
            {
                "query": "full-stack AI application development",
                "expected_doc_ids": ["doc_002", "doc_007", "doc_008"],
                "min_retrieved": 2,
                "test_type": "multi_document",
                "description": "Should retrieve documents about RAG, frontend, and backend"
            }
        ]
        
        test_cases.extend(positive_cases)
        test_cases.extend(negative_cases)
        test_cases.extend(multi_doc_cases)
        
        # Add metadata
        for i, case in enumerate(test_cases):
            case["test_id"] = f"retrieval_test_{i+1:03d}"
            case["created_at"] = datetime.now().isoformat()
            
        return test_cases
    
    def create_generation_test_cases(self) -> List[Dict[str, Any]]:
        """Create test cases for generation quality evaluation"""
        test_cases = []
        
        # Faithfulness tests - answers should be grounded in context
        faithfulness_tests = [
            {
                "question": "What performance improvements does Unsloth provide?",
                "context": "The Unsloth framework provides 2x faster training and 70% memory reduction. Techniques include DPO and ORPO for preference optimization.",
                "expected_elements": ["2x faster", "70% memory reduction"],
                "test_type": "faithfulness",
                "description": "Answer should include specific quantitative claims from context"
            },
            {
                "question": "What are examples of modern LLMs?",
                "context": "Modern LLMs like GPT, BERT, and T5 have revolutionized natural language processing.",
                "expected_elements": ["GPT", "BERT", "T5"],
                "test_type": "faithfulness", 
                "description": "Answer should mention specific models from context"
            }
        ]
        
        # Relevance tests - answers should address the question
        relevance_tests = [
            {
                "question": "How does RAG work?",
                "irrelevant_elements": ["Docker", "Next.js", "FastAPI"],
                "test_type": "relevance",
                "description": "RAG explanation should not include unrelated technologies"
            },
            {
                "question": "What is Docker used for?",
                "relevant_elements": ["containers", "deployment", "environments"],
                "test_type": "relevance",
                "description": "Docker answer should focus on containerization concepts"
            }
        ]
        
        # Completeness tests - answers should be comprehensive
        completeness_tests = [
            {
                "question": "What are the key components of a RAG system?",
                "required_elements": ["retrieval", "generation", "embeddings", "vector storage"],
                "test_type": "completeness",
                "description": "Should cover main RAG components"
            },
            {
                "question": "What are vector databases used for?",
                "required_elements": ["embeddings", "semantic meaning", "high-dimensional"],
                "test_type": "completeness",
                "description": "Should explain vector database purpose and characteristics"
            }
        ]
        
        test_cases.extend(faithfulness_tests)
        test_cases.extend(relevance_tests)
        test_cases.extend(completeness_tests)
        
        # Add metadata
        for i, case in enumerate(test_cases):
            case["test_id"] = f"generation_test_{i+1:03d}"
            case["created_at"] = datetime.now().isoformat()
            
        return test_cases
    
    def create_performance_test_cases(self) -> List[Dict[str, Any]]:
        """Create test cases for performance evaluation"""
        test_cases = [
            {
                "test_id": "perf_001",
                "test_type": "latency",
                "description": "Single query response time",
                "query": "What is a large language model?",
                "max_response_time_ms": 5000,
                "target_response_time_ms": 2000
            },
            {
                "test_id": "perf_002", 
                "test_type": "throughput",
                "description": "Concurrent query handling",
                "concurrent_queries": 10,
                "queries": ["What is RAG?"] * 10,
                "max_total_time_ms": 15000
            },
            {
                "test_id": "perf_003",
                "test_type": "memory_usage",
                "description": "Memory consumption during processing",
                "query": "Explain vector databases and embeddings in detail",
                "max_memory_mb": 1024,
                "baseline_memory_mb": 256
            },
            {
                "test_id": "perf_004",
                "test_type": "scalability",
                "description": "Performance under load",
                "load_levels": [1, 5, 10, 20],
                "sample_query": "How does fine-tuning work?",
                "max_degradation_percent": 50
            }
        ]
        
        return test_cases
    
    def save_dataset(self, data: Dict[str, Any], filename: str):
        """Save dataset to JSON file"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Count main data items for reporting
        item_count = 0
        if 'qa_pairs' in data:
            item_count = len(data['qa_pairs'])
        elif 'retrieval_tests' in data:
            item_count = len(data['retrieval_tests'])
        elif 'generation_tests' in data:
            item_count = len(data['generation_tests'])
        elif 'performance_tests' in data:
            item_count = len(data['performance_tests'])
        else:
            # For combined dataset or config files
            item_count = sum(len(v) for k, v in data.items() if isinstance(v, list) and k != 'documents')
        
        print(f"✅ Saved {filename} with {item_count} items")
    
    def create_complete_dataset(self):
        """Create the complete evaluation dataset"""
        print("🚀 Creating RAG Evaluation Dataset...")
        print("=" * 50)
        
        # Create all dataset components
        qa_pairs = self.create_question_answer_pairs()
        retrieval_tests = self.create_retrieval_test_cases()
        generation_tests = self.create_generation_test_cases()
        performance_tests = self.create_performance_test_cases()
        
        # Create metadata
        metadata = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "description": "RAG System Evaluation Dataset",
            "total_qa_pairs": len(qa_pairs),
            "total_retrieval_tests": len(retrieval_tests),
            "total_generation_tests": len(generation_tests),
            "total_performance_tests": len(performance_tests),
            "categories": list(set(qa["category"] for qa in qa_pairs)),
            "difficulty_levels": list(set(qa["difficulty"] for qa in qa_pairs))
        }
        
        # Save combined dataset
        combined_dataset = {
            "metadata": metadata,
            "documents": self.sample_documents,
            "qa_pairs": qa_pairs,
            "retrieval_tests": retrieval_tests,
            "generation_tests": generation_tests,
            "performance_tests": performance_tests
        }
        
        self.save_dataset(combined_dataset, "evaluation_dataset.json")
        
        # Create test configuration
        test_config = {
            "evaluation_settings": {
                "retrieval_top_k": 5,
                "generation_max_tokens": 512,
                "similarity_threshold": 0.7,
                "timeout_seconds": 30
            },
            "metrics_config": {
                "enable_bleu": True,
                "enable_rouge": True,
                "enable_bertscore": True,
                "enable_faithfulness": True,
                "enable_relevance": True
            },
            "performance_thresholds": {
                "max_response_time_ms": 5000,
                "min_accuracy_percent": 80,
                "max_hallucination_rate": 0.1
            }
        }
        
        self.save_dataset(test_config, "eval_config.json")
        
        print("\n📊 Dataset Summary:")
        print(f"   • {len(qa_pairs)} Question-Answer pairs")
        print(f"   • {len(retrieval_tests)} Retrieval test cases")
        print(f"   • {len(generation_tests)} Generation test cases") 
        print(f"   • {len(performance_tests)} Performance test cases")
        print(f"   • {len(self.sample_documents)} Sample documents")
        print(f"\n📁 Files created in '{self.output_dir}/':")
        print("   • evaluation_dataset.json")
        print("   • eval_config.json")
        print(f"\n✅ Evaluation dataset ready for use with run_rag_evaluation.py")

def main():
    """Main function to create evaluation dataset"""
    print("🚀 Starting create_eval_dataset.py...")
    try:
        creator = EvaluationDatasetCreator()
        creator.create_complete_dataset()
        print("✅ Script completed successfully!")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
