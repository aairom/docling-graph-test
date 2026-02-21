# Input Directory

Place your documents here for processing.

## Supported Formats

- **PDF** - `.pdf`
- **Images** - `.png`, `.jpg`, `.jpeg`, `.tiff`
- **Markdown** - `.md`
- **Office** - `.docx`, `.pptx`, `.xlsx`
- **HTML** - `.html`
- **Text** - `.txt`

## Usage

1. Copy or move your documents to this directory
2. Open the application at http://localhost:7860
3. Select your document from the dropdown
4. Configure processing options
5. Click "Process Document"

## Example

```bash
# Copy a PDF
cp /path/to/document.pdf input/

# Or use drag-and-drop in your file manager
```

## Tips

- **File Names** - Use descriptive names without special characters
- **File Size** - Large files (>50MB) may take longer to process
- **Batch Processing** - Place multiple files here for batch processing
- **Organization** - Keep files organized by type or project

## After Processing

Processed documents remain in this directory. Results are saved to the `output/` directory with timestamps.