# Template Guide for Docling-Graph

## Overview

Templates in Docling-Graph are Pydantic models that define the structure of data to extract from documents. They specify entities (nodes), relationships (edges), and validation rules to create structured knowledge graphs from unstructured documents.

## Available Templates

### 1. Billing Document Template (`billing_document.py`)
**Use Case:** Invoices, receipts, credit notes, debit notes

**Extracts:**
- Document metadata (number, type, dates, currency)
- Parties (seller, buyer with full contact details)
- Line items with products/services
- Tax breakdowns
- Payment information
- Delivery details
- Document references

**Best For:**
- Financial documents
- Purchase orders
- Sales invoices
- Tax documents

### 2. Rheology Research Template (`rheology_research.py`)
**Use Case:** Scientific research papers on rheology and material science

**Extracts:**
- Paper metadata (title, authors, institutions)
- Research studies and experiments
- Slurry formulations and components
- Preparation procedures
- Rheometer setups and protocols
- Test results and measurements
- Derived quantities and model fits

**Best For:**
- Academic papers
- Technical reports
- Laboratory documentation
- Material science research

### 3. ID Card Template (`id_card.py`)
**Use Case:** Identity documents and personal identification

**Extracts:**
- Personal information (names, dates)
- Document details (number, type, issuer)
- Address information
- Physical characteristics
- Validity periods

**Best For:**
- Identity cards
- Passports
- Driver's licenses
- Personal documents

### 4. CGV MRH Template (`cgv_mrh_staged.py`)
**Use Case:** French insurance contracts (Conditions Générales de Vente - Multirisque Habitation)

**Extracts:**
- Contract details
- Coverage information
- Premium amounts
- Terms and conditions
- Insured parties and properties

**Best For:**
- Insurance documents
- French legal contracts
- Policy documents

### 5. Simple Document Template (`_samples/simple_template.py`)
**Use Case:** General-purpose document extraction

**Extracts:**
- Document metadata (title, date, authors)
- People and organizations
- Sections and topics
- Keywords

**Best For:**
- General documents
- Reports
- Articles
- When no specific template matches

## Template Structure

### Basic Components

#### 1. Entity Classes
Entities are nodes in the knowledge graph. They must have:
- `model_config` with `graph_id_fields` for unique identification
- Field definitions with descriptions
- Optional validators

```python
class Person(BaseModel):
    """Person entity with stable ID."""
    model_config = {
        'is_entity': True,
        'graph_id_fields': ['name']
    }
    
    name: str = Field(description="Person's full name")
    role: Optional[str] = Field(default=None, description="Person's role")
```

#### 2. Component Classes
Components are embedded data without separate identity:
- `model_config` with `is_entity=False`
- Used for nested data structures

```python
class Address(BaseModel):
    """Address component (not a separate entity)."""
    model_config = ConfigDict(is_entity=False)
    
    street: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City")
```

#### 3. Edge Relationships
Use the `edge()` helper to define relationships:

```python
def edge(label: str, **kwargs):
    """Helper function to define graph edges."""
    return Field(..., json_schema_extra={"edge_label": label}, **kwargs)

class Document(BaseModel):
    authors: List[Person] = edge(
        "AUTHORED_BY",
        default_factory=list,
        description="Document authors"
    )
```

## Creating Custom Templates

### Step 1: Create Template File

Create a new Python file in the `templates/` directory:

```bash
touch templates/my_custom_template.py
```

### Step 2: Define Helper Function

```python
from typing import Any
from pydantic import Field

def edge(label: str, **kwargs: Any) -> Any:
    """Create a Pydantic Field with edge metadata."""
    if "default" not in kwargs and "default_factory" not in kwargs:
        kwargs["default"] = ...
    return Field(json_schema_extra={"edge_label": label}, **kwargs)
```

### Step 3: Define Entity Classes

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class Author(BaseModel):
    """Author entity."""
    model_config = ConfigDict(
        graph_id_fields=["name"],
        extra="ignore"
    )
    
    name: str = Field(
        description="Author's full name. LOOK FOR: Author section, byline"
    )
    affiliation: Optional[str] = Field(
        None,
        description="Author's institution or organization"
    )
```

### Step 4: Define Root Document Class

```python
class MyDocument(BaseModel):
    """
    Root document template for my custom extraction.
    
    This template extracts structured data from [document type].
    """
    model_config = ConfigDict(
        graph_id_fields=["title"],
        extra="ignore"
    )
    
    title: str = Field(
        description="Document title. LOOK FOR: Header, title section"
    )
    
    authors: List[Author] = edge(
        "AUTHORED_BY",
        default_factory=list,
        description="Document authors"
    )
    
    date: Optional[str] = Field(
        None,
        description="Publication date in YYYY-MM-DD format"
    )
