# API Reference

## Overview

This document provides detailed API reference for the Docling-Graph Showcase Application.

## Core Functions

### process_document()

Process a single document using docling-graph.

```python
def process_document(
    file_path: str,
    backend: str,
    processing_mode: str,
    use_chunking: bool,
    provider: str,
    model: str,
    progress=gr.Progress()
) -> Tuple[str, str, str, str]
```

**Parameters:**

- `file_path` (str): Path to the document relative to input directory
- `backend` (str): Extraction backend - "llm" or "vlm"
- `processing_mode` (str): Processing mode - "one-to-one" or "many-to-one"
- `use_chunking` (bool): Whether to enable document chunking
- `provider` (str): LLM provider - "ollama", "mistral", "openai", "gemini"
- `model` (str): Model identifier (e.g., "granite3.1:8b")
- `progress` (gr.Progress): Gradio progress tracker

**Returns:**

Tuple of (status_message, graph_html_path, nodes_csv_path, edges_csv_path)

**Example:**

```python
status, graph, nodes, edges = process_document(
    file_path="document.pdf",
    backend="llm",
    processing_mode="many-to-one",
    use_chunking=True,
    provider="ollama",
    model="granite3.1:8b"
)
```

### batch_process_documents()

Process all documents in the input directory.

```python
def batch_process_documents(
    backend: str,
    processing_mode: str,
    use_chunking: bool,
    provider: str,
    model: str,
    progress=gr.Progress()
) -> str
```

**Parameters:**

Same as `process_document()` except `file_path` (processes all files)

**Returns:**

String containing batch processing summary

**Example:**

```python
summary = batch_process_documents(
    backend="llm",
    processing_mode="many-to-one",
    use_chunking=True,
    provider="ollama",
    model="granite3.1:8b"
)
```

### list_input_files()

List all files in the input directory.

```python
def list_input_files() -> List[str]
```

**Returns:**

List of filenames in the input directory

**Example:**

```python
files = list_input_files()
# ['document1.pdf', 'document2.pdf', 'image.png']
```

### get_timestamp()

Generate timestamp for output files.

```python
def get_timestamp() -> str
```

**Returns:**

Timestamp string in format "YYYYMMDD_HHMMSS"

**Example:**

```python
timestamp = get_timestamp()
# '20260221_153045'
```

## Configuration Classes

### PipelineConfig

Configuration for docling-graph pipeline.

```python
from docling_graph import PipelineConfig

config = PipelineConfig(
    source: str,                    # Path to source document
    template: Type[BaseModel],      # Pydantic template class
    backend: str = "llm",           # "llm" or "vlm"
    inference: str = "remote",      # "remote" or "local"
    processing_mode: str = "many-to-one",  # Processing mode
    use_chunking: bool = True,      # Enable chunking
    provider_override: str = None,  # LLM provider
    model_override: str = None,     # Model name
    api_base: str = None,           # API base URL
    output_dir: str = None          # Output directory
)
```

**Example:**

```python
config = PipelineConfig(
    source="document.pdf",
    template=SimpleDocument,
    backend="llm",
    provider_override="ollama",
    model_override="granite3.1:8b",
    api_base="http://localhost:11434"
)
```

## Template Classes

### BaseModel

Base class for all templates (from Pydantic).

```python
from pydantic import BaseModel, Field

class YourTemplate(BaseModel):
    """Your template description."""
    model_config = {
        'is_entity': True,
        'graph_id_fields': ['field_name']
    }
    
    field_name: str = Field(description="Field description")
```

### edge()

Helper function to define graph relationships.

```python
def edge(label: str, **kwargs) -> Field
```

**Parameters:**

- `label` (str): Edge label/relationship type
- `**kwargs`: Additional Field parameters

**Returns:**

Pydantic Field with edge metadata

**Example:**

```python
from typing import List

class Document(BaseModel):
    authors: List[Person] = edge(
        "AUTHORED_BY",
        description="Document authors"
    )
```

## Pipeline Context

### PipelineContext

Result object from pipeline execution.

```python
from docling_graph import run_pipeline

context = run_pipeline(config)

# Access results
graph = context.knowledge_graph      # NetworkX graph
models = context.extracted_models    # List of Pydantic models
metadata = context.graph_metadata    # Processing metadata
```

**Attributes:**

- `knowledge_graph` (nx.DiGraph): NetworkX directed graph
- `extracted_models` (List[BaseModel]): Extracted Pydantic models
- `graph_metadata` (dict): Processing metadata

**Methods:**

```python
# Get node count
node_count = context.knowledge_graph.number_of_nodes()

# Get edge count
edge_count = context.knowledge_graph.number_of_edges()

# Iterate nodes
for node_id, node_data in context.knowledge_graph.nodes(data=True):
    print(f"Node: {node_id}, Data: {node_data}")

# Iterate edges
for source, target, edge_data in context.knowledge_graph.edges(data=True):
    print(f"Edge: {source} -> {target}, Data: {edge_data}")
```

