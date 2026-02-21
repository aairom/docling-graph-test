# Architecture Documentation

## System Overview

The Docling-Graph Showcase Application is a web-based interface for processing documents using the docling-graph library with local LLM inference via Ollama.

```mermaid
graph TB
    subgraph "User Interface"
        UI[Gradio Web UI]
    end
    
    subgraph "Application Layer"
        APP[app.py]
        TEMPLATE[Template Engine]
        PROCESSOR[Document Processor]
    end
    
    subgraph "Docling-Graph Pipeline"
        PIPELINE[Pipeline Config]
        CONVERTER[Document Converter]
        EXTRACTOR[LLM/VLM Extractor]
        GRAPH[Graph Builder]
    end
    
    subgraph "LLM Backend"
        OLLAMA[Ollama Service]
        GRANITE[Granite 3.1 Model]
    end
    
    subgraph "Storage"
        INPUT[(Input Files)]
        OUTPUT[(Output Files)]
        LOGS[(Logs)]
    end
    
    UI --> APP
    APP --> TEMPLATE
    APP --> PROCESSOR
    PROCESSOR --> PIPELINE
    PIPELINE --> CONVERTER
    CONVERTER --> EXTRACTOR
    EXTRACTOR --> OLLAMA
    OLLAMA --> GRANITE
    EXTRACTOR --> GRAPH
    GRAPH --> OUTPUT
    INPUT --> CONVERTER
    APP --> LOGS
```

## Component Architecture

### 1. User Interface Layer

**Technology:** Gradio 4.x

**Components:**
- Individual Processing Tab
- Batch Processing Tab
- Help & Documentation Tab

**Features:**
- File selection from input directory
- Configuration options (backend, mode, chunking)
- Real-time progress tracking
- Result visualization

### 2. Application Layer

**Main Components:**

```mermaid
classDiagram
    class Application {
        +process_document()
        +batch_process_documents()
        +list_input_files()
        +get_timestamp()
    }
    
    class DocumentProcessor {
        +configure_pipeline()
        +run_extraction()
        +save_results()
    }
    
    class TemplateManager {
        +load_template()
        +validate_schema()
    }
    
    class OutputManager {
        +create_output_dir()
        +save_markdown()
        +save_csv()
        +save_html()
    }
    
    Application --> DocumentProcessor
    Application --> TemplateManager
    Application --> OutputManager
```

### 3. Docling-Graph Pipeline

**Pipeline Stages:**

```mermaid
flowchart LR
    A[Input Document] --> B[Document Conversion]
    B --> C{Chunking?}
    C -->|Yes| D[Split into Chunks]
    C -->|No| E[Full Document]
    D --> F[LLM Extraction]
    E --> F
    F --> G[Schema Validation]
    G --> H[Graph Construction]
    H --> I[Export Formats]
    I --> J[Output Files]
```

**Processing Modes:**

```mermaid
graph TB
    subgraph "One-to-One Mode"
        O1[Page 1] --> E1[Extract 1]
        O2[Page 2] --> E2[Extract 2]
        O3[Page 3] --> E3[Extract 3]
        E1 --> G1[Graph 1]
        E2 --> G2[Graph 2]
        E3 --> G3[Graph 3]
    end
    
    subgraph "Many-to-One Mode"
        M1[Page 1] --> C[Consolidate]
        M2[Page 2] --> C
        M3[Page 3] --> C
        C --> E[Extract]
        E --> G[Single Graph]
    end
```

### 4. LLM Backend

**Ollama Integration:**

```mermaid
sequenceDiagram
    participant App
    participant Pipeline
    participant LiteLLM
    participant Ollama
    participant Granite
    
    App->>Pipeline: Configure with Ollama
    Pipeline->>LiteLLM: Initialize client
    LiteLLM->>Ollama: Connect to service
    Ollama->>Granite: Load model
    
    loop For each chunk
        Pipeline->>LiteLLM: Extract data
        LiteLLM->>Ollama: Send prompt
        Ollama->>Granite: Process
        Granite->>Ollama: Return result
        Ollama->>LiteLLM: JSON response
        LiteLLM->>Pipeline: Structured data
    end
    
    Pipeline->>App: Complete graph
```

## Data Flow

### Individual Processing Flow

```mermaid
flowchart TD
    A[User selects file] --> B[Configure options]
    B --> C[Click Process]
    C --> D[Create timestamped output dir]
    D --> E[Load template]
    E --> F[Configure pipeline]
    F --> G{Backend type?}
    
    G -->|LLM| H[Text extraction]
    G -->|VLM| I[Vision extraction]
    
    H --> J[Send to Ollama]
    I --> J
    
    J --> K[Receive structured data]
    K --> L[Build knowledge graph]
    L --> M[Generate outputs]
    
    M --> N[Save summary.md]
    M --> O[Save graph.html]
    M --> P[Save nodes.csv]
    M --> Q[Save edges.csv]
    
    N --> R[Display results]
    O --> R
    P --> R
    Q --> R
```

### Batch Processing Flow

```mermaid
flowchart TD
    A[User clicks Batch Process] --> B[List all input files]
    B --> C{Files found?}
    C -->|No| D[Show error]
    C -->|Yes| E[Initialize batch]
    
    E --> F[For each file]
    F --> G[Process document]
    G --> H[Save results]
    H --> I{More files?}
    
    I -->|Yes| F
    I -->|No| J[Generate batch summary]
    J --> K[Display results]
```

## Deployment Architecture

### Local Deployment

