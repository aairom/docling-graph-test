# Quick Start Guide

## Prerequisites Check

Before running the application, ensure:

1. **Python dependencies are installed** ✅ (Completed)
2. **Ollama is running**
3. **Granite4 model is available**

## Important: Use python3, not python

The dependencies were installed for `python3`. Always use:
```bash
python3 app.py  # ✅ Correct
```

NOT:
```bash
python app.py   # ❌ Wrong - will give ModuleNotFoundError
```

## Step 1: Clear Port 7860 (if needed)

If you get "address already in use" error:
```bash
bash scripts/kill-port.sh 7860
```

## Step 2: Verify Ollama is Running

Open a new terminal and run:
```bash
ollama serve
```

Keep this terminal running in the background.

## Step 3: Pull Granite4 Model (if not already available)

In another terminal:
```bash
ollama pull granite4
```

## Step 4: Launch the Application

### Option A: Direct Launch (Recommended for first time)
```bash
cd /Users/alainairom/Devs/docling-graph
python3 app.py
```

The application will automatically find an available port starting from 7860.
Look for the message: "Starting on port XXXX"

Then open: **http://localhost:XXXX** (usually 7860)

### Option B: Using Launch Script (Automated)
```bash
cd /Users/alainairom/Devs/docling-graph
bash scripts/launch.sh
```

This script will:
- Check if Ollama is running
- Pull granite4 model if needed
- Start the application in detached mode
- Save logs to `logs/app.log`

## Step 5: Access the Application

Open your browser and navigate to:
```
http://localhost:7860
```

## Application Features

### Individual Processing Tab
1. Upload a single document (PDF, image, markdown, etc.)
2. Select or upload a template file
3. Configure processing options
4. Click "Process Document"
5. View results and download outputs

### Batch Processing Tab
1. Select multiple files from the `./input` folder
2. Choose a template
3. Configure batch options
4. Click "Process Batch"
5. Monitor progress and download results

## Stopping the Application

### If running directly (Option A):
Press `Ctrl+C` in the terminal

### If using launch script (Option B):
```bash
bash scripts/stop.sh
```

## Troubleshooting

### Issue: "Connection refused" or Ollama errors
**Solution**: Make sure Ollama is running:
```bash
ollama serve
```

### Issue: "Model not found: granite4"
**Solution**: Pull the model:
```bash
ollama pull granite4
```

### Issue: Port 7860 already in use
**Solution**: Stop any existing Gradio applications or change the port in `app.py`:
```python
demo.launch(server_port=7861)  # Use different port
```

### Issue: Module not found errors
**Solution**: Reinstall dependencies:
```bash
python3 -m pip install --user -r requirements.txt
```

## Testing with Sample Documents

1. Place test documents in the `./input` folder
2. Use the provided sample templates in `_samples/` folder:
   - `simple_template.py` - Basic document structure
   - `rheology_template.py` - Research paper analysis

## Output Location

All processed results are saved to:
```
./output/YYYYMMDD_HHMMSS_<filename>/
```

Each output folder contains:
- `graph.json` - Knowledge graph in JSON format
- `graph.md` - Markdown representation
- `graph.html` - Interactive visualization
- `metadata.json` - Processing metadata

## Next Steps

- Read the full documentation in `Docs/user-guide.md`
- Explore example templates in `_samples/`
- Check deployment options in `Docs/deployment-guide.md`

## Support

For issues or questions:
1. Check the logs: `logs/app.log`
2. Review documentation in `Docs/` folder
3. Verify Ollama and granite4 are working: `ollama run granite4 "Hello"`