## Environment Variables

### Application Settings

```bash
# Gradio server configuration
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
PYTHONUNBUFFERED=1

# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.1:8b

# API keys (optional)
MISTRAL_API_KEY=your_key
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

## Error Handling

### Common Exceptions

```python
try:
    context = run_pipeline(config)
except FileNotFoundError:
    # Source file not found
    print("Document not found")
except ValueError:
    # Invalid configuration
    print("Invalid config")
except Exception as e:
    # Other errors
    print(f"Error: {e}")
```

## Gradio Components

### File Dropdown

```python
file_dropdown = gr.Dropdown(
    choices=list_input_files(),
    label="Select Document",
    info="Files from ./input directory"
)
```

### Radio Buttons

```python
backend_radio = gr.Radio(
    choices=["llm", "vlm"],
    value="llm",
    label="Extraction Backend"
)
```

### Checkbox

```python
chunking_check = gr.Checkbox(
    value=True,
    label="Use Chunking"
)
```

### Button

```python
process_btn = gr.Button(
    "🚀 Process Document",
    variant="primary"
)
```

### Markdown Output

```python
status_output = gr.Markdown(label="Status")
```

### File Output

```python
graph_file = gr.File(label="Graph HTML")
```

## Utility Functions

### File Operations

```python
from pathlib import Path

# Create directory
output_dir = Path("output/run_20260221_153045")
output_dir.mkdir(exist_ok=True, parents=True)

# List files
files = list(Path("input").glob("*.pdf"))

# Read file
with open("input/document.pdf", "rb") as f:
    content = f.read()

# Write file
with open("output/result.txt", "w") as f:
    f.write("Result")
```

### JSON Operations

```python
import json

# Save JSON
data = {"key": "value"}
with open("output/data.json", "w") as f:
    json.dump(data, f, indent=2)

# Load JSON
with open("output/data.json", "r") as f:
    data = json.load(f)
```

### CSV Operations

```python
import csv

# Write CSV
with open("output/nodes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "label", "type"])
    writer.writerow(["1", "Node 1", "Entity"])

# Read CSV
with open("output/nodes.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

## Graph Operations

### NetworkX Graph

```python
import networkx as nx

# Create graph
G = nx.DiGraph()

# Add nodes
G.add_node("node1", label="Node 1", type="Entity")
G.add_node("node2", label="Node 2", type="Entity")

# Add edges
G.add_edge("node1", "node2", label="RELATES_TO")

# Query graph
nodes = G.number_of_nodes()
edges = G.number_of_edges()
neighbors = list(G.neighbors("node1"))

# Export
nx.write_gexf(G, "output/graph.gexf")
```

## Logging

### Setup Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use logger
logger.info("Processing document")
logger.error("Error occurred", exc_info=True)
```

## Testing

### Unit Tests

```python
import unittest
from app import process_document, list_input_files

class TestApp(unittest.TestCase):
    def test_list_files(self):
        files = list_input_files()
        self.assertIsInstance(files, list)
    
    def test_process_document(self):
        # Add test implementation
        pass

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
def test_full_pipeline():
    """Test complete processing pipeline."""
    config = PipelineConfig(
        source="test_document.pdf",
        template=SimpleDocument,
        backend="llm"
    )
    
    context = run_pipeline(config)
    
    assert context.knowledge_graph.number_of_nodes() > 0
    assert context.knowledge_graph.number_of_edges() >= 0
    assert len(context.extracted_models) > 0
```

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def load_template(template_name: str):
    """Cache template loading."""
    # Load and return template
    pass
```

### Async Processing

```python
import asyncio

async def process_async(file_path: str):
    """Async document processing."""
    # Async implementation
    pass

# Run async
asyncio.run(process_async("document.pdf"))
```

## Security

### Input Validation

```python
from pathlib import Path

def validate_file_path(file_path: str) -> bool:
    """Validate file path is within input directory."""
    input_dir = Path("input").resolve()
    file_full_path = (input_dir / file_path).resolve()
    
    return file_full_path.is_relative_to(input_dir)
```

### Sanitize Output

```python
import html

def sanitize_output(text: str) -> str:
    """Sanitize text for display."""
    return html.escape(text)
```

## Best Practices

1. **Error Handling** - Always wrap operations in try-except
2. **Logging** - Log important events and errors
3. **Validation** - Validate inputs before processing
4. **Resource Cleanup** - Close files and connections
5. **Type Hints** - Use type hints for clarity
6. **Documentation** - Document functions and classes
7. **Testing** - Write tests for critical functions

## Resources

- [Docling-Graph API](https://docling-project.github.io/docling-graph/reference/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Gradio Documentation](https://gradio.app/docs/)
- [NetworkX Documentation](https://networkx.org/documentation/)