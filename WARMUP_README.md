# AI Agent Model Warmup Solution

This repository includes a model warmup solution to eliminate the long startup delays when first running AI agents that use Ollama with llama3.2.

## Problem Solved

When running AI agents for the first time in a session, there was a significant delay (multiple minutes) as the llama3.2 model needed to be loaded through the Ollama interface. This warmup solution preloads the model, making subsequent agent calls much faster.

## Files Added

- `scripts/warmup_model.py` - Main warmup script that tests all three client interfaces used by agents
- `scripts/warmup.sh` - Shell wrapper that handles virtual environment setup
- `warmup_model.py` - Root-level convenience script
- `venv/` - Virtual environment with required packages

## Modified Files

- `scripts/startOllama.sh` - Now includes automatic model warmup during startup
- `scripts/warmup.sh` - Updated to handle virtual environment management

## Usage

### Automatic Warmup (Recommended)
The warmup is automatically integrated into the startup process via `scripts/startOllama.sh`. When you start a new Codespace, the model will be warmed up automatically.

### Manual Warmup
You can manually warm up the model anytime with either of these commands:

```bash
# Option 1: Using the shell script (recommended)
./scripts/warmup.sh

# Option 2: Using the Python wrapper
python3 warmup_model.py
```

### Individual Interface Testing
The warmup script tests three different client interfaces:

1. **langchain_ollama** - Used by `agent1.py`, `agent4.py`, etc.
2. **OpenAI client** - Used by `rag_agent.py`, etc.
3. **Async ollama client** - Used by `learning.py`, `goal.py`, etc.

## Performance Impact

- **First warmup**: ~12-15 seconds (loads model into memory)
- **Subsequent warmups**: ~0.4 seconds (model already loaded)
- **Agent responses**: Near-instantaneous after warmup vs multiple minutes without

## Requirements

The warmup solution automatically handles dependency installation in a virtual environment:
- `ollama` - Core Ollama Python client
- `langchain-ollama` - LangChain Ollama integration
- `openai` - OpenAI-compatible client
- `requests` - HTTP requests for health checks

## Technical Details

The warmup script:
1. Checks if Ollama server is running
2. Creates a virtual environment if it doesn't exist
3. Installs required dependencies
4. Makes simple test requests to each client interface
5. Reports success/failure for each interface
6. Provides timing information

This ensures the llama3.2 model is loaded into memory and ready for fast responses from any of your AI agents.

## Integration with Codespaces

The warmup is integrated into the Codespace startup process through:
- `.devcontainer/devcontainer.json` calls `scripts/startOllama.sh`
- `scripts/startOllama.sh` now includes the warmup step
- The warmup runs after model download but before Ollama is stopped

This means your agents will be ready to use immediately when your Codespace finishes starting up.