# Changelog

## [Enhanced UI] - 2026-02-21

### Added
- **Dynamic Ollama Model Detection**: The application now automatically fetches and displays all available Ollama models from your local installation
- **Model Refresh Button**: Added "🔄 Refresh Ollama Models" button to update the model list without restarting the app
- **Provider-Specific Configuration**: UI now adapts based on selected provider (Ollama vs remote providers)
- **API Key Configuration**: Added secure API key input fields for remote providers (OpenAI, Mistral, Gemini)
- **Ollama Status Indicator**: Real-time status display showing if Ollama is running and how many models are available
- **Enhanced Help Documentation**: Updated help tab with detailed information about model selection and provider configuration

### Changed
- **Documentation Structure**: Moved all documentation files to `/Docs` folder for better organization
  - Original comprehensive README → `Docs/FULL_DOCUMENTATION.md`
  - `PROJECT_SUMMARY.md` → `Docs/PROJECT_SUMMARY.md`
  - `QUICKSTART.md` → `Docs/QUICKSTART.md`
  - `KNOWN_ISSUES.md` → `Docs/KNOWN_ISSUES.md`
- **Root README**: Kept concise README.md in root with links to all documentation in `/Docs`
- **Model Selection UI**: Changed from text input to dropdown for Ollama models
- **Provider Selection**: Enhanced to show/hide relevant configuration fields based on provider choice

### Technical Improvements
- Added `requests` library to requirements.txt for API calls
- Implemented `get_ollama_models()` function to fetch available models via Ollama API
- Implemented `check_ollama_status()` function to verify Ollama connectivity
- Added dynamic UI update functions for provider switching
- Improved error handling for Ollama connection issues

### UI Enhancements
- **Individual Processing Tab**:
  - Dropdown for Ollama models (auto-populated)
  - Text input for remote provider models
  - Collapsible API configuration section
  - Model refresh button
  
- **Batch Processing Tab**:
  - Same enhancements as individual processing
  - Consistent UI across both tabs

### Benefits
1. **Better User Experience**: No need to manually type model names
2. **Reduced Errors**: Dropdown prevents typos in model names
3. **Flexibility**: Easy switching between local and remote providers
4. **Visibility**: Clear indication of Ollama status and available models
5. **Organization**: All documentation in one place (`/Docs` folder)

### Files Modified
- `app.py` - Enhanced with dynamic model detection and improved UI
- `requirements.txt` - Added requests library
- `README.md` - Updated with links to all documentation in `/Docs`
- Created `Docs/CHANGELOG.md` - This file

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

### Using Remote Providers
1. Launch app: `python3 app.py`
2. Select provider (openai, mistral, or gemini)
3. Enter your API key in the configuration section
4. Type the model name (e.g., "gpt-4", "mistral-large-latest")
5. Process your documents

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