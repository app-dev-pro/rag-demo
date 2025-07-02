#!/bin/bash

echo "Setting up Ollama with llama3.2:1b model..."

# Wait for Ollama service to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull the llama3.2:1b model
echo "Pulling llama3.2:1b model..."
docker exec rag-demo-ollama-1 ollama pull llama3.2:1b

echo "Setup complete! Ollama is ready with llama3.2:1b model."