```

### Step 5: Add Field Descriptions

Good field descriptions help the LLM extract accurate data:

```python
name: str = Field(
    description=(
        "WHAT: The person's full legal name. "
        "LOOK FOR: 'Name', 'Full Name', 'Nom' labels in header. "
        "EXTRACT: Complete name including middle names. "
        "EXAMPLES: 'John Michael Smith', 'Marie-Claire Dubois'"
    ),
    examples=["John Michael Smith", "Marie-Claire Dubois"]
)
```

### Step 6: Add Validators (Optional)

```python
from pydantic import field_validator

class MyDocument(BaseModel):
    # ... fields ...
    
    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v):
        """Parse various date formats to YYYY-MM-DD."""
        if not v:
            return v
        # Add date parsing logic
        return v
```

### Step 7: Test Your Template

1. Save the template file
2. Restart the application
3. Select your template from the dropdown
4. Process a test document
5. Review the extracted graph

## Best Practices

### 1. Field Descriptions
- Use clear, specific descriptions
- Include "LOOK FOR" hints for the LLM
- Provide examples
- Specify format requirements

### 2. Entity Identification
- Choose stable, unique fields for `graph_id_fields`
- Use multiple fields if needed: `['name', 'date_of_birth']`
- Avoid auto-generated IDs when possible

### 3. Relationships
- Use descriptive edge labels in UPPER_CASE
- Examples: `AUTHORED_BY`, `CONTAINS_LINE`, `ISSUED_BY`
- Make relationships semantic and clear

### 4. Validation
- Add validators for data normalization
- Parse dates, currencies, numbers consistently
- Handle missing or malformed data gracefully

### 5. Nested Structures
- Use components for embedded data
- Use entities for reusable, identifiable objects
- Keep nesting reasonable (2-3 levels max)

## Template Selection Guide

| Document Type | Recommended Template | Alternative |
|--------------|---------------------|-------------|
| Invoice/Receipt | `billing_document` | `simple_document` |
| Research Paper | `rheology_research` | `simple_document` |
| ID Card | `id_card` | `simple_document` |
| Insurance Contract | `cgv_mrh_staged` | `simple_document` |
| General Document | `simple_document` | Create custom |
| Technical Report | Create custom | `simple_document` |
| Legal Contract | Create custom | `simple_document` |

## Advanced Features

### Staged Extraction
For complex documents, use staged extraction:

```python
# First stage: Extract high-level structure
# Second stage: Extract detailed information
# Third stage: Extract relationships
```

### Enum Types
Use enums for controlled vocabularies:

```python
from enum import Enum

class DocumentType(str, Enum):
    INVOICE = "Invoice"
    RECEIPT = "Receipt"
    CREDIT_NOTE = "Credit Note"
```

### Custom Validators
Add complex validation logic:

```python
@field_validator("amount", mode="before")
@classmethod
def parse_amount(cls, v):
    """Parse amount from various formats."""
    if isinstance(v, str):
        # Remove currency symbols, parse number
        clean = re.sub(r'[^\d.,]', '', v)
        return float(clean.replace(',', '.'))
    return v
```

## Troubleshooting

### Template Not Appearing
- Check file is in `templates/` directory
- Ensure file ends with `.py`
- Verify root class has `graph_id_fields` in `model_config`
- Restart the application

### Extraction Errors
- Review field descriptions for clarity
- Check validators for errors
- Simplify complex nested structures
- Test with simpler documents first

### Poor Extraction Quality
- Improve field descriptions with examples
- Add more specific "LOOK FOR" hints
- Use appropriate backend (LLM vs VLM)
- Try different models
- Enable chunking for large documents

## Examples

See the `templates/` directory for complete working examples:
- `billing_document.py` - Complex financial document
- `rheology_research.py` - Scientific paper with nested data
- `id_card.py` - Simple identity document
- `cgv_mrh_staged.py` - Staged extraction for contracts

## Resources

- [Docling-Graph Documentation](https://ibm.github.io/docling-graph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Template Examples](../templates/)
- [Sample Templates](../_samples/)

## Support

For questions or issues:
1. Check this guide
2. Review example templates
3. Test with simple documents first
4. Check application logs
5. Consult Docling-Graph documentation