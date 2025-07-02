FROM ollama/ollama

# Start Ollama service and pull the lightweight model
# This creates a custom image with llama3.2:1b pre-installed
RUN ollama serve & \
    sleep 10 && \
    ollama pull llama3.2:1b

# Set the default command
CMD ["ollama", "serve"]
