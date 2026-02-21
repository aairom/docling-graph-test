# Known Issues and Warnings

## pypdfium2 AssertionError Warnings

### Description
When processing PDF documents, you may see warnings like:
```
Exception ignored in: <finalize object at 0xb2855b68a0; dead>
Traceback (most recent call last):
  ...
  File ".../pypdfium2/internal/bases.py", line 67, in _close_template
    assert parent is None or not parent._tree_closed()
AssertionError:
```

### Impact
**These warnings are harmless and can be safely ignored.** They are cleanup warnings from the pypdfium2 library (used by docling for PDF processing) and do not affect the functionality of the application.

### Why This Happens
The warnings occur during Python's garbage collection when PDF objects are being cleaned up. This is a known issue in pypdfium2 related to the order of object finalization.

### What's Actually Working
Despite these warnings, the application is functioning correctly:
- ✅ PDF documents are being processed
- ✅ Text is being extracted
- ✅ LLM is being called
- ✅ Knowledge graphs are being generated
- ✅ Results are being saved

### Verification
You can verify the application is working by checking:
1. The console shows: `[DocumentProcessor] Extracted full document Markdown`
2. The console shows: `[DirectExtraction] Calling LLM...`
3. Output files are created in the `./output` directory
4. The Gradio UI shows processing progress and results

### Future Fix
This issue is tracked in the pypdfium2 project and will be resolved in a future version. For now, these warnings can be safely ignored.

## Other Known Issues

### Port Already in Use
**Error:** `OSError: Cannot find empty port in range: 7860-7860`

**Solution:**
```bash
# Kill process on port 7860
bash scripts/kill-port.sh 7860

# Or let the app auto-find a free port (it tries 7860-7869)
python3 app.py
```

### Module Not Found: gradio
**Error:** `ModuleNotFoundError: No module named 'gradio'`

**Solution:**
```bash
# Always use python3, not python
python3 -m pip install --user -r requirements.txt
python3 app.py
```

### Ollama Connection Error
**Error:** Connection refused to `http://localhost:11434`

**Solution:**
```bash
# Start Ollama service
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

### Model Not Found: granite4
**Error:** Model 'granite4' not found

**Solution:**
```bash
# Pull the model
ollama pull granite4

# Verify it's available
ollama list
```

## Performance Notes

### Large Documents
For documents larger than 100 pages:
- Enable chunking (default: enabled)
- Processing may take several minutes
- Monitor progress in the console output

### Memory Usage
- VLM (vision) backend uses more memory than LLM
- For low-memory systems, use LLM backend with chunking enabled
- Consider processing documents individually rather than in batch

## Getting Help

If you encounter issues not listed here:

1. **Check the logs:**
   ```bash
   tail -f logs/docling-graph-app.log
   ```

2. **Verify Ollama:**
   ```bash
   ollama list
   ollama run granite4 "Hello"
   ```

3. **Check documentation:**
   - `./Docs/user-guide.md` - Usage instructions
   - `./Docs/deployment-guide.md` - Deployment options
   - `./QUICKSTART.md` - Quick start guide

4. **Test with sample:**
   ```bash
   # Place a small PDF in ./input
   # Run the app and process it
   python3 app.py