"""
Docling-Graph Showcase Application
A Gradio-based UI for document processing using docling-graph with Ollama/Granite4
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
import json
import traceback

import gradio as gr
from rich.console import Console
from rich.panel import Panel

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from docling_graph import PipelineConfig, run_pipeline
except ImportError:
    print("Error: docling-graph not installed. Run: pip install docling-graph")
    sys.exit(1)

console = Console()

# Configuration
INPUT_DIR = project_root / "input"
OUTPUT_DIR = project_root / "output"
SAMPLES_DIR = project_root / "_samples"

# Ensure directories exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Ollama configuration for local LLM
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "granite4"


def get_timestamp() -> str:
    """Generate timestamp for output files."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def list_input_files() -> List[str]:
    """List all files in the input directory."""
    if not INPUT_DIR.exists():
        return []
    
    files = []
    for file_path in INPUT_DIR.iterdir():
        if file_path.is_file():
            files.append(file_path.name)
    return sorted(files)


def process_document(
    file_path: str,
    backend: str,
    processing_mode: str,
    use_chunking: bool,
    provider: str,
    model: str,
    progress=gr.Progress()
) -> Tuple[str, str, str, str]:
    """
    Process a single document using docling-graph.
    
    Args:
        file_path: Path to the document
        backend: Extraction backend (llm or vlm)
        processing_mode: Processing mode (one-to-one or many-to-one)
        use_chunking: Whether to use chunking
        provider: LLM provider (ollama, mistral, openai, etc.)
        model: Model name
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (status_message, graph_html_path, nodes_csv_path, edges_csv_path)
    """
    try:
        progress(0.0, desc="🔧 Initializing...")
        
        # Create timestamped output directory
        timestamp = get_timestamp()
        output_subdir = OUTPUT_DIR / f"run_{timestamp}"
        output_subdir.mkdir(exist_ok=True)
        
        # Prepare source path
        source_path = INPUT_DIR / file_path
        if not source_path.exists():
            return f"Error: File not found: {file_path}", "", "", ""
        
        progress(0.1, desc="📋 Configuring pipeline...")
        
        # Import a simple template for demonstration
        # In production, you would use domain-specific templates
        from _samples.simple_template import SimpleDocument
        
        # Configure pipeline
        config_dict = {
            "source": str(source_path),
            "template": SimpleDocument,
            "backend": backend,
            "inference": "remote" if provider != "ollama" else "remote",
            "processing_mode": processing_mode,
            "use_chunking": use_chunking,
            "output_dir": str(output_subdir),
        }
        
        # Add provider-specific configuration
        if provider == "ollama":
            config_dict["provider_override"] = "ollama"
            config_dict["model_override"] = f"ollama/{model}"
            config_dict["api_base"] = OLLAMA_BASE_URL
        else:
            config_dict["provider_override"] = provider
            config_dict["model_override"] = model
        
        config = PipelineConfig(**config_dict)
        
        progress(0.2, desc="⚙️ Processing document...")
        console.print("  • Converting document to markdown")
        
        progress(0.3, desc="📄 Converting to markdown...")
        
        progress(0.5, desc="🧠 Extracting data with LLM...")
        console.print("  • Extracting structured data")
        
        progress(0.7, desc="🔗 Building knowledge graph...")
        
        # Run pipeline
        context = run_pipeline(config)
        
        progress(0.9, desc="💾 Generating outputs...")
        console.print("  • Saving results")
        
        # Get results
        graph = context.knowledge_graph
        models = context.extracted_models
        
        # Save results with timestamp
        timestamp_str = timestamp
        
        # Save report in the style of 02_quickstart_llm_pdf.py
        report_path = output_subdir / f"report_{timestamp_str}.md"
        with open(report_path, "w") as f:
            f.write(f"# Document Processing Report\n\n")
            f.write(f"## Configuration\n\n")
            f.write(f"- **Source:** {file_path}\n")
            f.write(f"- **Template:** SimpleDocument\n")
            f.write(f"- **Backend:** {backend.upper()} ({'Large Language Model' if backend == 'llm' else 'Vision Language Model'})\n")
            f.write(f"- **Provider:** {provider}\n")
            f.write(f"- **Model:** {model}\n")
            f.write(f"- **Mode:** {processing_mode}\n")
            f.write(f"- **Chunking:** {'Enabled' if use_chunking else 'Disabled'}\n\n")
            
            f.write(f"## Results\n\n")
            f.write(f"**Extracted:** {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges\n\n")
            
            f.write(f"## What Happened\n\n")
            f.write(f"- Document converted to markdown using Docling\n")
            if use_chunking:
                f.write(f"- Document split into chunks respecting context limits\n")
                f.write(f"- Each chunk processed by {provider} {backend.upper()}\n")
                f.write(f"- Results merged programmatically\n")
            else:
                f.write(f"- Document processed by {provider} {backend.upper()}\n")
            f.write(f"- Knowledge graph built from extracted entities\n\n")
            
            f.write(f"## Output Files\n\n")
            f.write(f"- **nodes.csv:** Extracted entities\n")
            f.write(f"- **edges.csv:** Relationships between entities\n")
            f.write(f"- **graph.html:** Interactive knowledge graph visualization\n")
            f.write(f"- **document.md:** Markdown version of the document\n")
            f.write(f"- **report.md:** This extraction report\n")
        
        # Find generated files
        graph_html = list(output_subdir.glob("*.html"))
        nodes_csv = list(output_subdir.glob("*nodes*.csv"))
        edges_csv = list(output_subdir.glob("*edges*.csv"))
        
        graph_html_path = str(graph_html[0]) if graph_html else ""
        nodes_csv_path = str(nodes_csv[0]) if nodes_csv else ""
        edges_csv_path = str(edges_csv[0]) if edges_csv else ""
        
        progress(1.0, desc="✅ Complete!")
        
        status = f"""## ✅ Success!

**Extracted:** {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges

### 📋 Configuration
- **Source:** {file_path}
- **Backend:** {backend.upper()} ({'Large Language Model' if backend == 'llm' else 'Vision Language Model'})
- **Provider:** {provider}
- **Model:** {model}
- **Mode:** {processing_mode}

### 💡 What Happened
- Document converted to markdown using Docling
{f'- Document split into chunks respecting context limits' if use_chunking else ''}
{f'- Each chunk processed by {provider} {backend.upper()}' if use_chunking else f'- Document processed by {provider} {backend.upper()}'}
{f'- Results merged programmatically' if use_chunking else ''}
- Knowledge graph built from extracted entities

### 📁 Output Files
**Directory:** `{output_subdir.name}`

- **report_{timestamp_str}.md** - Extraction report and statistics
- **{Path(graph_html_path).name if graph_html_path else 'graph.html'}** - Interactive visualization
- **{Path(nodes_csv_path).name if nodes_csv_path else 'nodes.csv'}** - Extracted entities
- **{Path(edges_csv_path).name if edges_csv_path else 'edges.csv'}** - Relationships
"""
        
        return status, graph_html_path, nodes_csv_path, edges_csv_path
        
    except Exception as e:
        error_msg = f"""❌ Error Processing Document

**Error:** {str(e)}

**Traceback:**
```
{traceback.format_exc()}
```

**Troubleshooting:**
- Ensure Ollama is running: `ollama serve`
- Check if model is available: `ollama list`
- Verify input file exists in ./input directory
- Check API keys if using remote providers
"""
        return error_msg, "", "", ""


