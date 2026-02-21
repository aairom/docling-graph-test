# Changelog

## [Template System + Enhanced UI] - 2026-02-21

### Added
- **Template System Integration**
  - Dynamic template loading from `templates/` directory
  - Template selection dropdown in UI with real-time descriptions
  - Support for domain-specific templates (billing, research, ID cards, insurance, general)
  - Created comprehensive `TEMPLATE_GUIDE.md` documentation (438 lines)
  - Automatic template discovery and loading at startup
  - Template information display showing description for selected template
  
- **Dynamic Ollama Model Detection**: The application now automatically fetches and displays all available Ollama models from your local installation
- **Model Refresh Button**: Added "🔄 Refresh Ollama Models" button to update the model list without restarting the app
- **Provider-Specific Configuration**: UI now adapts based on selected provider (Ollama vs remote providers)
- **watsonx Provider Support**: Added IBM watsonx as a provider option with configuration via .env file
- **Environment Configuration**: Created `.env.template` for easy configuration of all providers
- **API Key Configuration**: Added secure API key input fields for remote providers (OpenAI, Mistral, Gemini, watsonx)
- **Ollama Status Indicator**: Real-time status display showing if Ollama is running and how many models are available
- **Enhanced Help Documentation**: Updated help tab with detailed information about model selection, provider configuration, and template usage

### Changed
- **Documentation Structure**: Moved all documentation files to `/Docs` folder for better organization
  - Original comprehensive README → `Docs/FULL_DOCUMENTATION.md`
  - `PROJECT_SUMMARY.md` → `Docs/PROJECT_SUMMARY.md`
  - `QUICKSTART.md` → `Docs/QUICKSTART.md`
  - `KNOWN_ISSUES.md` → `Docs/KNOWN_ISSUES.md`
  - Added `TEMPLATE_GUIDE.md` → Complete guide for template creation and usage
- **Root README**: Kept concise README.md in root with links to all documentation in `/Docs`
- **Model Selection UI**: Changed from text input to dropdown for Ollama models
- **Provider Selection**: Enhanced to show/hide relevant configuration fields based on provider choice
- **Processing Functions**: Updated to accept template parameter for flexible extraction
- **Batch Processing**: Enhanced to support template selection

### Technical Improvements
- Added `requests` library to requirements.txt for API calls
- Implemented `get_ollama_models()` function to fetch available models via Ollama API
- Implemented `check_ollama_status()` function to verify Ollama connectivity
- Added dynamic UI update functions for provider switching
- Improved error handling for Ollama connection issues
- **Template Loading System**:
  - `load_template_from_file()` - Dynamically loads Pydantic templates from Python files
  - `get_available_templates()` - Discovers and catalogs all available templates
  - Automatic detection of root template classes via `graph_id_fields`
  - Support for templates in both `templates/` and `_samples/` directories

### UI Enhancements
- **Individual Processing Tab**:
  - Template selection dropdown with descriptions
  - Real-time template description display
  - Dropdown for Ollama models (auto-populated)
  - Text input for remote provider models
  - Collapsible API configuration section
  - Model refresh button
  
- **Batch Processing Tab**:
  - Template selection dropdown with descriptions
  - Same enhancements as individual processing
  - Consistent UI across both tabs

### Benefits
1. **Domain-Specific Extraction**: Choose templates tailored to your document type
2. **Better User Experience**: No need to manually type model names or create templates from scratch
3. **Reduced Errors**: Dropdown prevents typos in model names and template selection
4. **Flexibility**: Easy switching between local and remote providers, and between templates
5. **Visibility**: Clear indication of Ollama status, available models, and template descriptions
6. **Organization**: All documentation in one place (`/Docs` folder)
7. **Extensibility**: Easy to add custom templates without modifying core code

### Files Modified
- `app.py` - Enhanced with template system, dynamic model detection, watsonx support, and environment variable loading
- `requirements.txt` - Added requests library
- `README.md` - Updated with links to all documentation in `/Docs` and configuration instructions
- Created `.env.template` - Environment configuration template
- Created `Docs/CHANGELOG.md` - This file
- Created `Docs/TEMPLATE_GUIDE.md` - Comprehensive template creation and usage guide

### Files Moved to /Docs
- Original comprehensive README → `Docs/FULL_DOCUMENTATION.md`
- `PROJECT_SUMMARY.md` → `Docs/PROJECT_SUMMARY.md`
- `QUICKSTART.md` → `Docs/QUICKSTART.md`
- `KNOWN_ISSUES.md` → `Docs/KNOWN_ISSUES.md`

## Usage Examples

### Using Ollama (Local)
1. Start Ollama: `ollama serve`
2. Pull models: `ollama pull granite4`, `ollama pull llama3`
3. Launch app: `python3 app.py`
4. Select "ollama" as provider
5. Choose your model from the dropdown
6. Click "🔄 Refresh Ollama Models" if you pull new models

### Using watsonx
1. Copy `.env.template` to `.env`
2. Set `WO_INSTANCE` and `WO_API_KEY` in `.env`
3. Launch app: `python3 app.py`
4. Select "watsonx" as provider
5. Choose your watsonx model
6. Process your documents

### Using Other Remote Providers
1. Copy `.env.template` to `.env` (optional, can also enter in UI)
2. Launch app: `python3 app.py`
3. Select provider (openai, mistral, or gemini)
4. Enter your API key in the configuration section
5. Type the model name (e.g., "gpt-4", "mistral-large-latest")
6. Process your documents

## Migration Notes

If you're upgrading from a previous version:
1. Documentation is now in `/Docs` folder
2. Update any scripts that reference old documentation paths
3. The new UI will automatically detect your Ollama models
4. No changes needed to existing workflows

## Future Enhancements

Potential improvements for future versions:
- Model performance metrics display
- Model comparison features
- Saved provider configurations
- Model download/management from UI
- Cost estimation for remote providers