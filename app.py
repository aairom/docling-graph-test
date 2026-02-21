"""
Docling-Graph Showcase Application
A Gradio-based UI for document processing using docling-graph with Ollama/Granite4
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import json
import traceback
import requests

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


def get_ollama_models() -> List[str]:
    """Fetch available Ollama models from the local Ollama instance."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            return sorted(models) if models else [OLLAMA_MODEL]
        else:
            console.print(f"[yellow]Warning: Could not fetch Ollama models (status {response.status_code})[/yellow]")
            return [OLLAMA_MODEL]
    except requests.exceptions.RequestException as e:
        console.print(f"[yellow]Warning: Ollama not available - {str(e)}[/yellow]")
        return [OLLAMA_MODEL]


def check_ollama_status() -> Tuple[bool, str]:
    """Check if Ollama is running and return status."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models = get_ollama_models()
            return True, f"🟢 Ollama Running ({len(models)} models available)"
        return False, "🟡 Ollama responding but no models found"
    except requests.exceptions.RequestException:
        return False, "🔴 Ollama Not Running"


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
) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
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
        File paths may be None if files weren't generated
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
            return f"Error: File not found: {file_path}", None, None, None
        
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
        
        progress(0.85, desc="💾 Exporting results...")
        console.print("  • Exporting to CSV and HTML")
        
        # Get results
        graph = context.knowledge_graph
        models = context.extracted_models
        
        # Export results manually
        from docling_graph.core import CSVExporter, JSONExporter, InteractiveVisualizer
        from pathlib import Path
        
        # Export nodes and edges as CSV
        csv_exporter = CSVExporter()
        csv_output_path = output_subdir / f"graph_{timestamp}"
        csv_exporter.export(graph=graph, output_path=csv_output_path)
        
        # Export as JSON
        json_exporter = JSONExporter()
        json_output_path = output_subdir / f"graph_{timestamp}.json"
        json_exporter.export(graph=graph, output_path=json_output_path)
        
        # Generate HTML visualization
        visualizer = InteractiveVisualizer()
        html_output_path = output_subdir / f"graph_{timestamp}.html"
        visualizer.save_cytoscape_graph(graph=graph, output_path=html_output_path)
        
        progress(0.95, desc="💾 Generating outputs...")
        console.print("  • Saving results")
        
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
        
        # Find generated files (CSV files are in subdirectory)
        graph_html = list(output_subdir.glob("*.html"))
        nodes_csv = list(output_subdir.glob("**/nodes.csv"))
        edges_csv = list(output_subdir.glob("**/edges.csv"))
        
        # Return None instead of empty string if files don't exist (Gradio handles None properly)
        graph_html_path = str(graph_html[0]) if graph_html else None
        nodes_csv_path = str(nodes_csv[0]) if nodes_csv else None
        edges_csv_path = str(edges_csv[0]) if edges_csv else None
        
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
- For large documents, processing may take 30-60 minutes
- Check logs: `tail -f logs/docling-graph-app.log`
"""
        return error_msg, None, None, None


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
    # Check Ollama status at startup
    ollama_running, ollama_status = check_ollama_status()
    available_models = get_ollama_models() if ollama_running else [OLLAMA_MODEL]
    
    gr.Markdown(f"""
    # 🔍 Docling-Graph Showcase
    
    Transform documents into validated knowledge graphs using docling-graph with local or remote LLMs.
    
    **Status:** {ollama_status}
    
    **Features:**
    - 📄 Individual or batch document processing
    - 🧠 Local LLM inference with Ollama or remote providers
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
                    
                    # Dynamic model selection based on provider
                    model_dropdown = gr.Dropdown(
                        choices=available_models,
                        value=available_models[0] if available_models else OLLAMA_MODEL,
                        label="Ollama Model",
                        info="Select from available Ollama models",
                        visible=True,
                        allow_custom_value=True
                    )
                    
                    model_text = gr.Textbox(
                        value="",
                        label="Model Name (for non-Ollama providers)",
                        info="e.g., gpt-4, mistral-large, gemini-pro",
                        visible=False
                    )
                    
                    refresh_models_btn = gr.Button("🔄 Refresh Ollama Models", size="sm")
                    
                    # API Key fields for remote providers
                    with gr.Accordion("🔑 API Configuration (for remote providers)", open=False):
                        api_key_text = gr.Textbox(
                            value="",
                            label="API Key",
                            type="password",
                            info="Required for OpenAI, Mistral, or Gemini",
                            visible=False
                        )
                        api_base_text = gr.Textbox(
                            value="",
                            label="API Base URL (optional)",
                            info="Custom API endpoint if needed",
                            visible=False
                        )
                    
                    process_btn = gr.Button("🚀 Process Document", variant="primary")
                
                with gr.Column(scale=2):
                    status_output = gr.Markdown(label="Status")
                    
                    with gr.Accordion("📊 Outputs", open=False):
                        graph_file = gr.File(label="Graph HTML")
                        nodes_file = gr.File(label="Nodes CSV")
                        edges_file = gr.File(label="Edges CSV")
            
            # Function to handle provider change
            def update_model_inputs(provider):
                """Update model input fields based on selected provider."""
                if provider == "ollama":
                    models = get_ollama_models()
                    return (
                        gr.Dropdown(visible=True, choices=models, value=models[0] if models else OLLAMA_MODEL),
                        gr.Textbox(visible=False),
                        gr.Textbox(visible=False),
                        gr.Textbox(visible=False)
                    )
                else:
                    # For remote providers, show text input and API key
                    default_models = {
                        "openai": "gpt-4",
                        "mistral": "mistral-large-latest",
                        "gemini": "gemini-pro"
                    }
                    return (
                        gr.Dropdown(visible=False),
                        gr.Textbox(visible=True, value=default_models.get(provider, "")),
                        gr.Textbox(visible=True),
                        gr.Textbox(visible=True)
                    )
            
            def refresh_ollama_models():
                """Refresh the list of available Ollama models."""
                models = get_ollama_models()
                return gr.Dropdown(choices=models, value=models[0] if models else OLLAMA_MODEL)
            
            def get_model_value(provider, model_dropdown_value, model_text_value):
                """Get the appropriate model value based on provider."""
                return model_dropdown_value if provider == "ollama" else model_text_value
            
            # Wire up individual processing
            refresh_btn.click(
                fn=lambda: gr.Dropdown(choices=list_input_files()),
                outputs=file_dropdown
            )
            
            provider_dropdown.change(
                fn=update_model_inputs,
                inputs=[provider_dropdown],
                outputs=[model_dropdown, model_text, api_key_text, api_base_text]
            )
            
            refresh_models_btn.click(
                fn=refresh_ollama_models,
                outputs=model_dropdown
            )
            
            # Modified process function to handle both model inputs
            def process_with_model_selection(file_path, backend, mode, chunking, provider,
                                            model_dropdown_val, model_text_val, progress=gr.Progress()):
                model = model_dropdown_val if provider == "ollama" else model_text_val
                return process_document(file_path, backend, mode, chunking, provider, model, progress)
            
            process_btn.click(
                fn=process_with_model_selection,
                inputs=[
                    file_dropdown,
                    backend_radio,
                    mode_radio,
                    chunking_check,
                    provider_dropdown,
                    model_dropdown,
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
                    
                    # Dynamic model selection for batch processing
                    batch_model_dropdown = gr.Dropdown(
                        choices=available_models,
                        value=available_models[0] if available_models else OLLAMA_MODEL,
                        label="Ollama Model",
                        info="Select from available Ollama models",
                        visible=True,
                        allow_custom_value=True
                    )
                    
                    batch_model_text = gr.Textbox(
                        value="",
                        label="Model Name (for non-Ollama providers)",
                        info="e.g., gpt-4, mistral-large, gemini-pro",
                        visible=False
                    )
                    
                    batch_refresh_models_btn = gr.Button("🔄 Refresh Ollama Models", size="sm")
                    
                    with gr.Accordion("🔑 API Configuration (for remote providers)", open=False):
                        batch_api_key_text = gr.Textbox(
                            value="",
                            label="API Key",
                            type="password",
                            info="Required for OpenAI, Mistral, or Gemini",
                            visible=False
                        )
                    
                    batch_btn = gr.Button("🚀 Process All Documents", variant="primary")
                
                with gr.Column(scale=2):
                    batch_status = gr.Markdown(label="Batch Status")
            
            # Wire up batch processing provider change
            batch_provider.change(
                fn=update_model_inputs,
                inputs=[batch_provider],
                outputs=[batch_model_dropdown, batch_model_text, batch_api_key_text, gr.Textbox(visible=False)]
            )
            
            batch_refresh_models_btn.click(
                fn=refresh_ollama_models,
                outputs=batch_model_dropdown
            )
            
            # Modified batch process function
            def batch_process_with_model_selection(backend, mode, chunking, provider,
                                                   model_dropdown_val, model_text_val, progress=gr.Progress()):
                model = model_dropdown_val if provider == "ollama" else model_text_val
                return batch_process_documents(backend, mode, chunking, provider, model, progress)
            
            # Wire up batch processing
            batch_btn.click(
                fn=batch_process_with_model_selection,
                inputs=[
                    batch_backend,
                    batch_mode,
                    batch_chunking,
                    batch_provider,
                    batch_model_dropdown,
                    batch_model_text
                ],
                outputs=batch_status
            )
        
        # Help Tab
        with gr.Tab("ℹ️ Help"):
            gr.Markdown("""
            ## Getting Started
            
            ### 1. Setup Ollama (for local inference)
            ```bash
            # Install Ollama
            curl -fsSL https://ollama.com/install.sh | sh
            
            # Start Ollama service
            ollama serve
            
            # Pull a model (examples)
            ollama pull granite4
            ollama pull llama3
            ollama pull mistral
            ```
            
            ### 2. Add Documents
            Place your documents (PDF, images, markdown, etc.) in the `./input` directory.
            
            ### 3. Select Provider & Model
            - **Ollama (Local):** Select from your installed models using the dropdown
            - **Remote Providers:** Choose OpenAI, Mistral, or Gemini and enter your API key
            
            ### 4. Process Documents
            - **Individual:** Select a file and click "Process Document"
            - **Batch:** Click "Process All Documents" to process everything
            
            ### 5. View Results
            Results are saved in `./output` with timestamps:
            - `report_TIMESTAMP.md` - Processing summary
            - `graph_TIMESTAMP.html` - Interactive visualization
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
            
            #### Ollama (Local - Recommended)
            - **Advantages:** Privacy, no API costs, works offline
            - **Models:** Any model you've pulled (granite4, llama3, mistral, etc.)
            - **Setup:** Just install Ollama and pull models
            - **Refresh:** Click "🔄 Refresh Ollama Models" to update the list
            
            #### Remote Providers
            - **OpenAI:** GPT-4, GPT-3.5-turbo (requires API key)
            - **Mistral:** mistral-large-latest, mistral-medium (requires API key)
            - **Gemini:** gemini-pro (requires API key)
            
            ## Troubleshooting
            
            ### Ollama Connection Error
            ```bash
            # Check if Ollama is running
            curl http://localhost:11434/api/tags
            
            # Restart Ollama
            ollama serve
            ```
            
            ### No Models Available
            ```bash
            # List available models
            ollama list
            
            # Pull a model
            ollama pull granite4
            ollama pull llama3
            
            # Refresh the model list in the UI
            # Click "🔄 Refresh Ollama Models" button
            ```
            
            ### Remote Provider Errors
            - Verify your API key is correct
            - Check your API quota/credits
            - Ensure you have network connectivity
            
            ### Out of Memory
            - Enable chunking (recommended for large documents)
            - Use a smaller model
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
