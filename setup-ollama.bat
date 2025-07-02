@echo off
echo Setting up Ollama with llama3.2:1b model...

echo Waiting for Ollama to start...
timeout /t 10 /nobreak > nul

echo Pulling llama3.2:1b model (lightweight)...
docker exec rag-demo-ollama-1 ollama pull llama3.2:1b

echo Setup complete! Ollama is ready with llama3.2:1b model.
