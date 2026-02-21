# Environment Configuration Guide

This guide explains how to configure the Docling-Graph Showcase Application using the `.env` file.

## Quick Setup

```bash
# 1. Copy the template
cp .env.template .env

# 2. Edit the .env file with your settings
nano .env  # or use your preferred editor

# 3. Launch the application
python3 app.py
```

## Configuration Options

### Ollama (Local LLM)

For local inference with Ollama:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.1:8b
```

**Setup:**
1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Start Ollama: `ollama serve`
3. Pull models: `ollama pull granite3.1:8b`

### watsonx (IBM watsonx)

For IBM watsonx integration:

```bash
WO_DEVELOPER_EDITION_SOURCE=orchestrate
WO_INSTANCE=your-instance-url
WO_API_KEY=your-api-key
```

**Setup:**
1. Get your watsonx instance URL
2. Generate an API key from your watsonx account
3. Update the values in `.env`

### OpenAI

For OpenAI models (GPT-4, GPT-3.5-turbo):

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

**Setup:**
1. Sign up at https://platform.openai.com/
2. Generate an API key
3. Update the value in `.env`

### Mistral AI

For Mistral models:

```bash
MISTRAL_API_KEY=your-api-key-here
```

**Setup:**
1. Sign up at https://console.mistral.ai/
2. Generate an API key
3. Update the value in `.env`

### Google Gemini

For Google Gemini models:

```bash
GEMINI_API_KEY=your-api-key-here
```

**Setup:**
1. Sign up at https://makersuite.google.com/
2. Generate an API key
3. Update the value in `.env`

## Application Settings

### Server Configuration

```bash
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

- `GRADIO_SERVER_PORT`: Port number for the web interface (default: 7860)
- `GRADIO_SERVER_NAME`: Server address (0.0.0.0 for all interfaces, 127.0.0.1 for localhost only)

### Processing Defaults

```bash
DEFAULT_BACKEND=llm
DEFAULT_PROCESSING_MODE=many-to-one
DEFAULT_USE_CHUNKING=true
```

- `DEFAULT_BACKEND`: Default extraction backend (llm or vlm)
- `DEFAULT_PROCESSING_MODE`: Default processing mode (one-to-one or many-to-one)
- `DEFAULT_USE_CHUNKING`: Enable chunking by default (true or false)

## Security Best Practices

1. **Never commit `.env` to version control**
   - The `.env` file is already in `.gitignore`
   - Only commit `.env.template` with placeholder values

2. **Use strong API keys**
   - Generate unique keys for each environment
   - Rotate keys regularly

3. **Restrict file permissions**
   ```bash
   chmod 600 .env
   ```

4. **Use environment-specific files**
   - `.env.development` for development
   - `.env.production` for production
   - Load the appropriate file based on your environment

## Troubleshooting

### Environment Variables Not Loading

**Problem:** Changes to `.env` not reflected in application

**Solution:**
1. Ensure `.env` is in the project root directory
2. Restart the application after changes
3. Check for syntax errors in `.env` (no spaces around `=`)

### API Key Errors

**Problem:** "Invalid API key" or authentication errors

**Solution:**
1. Verify the API key is correct (no extra spaces)
2. Check if the key has the necessary permissions
3. Ensure the key hasn't expired
4. For watsonx, verify both `WO_INSTANCE` and `WO_API_KEY` are set

### Ollama Connection Issues

**Problem:** Cannot connect to Ollama

**Solution:**
1. Verify Ollama is running: `curl http://localhost:11434/api/tags`
2. Check `OLLAMA_BASE_URL` matches your Ollama installation
3. Ensure the port (11434) is not blocked by firewall

## Example Configurations

### Local Development (Ollama only)

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.1:8b

# Application Settings
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=127.0.0.1
```

### Production (Multiple Providers)

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.1:8b

# watsonx Configuration
WO_DEVELOPER_EDITION_SOURCE=orchestrate
WO_INSTANCE=https://your-instance.watsonx.ibm.com
WO_API_KEY=your-production-api-key

# Remote API Keys
OPENAI_API_KEY=sk-prod-key-here
MISTRAL_API_KEY=prod-key-here

# Application Settings
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

## Additional Resources

- [Main README](../README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Full Documentation](FULL_DOCUMENTATION.md)
- [Changelog](CHANGELOG.md)

## Support

If you encounter issues with environment configuration:

1. Check the [Known Issues](KNOWN_ISSUES.md) document
2. Verify your `.env` syntax matches the template
3. Review the application logs for specific error messages
4. Ensure all required dependencies are installed