def batch_process_documents(
    backend: str,
    processing_mode: str,
    use_chunking: bool,
    provider: str,
    model: str,
    progress=gr.Progress()
) -> str:
    """
    Process all documents in the input directory.
    
    Returns:
        Status message with results
    """
    try:
        files = list_input_files()
        if not files:
            return "❌ No files found in input directory"
        
        results = []
        total_files = len(files)
        
        for idx, file_name in enumerate(files):
            progress((idx + 1) / total_files, desc=f"Processing {file_name}...")
            
            status, _, _, _ = process_document(
                file_name,
                backend,
                processing_mode,
                use_chunking,
                provider,
                model,
                progress=gr.Progress()
            )
            
            results.append(f"### {file_name}\n{status}\n")
        
        summary = f"""# Batch Processing Complete

**Total Files:** {total_files}
**Output Directory:** {OUTPUT_DIR}

---

{"".join(results)}
"""
        return summary
        
    except Exception as e:
        return f"❌ Batch Processing Error: {str(e)}\n\n{traceback.format_exc()}"


# Create Gradio Interface
with gr.Blocks(title="Docling-Graph Showcase") as app:
    gr.Markdown("""
    # 🔍 Docling-Graph Showcase
    
    Transform documents into validated knowledge graphs using docling-graph with local Ollama/Granite4 LLM.
    
    **Status:** 🟢 Application Running | **Model:** Granite4 | **Provider:** Ollama (Local)
    
    **Features:**
    - 📄 Individual or batch document processing
    - 🧠 Local LLM inference with Ollama
    - 📊 Interactive graph visualization
    - 💾 CSV export for nodes and edges
    
    ---
    """)
    
    with gr.Tabs():
        # Individual Processing Tab
        with gr.Tab("📄 Individual Processing"):
            gr.Markdown("### Process a single document")
            
            with gr.Row():
                with gr.Column(scale=1):
                    file_dropdown = gr.Dropdown(
                        choices=list_input_files(),
                        label="Select Document",
                        info="Files from ./input directory"
                    )
                    refresh_btn = gr.Button("🔄 Refresh File List", size="sm")
                    
                    backend_radio = gr.Radio(
                        choices=["llm", "vlm"],
                        value="llm",
                        label="Extraction Backend",
                        info="LLM for text, VLM for images"
                    )
                    
                    mode_radio = gr.Radio(
                        choices=["one-to-one", "many-to-one"],
                        value="many-to-one",
                        label="Processing Mode",
                        info="one-to-one: separate outputs per page, many-to-one: merged output"
                    )
                    
                    chunking_check = gr.Checkbox(
                        value=True,
                        label="Use Chunking",
                        info="Split large documents for LLM context limits"
                    )
                    
                    provider_dropdown = gr.Dropdown(
                        choices=["ollama", "mistral", "openai", "gemini"],
                        value="ollama",
                        label="Provider",
                        info="LLM provider (ollama for local)"
                    )
                    
                    model_text = gr.Textbox(
                        value=OLLAMA_MODEL,
                        label="Model Name",
                        info="Model identifier (e.g., granite3.1:8b for Ollama)"
                    )
                    
                    process_btn = gr.Button("🚀 Process Document", variant="primary")
                
                with gr.Column(scale=2):
                    status_output = gr.Markdown(label="Status")
                    
                    with gr.Accordion("📊 Outputs", open=False):
                        graph_file = gr.File(label="Graph HTML")
                        nodes_file = gr.File(label="Nodes CSV")
                        edges_file = gr.File(label="Edges CSV")
            
            # Wire up individual processing
            refresh_btn.click(
                fn=lambda: gr.Dropdown(choices=list_input_files()),
                outputs=file_dropdown
            )
            
            process_btn.click(
                fn=process_document,
                inputs=[
                    file_dropdown,
                    backend_radio,
                    mode_radio,
                    chunking_check,
                    provider_dropdown,
                    model_text
                ],
                outputs=[status_output, graph_file, nodes_file, edges_file]
            )
        
        # Batch Processing Tab
        with gr.Tab("📚 Batch Processing"):
            gr.Markdown("### Process all documents in the input directory")
            
            with gr.Row():
                with gr.Column(scale=1):
                    batch_backend = gr.Radio(
                        choices=["llm", "vlm"],
                        value="llm",
                        label="Extraction Backend"
                    )
                    
                    batch_mode = gr.Radio(
                        choices=["one-to-one", "many-to-one"],
                        value="many-to-one",
                        label="Processing Mode"
                    )
                    
                    batch_chunking = gr.Checkbox(
                        value=True,
                        label="Use Chunking"
                    )
                    
                    batch_provider = gr.Dropdown(
                        choices=["ollama", "mistral", "openai", "gemini"],
                        value="ollama",
                        label="Provider"
                    )
                    
                    batch_model = gr.Textbox(
                        value=OLLAMA_MODEL,
                        label="Model Name"
                    )
                    
                    batch_btn = gr.Button("🚀 Process All Documents", variant="primary")
                
                with gr.Column(scale=2):
                    batch_status = gr.Markdown(label="Batch Status")
            
            # Wire up batch processing
            batch_btn.click(
                fn=batch_process_documents,
                inputs=[
                    batch_backend,
                    batch_mode,
                    batch_chunking,
                    batch_provider,
                    batch_model
                ],
                outputs=batch_status
            )
        
        # Help Tab
        with gr.Tab("ℹ️ Help"):
            gr.Markdown("""
            ## Getting Started
            
            ### 1. Setup Ollama
            ```bash
            # Install Ollama
            curl -fsSL https://ollama.com/install.sh | sh
            
            # Start Ollama service
            ollama serve
            
            # Pull Granite model
            ollama pull granite3.1:8b
            ```
            
            ### 2. Add Documents
            Place your documents (PDF, images, markdown, etc.) in the `./input` directory.
            
            ### 3. Process Documents
            - **Individual:** Select a file and click "Process Document"
            - **Batch:** Click "Process All Documents" to process everything
            
            ### 4. View Results
            Results are saved in `./output` with timestamps:
            - `summary_TIMESTAMP.md` - Processing summary
            - `graph.html` - Interactive visualization
            - `nodes.csv` - Extracted entities
            - `edges.csv` - Relationships
            
            ## Configuration
            
            ### Backends
            - **LLM:** Text-based extraction (best for PDFs, documents)
            - **VLM:** Vision-based extraction (best for images, forms)
            
            ### Processing Modes
            - **one-to-one:** Each page becomes a separate output
            - **many-to-one:** All pages merged into single output
            
            ### Providers
            - **ollama:** Local inference (recommended)
            - **mistral:** Mistral AI API (requires MISTRAL_API_KEY)
            - **openai:** OpenAI API (requires OPENAI_API_KEY)
            - **gemini:** Google Gemini API (requires GEMINI_API_KEY)
            
            ## Troubleshooting
            
            ### Ollama Connection Error
            ```bash
            # Check if Ollama is running
            curl http://localhost:11434/api/tags
            
            # Restart Ollama
            ollama serve
            ```
            
            ### Model Not Found
            ```bash
            # List available models
            ollama list
            
            # Pull required model
            ollama pull granite3.1:8b
            ```
            
            ### Out of Memory
            - Enable chunking
            - Use smaller model
            - Process fewer documents at once
            
            ## Documentation
            
            For detailed documentation, see the `./Docs` directory or visit:
            https://docling-project.github.io/docling-graph/
            """)

if __name__ == "__main__":
    console.print(
        Panel.fit(
            "[bold blue]Docling-Graph Showcase[/bold blue]\n"
            "[dim]Starting Gradio application...[/dim]",
            border_style="blue",
        )
    )
    
    # Try to find an available port starting from 7861
    import socket
    
    def find_free_port(start_port=7861, max_attempts=10):
        """Find a free port starting from start_port."""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    return port
            except OSError:
                continue
        return start_port  # Fallback to original port
    
    port = find_free_port()
    console.print(f"[green]Starting on port {port}[/green]")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True
    )

# Made with Bob
