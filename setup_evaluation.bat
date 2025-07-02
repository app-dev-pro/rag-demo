@echo off
echo 🔍 RAG Pipeline Evaluation Setup
echo ================================
echo.

echo ✅ Step 1: Installing evaluation dependencies...
pip install -r requirements_eval.txt

echo.
echo ✅ Step 2: Creating evaluation dataset...
python create_eval_dataset.py

echo.
echo ✅ Step 3: Running evaluation pipeline...
echo Note: This requires your RAG system to be running (docker-compose up -d)
echo.

echo 🚀 Ready to run evaluation!
echo.
echo 📋 Available commands:
echo   python run_rag_evaluation.py    - Run complete evaluation
echo   evaluation_dashboard.html       - Open dashboard in browser
echo.

echo 💡 For technical reviewers:
echo This evaluation framework demonstrates:
echo   • Enterprise-level AI system testing
echo   • Multiple evaluation metrics (ROUGE, faithfulness, etc.)
echo   • Performance benchmarking capabilities
echo   • Production-ready monitoring practices
echo   • Systematic quality assurance approach
echo.

pause
