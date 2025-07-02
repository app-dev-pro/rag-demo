# Quick Observability Setup Guide

## Current - **Error monitoring and debugging
- **A/B testing capabilities

### Professional Benefitsur RAG system is running but observability is not yet configured:
- ✅ Backend: Running at http://localhost:8000
- 🔶 LangSmith: Not configured

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install langsmith structlog
```

### Step 2: Get API Keys

**LangSmith:**
1. Visit https://smith.langchain.com
2. Create account and login
3. Go to Settings → API Keys
4. Generate new API key

### Step 3: Update Environment
Add these to your `.env` file:
```bash
# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=rag-demo
```

### Step 4: Restart System
```bash
docker-compose down
docker-compose up -d
```

### Step 5: Verify
```bash
curl http://localhost:8000/
# Should show: "langsmith": true
```

## What You'll Get

### LangSmith Dashboard
- Real-time request tracing
- Performance analytics
- Error monitoring and debugging
- A/B testing capabilities

### Professional Benefits
- **Enterprise-grade monitoring** from day one
- **Production-ready observability** practices
- **Industry-standard tools** experience
- **AI engineering best practices** demonstration

## Need Help?
- 📖 Full guide: `OBSERVABILITY_FRAMEWORK.md`
- ⚡ Auto setup: Run `setup_observability.bat`
- 🔍 Check status: Visit portfolio page and click "Check Status"

This observability setup demonstrates professional AI engineering practices that are essential for production RAG deployments.
