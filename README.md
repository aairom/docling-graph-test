# Docling-Graph Showcase Application

**Transform documents into validated knowledge graphs using docling-graph with local Ollama LLM**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)
[![Ollama](https://img.shields.io/badge/Ollama-compatible-green.svg)](https://ollama.com/)

---

## 🚀 Quick Start

```bash
# 1. Configure environment (optional)
cp .env.template .env
# Edit .env with your settings (Ollama, watsonx, or other providers)

# 2. Install Ollama (for local inference)
curl -fsSL https://ollama.com/install.sh | sh

# 3. Pull a model (e.g., granite4 or llama3)
ollama pull granite4

# 4. Launch application
./scripts/launch.sh
```

The application will be available at **http://localhost:7860**

## 📚 Documentation

All documentation is available in the [`Docs/`](Docs/) directory:

- **[Quick Start Guide](Docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Environment Setup](Docs/ENVIRONMENT_SETUP.md)** - Configure providers and API keys
- **[Full Documentation](Docs/FULL_DOCUMENTATION.md)** - Comprehensive guide with all features
- **[User Guide](Docs/user-guide.md)** - Complete usage instructions
- **[Architecture](Docs/architecture.md)** - System design and components
- **[Deployment Guide](Docs/deployment-guide.md)** - Production deployment
- **[API Reference](Docs/api-reference.md)** - Function documentation
- **[Project Summary](Docs/PROJECT_SUMMARY.md)** - Project overview
- **[Known Issues](Docs/KNOWN_ISSUES.md)** - Troubleshooting guide
- **[Changelog](Docs/CHANGELOG.md)** - Recent updates and enhancements

## ✨ Key Features

- 🎯 **Intuitive Web UI** - User-friendly Gradio interface
- 📄 **Multiple Formats** - PDF, images, markdown, Office documents
- 🔄 **Batch Processing** - Process multiple documents simultaneously
- 🧠 **Multiple LLM Providers** - Ollama (local), watsonx, OpenAI, Mistral, Gemini
- 🔧 **Environment Configuration** - Easy setup with .env file
- 📊 **Interactive Graphs** - Visualize knowledge graphs
- 💾 **Multiple Exports** - CSV, JSON, HTML formats
- 🐳 **Container Ready** - Docker and Kubernetes support

## 🎯 Use Cases

- Research papers analysis
- Legal document processing
- Technical manual extraction
- Business report insights
- Medical record structuring

## 📁 Project Structure

```
docling-graph-showcase/
├── README.md              # Main README (this file)
├── .env.template          # Environment configuration template
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image
├── input/                 # Input documents
├── output/                # Processed results
├── scripts/               # Automation scripts
├── Docs/                  # 📚 All documentation
└── k8s/                   # Kubernetes manifests
```

## ⚙️ Configuration

Copy `.env.template` to `.env` and configure your settings:

```bash
cp .env.template .env
```

### Supported Providers

- **Ollama** (Local) - No API key needed, just install and pull models
- **watsonx** - Set `WO_INSTANCE` and `WO_API_KEY`
- **OpenAI** - Set `OPENAI_API_KEY`
- **Mistral** - Set `MISTRAL_API_KEY`
- **Gemini** - Set `GEMINI_API_KEY`

## 🛠️ Scripts

- `./scripts/launch.sh` - Start the application
- `./scripts/stop.sh` - Stop the application
- `./scripts/kill-port.sh` - Free up a port

## 🤝 Contributing

Contributions are welcome! Please see the documentation for guidelines.

## 📝 License

This project is licensed under the MIT License.

---

**Made with ❤️ using Docling-Graph**

[Documentation](Docs/) • [Quick Start](Docs/QUICKSTART.md) • [Architecture](Docs/architecture.md)