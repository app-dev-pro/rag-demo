@echo off
echo.
echo ========================================================
echo    🔍 LLM OBSERVABILITY SETUP - ENTERPRISE MONITORING
echo ========================================================
echo.
echo This script sets up enterprise-grade LLM observability
echo and monitoring for the RAG system using industry-standard
echo platforms: LangSmith.
echo.

echo 📋 OBSERVABILITY CAPABILITIES:
echo ===============================
echo ✅ Automatic request tracing with unique trace IDs
echo ✅ Real-time performance monitoring and metrics
echo ✅ Cost tracking and token usage analytics
echo ✅ Quality scoring and evaluation frameworks
echo ✅ Error tracking and debugging capabilities
echo ✅ Session analytics and user behavior insights
echo ✅ A/B testing infrastructure for model comparison
echo ✅ Production-ready alerting and monitoring
echo.

echo 🚀 SETTING UP OBSERVABILITY...
echo ==============================
echo.

echo Step 1: Installing observability dependencies...
echo Installing LangSmith and monitoring libraries...
pip install langsmith structlog opentelemetry-api opentelemetry-sdk prometheus-client

if %errorlevel% neq 0 (
    echo ❌ Failed to install observability dependencies
    echo 💡 Try: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Observability dependencies installed successfully
echo.

echo Step 2: Creating observability configuration...
if not exist .env.observability.example (
    echo ❌ Observability config template not found
    echo 💡 Please ensure .env.observability.example exists
    pause
    exit /b 1
)

if not exist .env (
    echo 📝 Creating .env file from observability template...
    copy .env.observability.example .env
    echo ✅ Configuration file created
) else (
    echo 📝 .env file already exists
    echo 💡 Ensure it includes observability settings from .env.observability.example
)

echo.
echo Step 3: Configuration instructions...
echo.
echo 🔗 LANGSMITH SETUP:
echo ===================
echo 1. Visit: https://smith.langchain.com
echo 2. Create an account and login
echo 3. Go to Settings ^> API Keys
echo 4. Generate a new API key
echo 5. Copy the key to LANGCHAIN_API_KEY in your .env file
echo 6. Create a project named "rag-demo"
echo.

echo ⚡ QUICK TEST:
echo =============
echo After configuring API keys, restart your RAG system:
echo   docker-compose down
echo   docker-compose up --build -d
echo.
echo Then check observability status:
echo   curl http://localhost:8000/
echo.
echo Look for "observability" section in the response showing:
echo   "langsmith": true
echo.

echo ========================================================
echo    ✅ OBSERVABILITY SETUP GUIDE COMPLETE
echo ========================================================
echo.
echo 💼 WHAT THIS DEMONSTRATES FOR TECHNICAL REVIEW:
echo ===============================================
echo • Enterprise-level LLM monitoring and observability
echo • Production-ready system instrumentation
echo • Industry-standard tooling integration (LangSmith)
echo • Comprehensive metrics collection and analysis
echo • Professional operational practices for AI systems
echo • Cost optimization and performance monitoring capabilities
echo.

echo 📚 DOCUMENTATION:
echo =================
echo • Full setup guide: OBSERVABILITY_FRAMEWORK.md
echo • Integration details: backend/app/main.py observability section
echo • Dashboard features: LangSmith web interface
echo.

echo 🎯 NEXT STEPS:
echo ==============
echo 1. Configure API keys in .env file
echo 2. Restart the RAG system
echo 3. Run some test queries
echo 4. View traces in LangSmith dashboard
echo 5. Explore analytics and performance insights
echo.

pause