```mermaid
graph TB
    subgraph "Local Machine"
        subgraph "Application"
            APP[Gradio App :7860]
        end
        
        subgraph "LLM Service"
            OLLAMA[Ollama :11434]
            MODEL[Granite Model]
        end
        
        subgraph "File System"
            INPUT[./input/]
            OUTPUT[./output/]
            LOGS[./logs/]
        end
        
        APP --> OLLAMA
        OLLAMA --> MODEL
        INPUT --> APP
        APP --> OUTPUT
        APP --> LOGS
    end
    
    USER[User Browser] --> APP
```

### Docker Deployment

```mermaid
graph TB
    subgraph "Docker Host"
        subgraph "App Container"
            APP[Gradio App :7860]
            VENV[Python Env]
        end
        
        subgraph "Volumes"
            INPUT[input-volume]
            OUTPUT[output-volume]
            LOGS[logs-volume]
        end
        
        APP --> INPUT
        APP --> OUTPUT
        APP --> LOGS
    end
    
    OLLAMA_EXT[External Ollama] --> APP
    USER[User Browser] --> APP
```

### Kubernetes Deployment

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Ingress"
            LB[LoadBalancer]
        end
        
        subgraph "Services"
            SVC[docling-graph-service :80]
        end
        
        subgraph "Deployments"
            POD1[App Pod 1]
            POD2[App Pod 2]
        end
        
        subgraph "Storage"
            PVC1[Input PVC 10Gi]
            PVC2[Output PVC 20Gi]
        end
        
        subgraph "Config"
            CM[ConfigMap]
            SECRET[Secrets]
        end
        
        LB --> SVC
        SVC --> POD1
        SVC --> POD2
        POD1 --> PVC1
        POD1 --> PVC2
        POD2 --> PVC1
        POD2 --> PVC2
        CM --> POD1
        CM --> POD2
        SECRET --> POD1
        SECRET --> POD2
    end
    
    USER[Users] --> LB
    OLLAMA_SVC[Ollama Service] --> POD1
    OLLAMA_SVC --> POD2
```

## Security Architecture

```mermaid
flowchart TD
    A[User Request] --> B{Authentication}
    B -->|Pass| C[Authorization Check]
    B -->|Fail| D[Reject]
    
    C --> E{File Access}
    E -->|Allowed| F[Process Request]
    E -->|Denied| D
    
    F --> G{API Keys}
    G -->|From Secret| H[Secure Access]
    G -->|From Env| I[Environment Vars]
    
    H --> J[LLM Service]
    I --> J
    
    J --> K[Return Results]
    K --> L[Sanitize Output]
    L --> M[Return to User]
```

## Scalability Considerations

### Horizontal Scaling

```mermaid
graph LR
    subgraph "Load Balancer"
        LB[Ingress]
    end
    
    subgraph "Application Tier"
        APP1[Pod 1]
        APP2[Pod 2]
        APP3[Pod 3]
    end
    
    subgraph "Shared Storage"
        PVC[Persistent Volumes]
    end
    
    subgraph "LLM Backend"
        OLLAMA[Ollama Service]
    end
    
    LB --> APP1
    LB --> APP2
    LB --> APP3
    
    APP1 --> PVC
    APP2 --> PVC
    APP3 --> PVC
    
    APP1 --> OLLAMA
    APP2 --> OLLAMA
    APP3 --> OLLAMA
```

### Performance Optimization

1. **Caching Strategy**
   - Template caching
   - Model response caching
   - File metadata caching

2. **Async Processing**
   - Background job queue
   - Parallel chunk processing
   - Async file I/O

3. **Resource Management**
   - Connection pooling
   - Memory limits
   - CPU throttling

## Monitoring & Observability

```mermaid
graph TB
    subgraph "Application"
        APP[Gradio App]
    end
    
    subgraph "Metrics"
        PROM[Prometheus]
        GRAF[Grafana]
    end
    
    subgraph "Logging"
        LOGS[Application Logs]
        FLUENTD[Fluentd]
        ELK[ELK Stack]
    end
    
    subgraph "Tracing"
        JAEGER[Jaeger]
    end
    
    APP --> PROM
    PROM --> GRAF
    APP --> LOGS
    LOGS --> FLUENTD
    FLUENTD --> ELK
    APP --> JAEGER
```

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Gradio | 4.x | Web UI |
| Backend | Python | 3.11 | Application logic |
| Framework | docling-graph | latest | Document processing |
| LLM | Ollama | latest | Local inference |
| Model | Granite 3.1 | 8B | Language model |
| Container | Docker | latest | Containerization |
| Orchestration | Kubernetes | 1.28+ | Container orchestration |
| Storage | PVC | - | Persistent storage |

## Design Patterns

### 1. Pipeline Pattern
- Sequential processing stages
- Each stage transforms data
- Error handling at each stage

### 2. Factory Pattern
- Template creation
- Pipeline configuration
- Output format generation

### 3. Strategy Pattern
- Backend selection (LLM/VLM)
- Processing mode selection
- Export format selection

### 4. Observer Pattern
- Progress tracking
- Status updates
- Event logging

## Future Enhancements

1. **Multi-tenancy Support**
   - User authentication
   - Workspace isolation
   - Resource quotas

2. **Advanced Features**
   - Custom template builder UI
   - Real-time collaboration
   - Version control for templates

3. **Integration**
   - REST API
   - Webhook support
   - External storage (S3, GCS)

4. **Performance**
   - GPU acceleration
   - Distributed processing
   - Advanced caching