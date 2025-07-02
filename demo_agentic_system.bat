@echo off
REM Quick Demo Script for Agentic RAG Evaluation System
REM This script demonstrates the autonomous multi-agent evaluation framework

echo ==========================================================
echo             AGENTIC RAG EVALUATION DEMO
echo ==========================================================
echo.
echo This demo showcases autonomous AI agents for RAG evaluation:
echo - 4 specialized evaluation agents with different responsibilities
echo - Autonomous decision-making and adaptive behavior
echo - Real-time state management and decision logging
echo - Simulated continuous optimization and monitoring
echo.

echo [1/3] Setting up agent framework...
python setup_agents.py
echo.

if not exist agent_config.json (
    echo ❌ Agent setup failed. Please check your Python environment.
    pause
    exit /b 1
)

echo [2/3] Starting autonomous evaluation agents...
echo.
echo The agents will run for 60 seconds to demonstrate autonomous behavior.
echo You can monitor their decisions in real-time:
echo.
echo   📊 Agent decisions: Check agent_logs/ directory
echo   📋 Agent state: Check agent_state/ directory
echo   🔍 Live monitoring: tail -f agent_logs/*.log
echo.

REM Run agents for 60 seconds for demonstration
python start_agentic_evaluation.py 60

echo.
echo [3/3] Demo completed! Review agent decisions and state...
echo.
echo 📋 Agent Decision Summary:
echo ----------------------------------------
for %%f in (agent_state\*.json) do (
    echo Agent State: %%~nf
    python -m json.tool "%%f" | findstr "status\|last_updated\|decision" | head -3
    echo.
)

echo.
echo 📁 Files created during demo:
echo   - agent_config.json: Agent configuration
echo   - agent_state/: Agent state files with decision history
echo   - agent_logs/: Detailed agent decision logs
echo   - example_agentic_workflow.py: Standalone workflow example
echo.

echo ✅ Agentic RAG evaluation demo completed successfully!
echo.
echo Next steps for portfolio review:
echo 1. Review agent_config.json to see system architecture
echo 2. Check agent_state/ for autonomous decision examples
echo 3. Run 'python example_agentic_workflow.py' for simple workflow demo
echo 4. Run evaluation dashboard: 'python -m http.server 8000' then open evaluation_dashboard.html
echo.
pause
