# 🏛️ Tamil Nadu Government Scheme — Hybrid Knowledge Graph RAG

A Retrieval-Augmented Generation (RAG) chatbot that helps users discover and understand **Tamil Nadu Government schemes** using a combination of:

* 🕸️ Knowledge Graph RAG
* 🔎 Vector Semantic Search
* 🔀 Hybrid Retrieval
* 🤖 Large Language Model (LLM)
* 🌐 Playwright web scraping
* 🗄️ Neo4j Aura
* 💬 Streamlit chatbot interface

The project collects scheme information from the Tamil Nadu Government website, structures the information into a Knowledge Graph, generates vector embeddings, performs hybrid retrieval, and generates grounded answers.

---

## 📌 Project Objective

The objective of this project is to build an intelligent chatbot that allows citizens to ask natural-language questions about Tamil Nadu Government schemes.

For example:

> What schemes are available for farmers in Coimbatore?

> What benefits are available for farmers?

> How can I apply for Training to Farmers?

Instead of relying only on keyword search, the application combines:

```text
Knowledge Graph Search
        +
Vector Semantic Search
        ↓
Hybrid Retrieval
        ↓
LLM
        ↓
Grounded Answer
```

---

# 🏗️ Architecture

```text
                    ┌─────────────────────────────┐
                    │ Tamil Nadu Government Site  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Playwright       │
                         │ Web Scraper      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Raw Scheme Data  │
                         │ JSON             │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Data Cleaning &  │
                         │ Normalization    │
                         └────────┬─────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │          Neo4j Aura            │
                  │                               │
                  │  Knowledge Graph + Vector DB │
                  └───────────────┬───────────────┘
                                  │
                   ┌──────────────┴──────────────┐
                   │                             │
                   ▼                             ▼
          ┌─────────────────┐          ┌──────────────────┐
          │ Knowledge Graph │          │ Vector Index     │
          │ Retrieval       │          │ Semantic Search  │
          └────────┬────────┘          └────────┬─────────┘
                   │                            │
                   └──────────────┬─────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Hybrid Retriever │
                         │ RRF Fusion       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ RAG Pipeline     │
                         │ + LLM            │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Streamlit        │
                         │ Chatbot          │
                         └──────────────────┘
```

---

# ✨ Key Features

## 1. Automated Web Scraping

Playwright is used to retrieve scheme information from the Tamil Nadu Government website.

The scraper:

* Opens the government scheme page
* Finds scheme detail links
* Visits individual scheme pages
* Extracts scheme information
* Saves the raw data as JSON

---

## 2. Data Cleaning

Raw web content is transformed into structured scheme records.

Important fields include:

```text
Department
Scheme Name
Description
Benefits
Beneficiaries
Eligibility
Income
Age
Community
Funding Pattern
Sponsored By
Scheme Type
Validity
Introduced On
How To Avail
Districts
Source URL
```

---

# 🕸️ 3. Knowledge Graph

Neo4j Aura is used to represent relationships between government schemes and their associated information.

The primary graph structure is:

```text
(:Department)-[:OFFERS]->(:Scheme)

(:Scheme)-[:AVAILABLE_IN]->(:District)

(:Scheme)-[:TARGETS]->(:Beneficiary)

(:Scheme)-[:HAS_BENEFIT]->(:Benefit)

(:Scheme)-[:SPONSORED_BY]->(:Sponsor)
```

Example:

```text
Agriculture - Farmers Welfare Department
                 │
                 │ OFFERS
                 ▼
        Training to Farmers
           │          │
           │          │
           ▼          ▼
       District    Beneficiary
       Coimbatore    Farmers
       Dindigul
       Erode
       ...
```

---

# 🔎 4. Vector Semantic Search

Each scheme is converted into an embedding using:

```text
text-embedding-3-small
```

The embedding is stored directly on the corresponding Neo4j `Scheme` node.

Example:

```text
(:Scheme {
    name: "Training to Farmers",
    embedding: [...]
})
```

The vector index allows the system to retrieve schemes based on semantic similarity rather than exact keyword matching.

---

# 🔀 5. Hybrid Retrieval

The application combines:

### Graph Retrieval

Useful for structured questions such as:

```text
Schemes in Coimbatore
Schemes for farmers
Benefits of a particular scheme
```

### Vector Retrieval

Useful for semantic questions such as:

```text
What financial assistance can farmers get?
```

The two result sets are combined using **Reciprocal Rank Fusion (RRF)**.

```text
Graph Results
      +
Vector Results
      ↓
RRF Fusion
      ↓
Top Relevant Schemes
```

---

# 🤖 6. RAG Answer Generation

The retrieved scheme information is passed to the LLM as context.

The LLM is instructed to:

* Use retrieved information only
* Avoid inventing scheme information
* Avoid hallucinating eligibility
* Avoid inventing benefits
* Provide application information when available
* Provide official source URLs

---

# 💬 7. Streamlit Chatbot

The Streamlit interface allows users to interact with the RAG system using natural language.

Example:

```text
┌─────────────────────────────────────────────┐
│ 🏛️ Tamil Nadu Government Scheme Assistant  │
├─────────────────────────────────────────────┤
│                                             │
│ User: What schemes are available for       │
│       farmers in Coimbatore?                │
│                                             │
│ Assistant:                                  │
│ Here are the relevant schemes...            │
│                                             │
│ Sources:                                    │
│ https://www.tn.gov.in/...                   │
│                                             │
├─────────────────────────────────────────────┤
│ Ask about Tamil Nadu Government schemes...  │
└─────────────────────────────────────────────┘
```

---

# 📊 Current Dataset

The current implementation successfully scraped and processed:

```text
Total Schemes:              54
District Relationships:     83
Embedding Model:            text-embedding-3-small
Embedding Dimensions:       1536
Database:                   Neo4j Aura
Vector Index:               scheme_embeddings
```

The current scheme dataset is primarily based on the:

```text
Agriculture - Farmers Welfare Department
```

---

# 🗂️ Project Structure

```text
TN_Scheme_KG_RAG/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── data/
│   │
│   ├── raw/
│   │   ├── html/
│   │   ├── screenshots/
│   │   └── raw_schemes.json
│   │
│   ├── processed/
│   │   ├── cleaned_schemes.json
│   │   └── normalized_schemes.json
│   │
│   └── documents/
│
├── src/
│   ├── __init__.py
│   │
│   ├── scraper.py
│   ├── scrape_scheme_details.py
│   ├── cleaner.py
│   ├── normalize_data.py
│   │
│   ├── neo4j_connection.py
│   ├── neo4j_loader.py
│   ├── graph_queries.py
│   ├── graph_retriever.py
│   │
│   ├── embeddings.py
│   ├── embedding_generator.py
│   ├── vector_store.py
│   ├── vector_search.py
│   │
│   ├── hybrid_retriever.py
│   ├── rag_pipeline.py
│   └── prompts.py
│
└── tests/
    ├── test_scraper.py
    ├── test_neo4j.py
    └── test_rag.py
```

---

# 🛠️ Technology Stack

| Technology        | Purpose                           |
| ----------------- | --------------------------------- |
| Python            | Application development           |
| Playwright        | Web scraping                      |
| Neo4j Aura        | Knowledge Graph + Vector Database |
| Cypher            | Graph querying                    |
| LangChain         | LLM/embedding integration         |
| OpenAI Embeddings | Semantic vector representation    |
| OpenAI LLM        | Answer generation                 |
| Streamlit         | Chatbot UI                        |
| python-dotenv     | Environment configuration         |

---

# ⚙️ Prerequisites

Install the following:

* Python 3.11+
* Neo4j Aura account
* OpenAI API access
* Git
* VS Code recommended

Verify Python:

```bash
python --version
```

Recommended:

```text
Python 3.11.x
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project:

```bash
cd TN_Scheme_KG_RAG
```

---

# 2. Create Virtual Environment

Windows:

```cmd
python -m venv venv
```

Activate:

```cmd
venv\Scripts\activate
```

You should see:

```text
(venv)
```

---

# 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

If `requirements.txt` has not yet been generated:

```cmd
pip install playwright
pip install neo4j python-dotenv
pip install langchain-openai
pip install openai
pip install streamlit
```

Install Playwright browser:

```cmd
playwright install chromium
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

```env
NEO4J_URI=neo4j+s://YOUR_INSTANCE.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=YOUR_NEO4J_PASSWORD

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_CHAT_MODEL=YOUR_CHAT_MODEL
```

Never commit `.env` to GitHub.

---

# 🔒 .gitignore

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc

data/raw/
data/processed/

.pytest_cache/
.streamlit/
```

If you want to keep processed JSON files in GitHub, remove:

```text
data/processed/
```

---

# 🌐 Step 1 — Scrape Scheme Links

Run:

```cmd
python src\scraper.py
```

This discovers the scheme detail pages and saves:

```text
data/raw/raw_schemes.json
```

---

# 🌐 Step 2 — Scrape Scheme Details

Run:

```cmd
python src\scrape_scheme_details.py
```

Expected result:

```text
Total schemes: 54
Successful: 54
Failed: 0
```

---

# 🧹 Step 3 — Clean the Data

Run:

```cmd
python src\cleaner.py
```

Output:

```text
data/processed/cleaned_schemes.json
```

---

# 🕸️ Step 4 — Connect to Neo4j Aura

Run:

```cmd
python src\neo4j_connection.py
```

Expected:

```text
Connecting to Neo4j Aura...
Successfully connected to Neo4j Aura!
```

---

# 🗄️ Step 5 — Load Knowledge Graph

Run:

```cmd
python src\neo4j_loader.py
```

The loader creates:

```text
Department
Scheme
District
Beneficiary
Benefit
Sponsor
```

and their relationships.

---

# 🔍 Step 6 — Verify Knowledge Graph

Open Neo4j Aura and run:

```cypher
MATCH (s:Scheme)
RETURN count(s) AS total_schemes;
```

Expected:

```text
54
```

Check district relationships:

```cypher
MATCH (s:Scheme)-[:AVAILABLE_IN]->(d:District)
RETURN count(*) AS district_relationships;
```

Current dataset:

```text
83
```

Check graph:

```cypher
MATCH (d:Department)-[:OFFERS]->(s:Scheme)
RETURN d, s
LIMIT 20;
```

---

# 🧠 Step 7 — Generate Embeddings

Run:

```cmd
python src\embedding_generator.py
```

The script creates embeddings for all schemes.

Verify:

```cypher
MATCH (s:Scheme)
RETURN
    count(s) AS total_schemes,
    count(s.embedding) AS schemes_with_embeddings;
```

Expected:

```text
total_schemes = 54
schemes_with_embeddings = 54
```

Check embedding dimensions:

```cypher
MATCH (s:Scheme)
WHERE s.embedding IS NOT NULL
RETURN
    s.name,
    size(s.embedding) AS embedding_dimensions
LIMIT 5;
```

Expected:

```text
embedding_dimensions = 1536
```

---

# 📐 Step 8 — Create Vector Index

Run in Neo4j Aura:

```cypher
CREATE VECTOR INDEX scheme_embeddings
IF NOT EXISTS
FOR (s:Scheme)
ON s.embedding
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 1536,
        `vector.similarity_function`: 'cosine'
    }
};
```

Check:

```cypher
SHOW VECTOR INDEXES;
```

Wait until:

```text
state = ONLINE
```

---

# 🔎 Step 9 — Test Vector Search

Run:

```cmd
python src\vector_search.py
```

Example question:

```text
What government schemes are available for farmers?
```

The system should return the most semantically relevant schemes.

---

# 🔀 Step 10 — Test Hybrid Retrieval

Run:

```cmd
python src\hybrid_retriever.py
```

Example:

```text
What schemes are available for farmers in Coimbatore?
```

The system combines:

```text
Graph Search
+
Vector Search
↓
RRF
↓
Top Results
```

---

# 🤖 Step 11 — Test Complete RAG Pipeline

Run:

```cmd
python -m src.rag_pipeline
```

The complete pipeline is:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   +
Graph Search
   ↓
Hybrid Retrieval
   ↓
RRF
   ↓
Context
   ↓
LLM
   ↓
Answer
```

---

# 💬 Step 12 — Run Streamlit

Start the chatbot:

```cmd
streamlit run app.py
```

Open the displayed local URL in your browser.

Usually:

```text
http://localhost:8501
```

---

# 🧪 Test Questions

Use the following questions to test the application.

### General scheme search

```text
What government schemes are available for farmers?
```

### District-based search

```text
What schemes are available in Coimbatore?
```

### Combined search

```text
What schemes can farmers in Coimbatore benefit from?
```

### Scheme-specific question

```text
Tell me about Training to Farmers.
```

### Application question

```text
How can I apply for Training to Farmers?
```

### Benefits

```text
What benefits are available to farmers?
```

### Eligibility

```text
Who is eligible for Training to Farmers?
```

---

# 🛡️ Hallucination Prevention

The RAG prompt instructs the LLM to use only retrieved information.

The chatbot should not invent:

```text
❌ Scheme names
❌ Benefits
❌ Eligibility
❌ Funding
❌ Application procedures
❌ Government departments
```

If information is unavailable, the chatbot should state that the available dataset does not contain sufficient information.

---

# 📚 Knowledge Graph Example

A user asks:

```text
What schemes are available for farmers in Coimbatore?
```

The graph can traverse:

```text
Farmer
   ▲
   │ TARGETS
   │
Scheme
   │
   │ AVAILABLE_IN
   ▼
Coimbatore
```

This is one of the main advantages of Knowledge Graph RAG: relationships between entities are explicitly represented.

---

# 🔎 Why Hybrid RAG?

Traditional vector RAG:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Similar Documents
```

Knowledge Graph RAG:

```text
Question
   ↓
Entities / Relationships
   ↓
Cypher
   ↓
Related Nodes
```

Hybrid RAG:

```text
                 Question
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Graph Search       Vector Search
          │                   │
          └─────────┬─────────┘
                    ▼
                 RRF
                    │
                    ▼
             Relevant Context
                    │
                    ▼
                   LLM
```

This provides both:

* **Structured relationship reasoning**
* **Semantic similarity**

---

# 📈 Future Enhancements

The current implementation can be extended with:

## 1. Query Understanding

Extract entities from user questions:

```text
District
Beneficiary
Scheme
Benefit
Eligibility
Intent
```

Example:

```text
"I am a small farmer from Coimbatore. What financial
assistance can I get?"
```

Could become:

```json
{
  "district": "Coimbatore",
  "beneficiary": "Farmer",
  "intent": "Find financial assistance"
}
```

---

## 2. Dynamic Cypher Generation

Use an LLM to convert natural-language questions into safe, validated Cypher queries.

---

## 3. Better Knowledge Graph

Expand the graph:

```text
Department
    │
    ▼
Scheme
 ├── Benefit
 ├── Eligibility
 ├── Beneficiary
 ├── District
 ├── Document
 ├── ApplicationMethod
 ├── Sponsor
 └── Source
```

---

## 4. Reranking

Add a reranker after hybrid retrieval:

```text
Graph Results
      +
Vector Results
      ↓
RRF
      ↓
Reranker
      ↓
Top-K Context
```

---

## 5. Multilingual Support

Support questions in:

```text
English
Tamil
Tanglish
```

Example:

```text
"Vivasayigalukku enna government schemes irukku?"
```

---

## 6. Conversation Memory

Allow follow-up questions:

```text
User:
What schemes are available for farmers?

Assistant:
...

User:
What about Coimbatore?

Assistant:
...
```

The system should understand that "What about Coimbatore?" refers to the previous topic.

---

## 7. Source Citations

Every answer should provide the original Tamil Nadu Government source.

Example:

```text
Source:
https://www.tn.gov.in/scheme_details.php?id=...
```

This improves transparency and trust.

---

# 🧪 Testing Strategy

The project can include three levels of testing.

## Unit Testing

Test individual components:

```text
Scraper
Cleaner
Neo4j connection
Graph Retriever
Vector Retriever
```

## Integration Testing

Test:

```text
Scraper
   ↓
Cleaner
   ↓
Neo4j
   ↓
Retriever
```

## End-to-End Testing

Test:

```text
User
 ↓
Streamlit
 ↓
Hybrid Retriever
 ↓
Neo4j
 ↓
LLM
 ↓
Answer
```

---

# ⚠️ Common Issues

## Neo4j Authentication Error

Check:

```env
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
```

Do not hard-code credentials in Python.

---

## SSL Certificate Error

If your Windows/Python environment requires the Certifi CA bundle:

```cmd
set SSL_CERT_FILE=D:\Workspace\TN_Scheme_KG_RAG\venv\Lib\site-packages\certifi\cacert.pem
```

Then retry the Neo4j connection.

---

## OpenAI API Key Error

Check:

```cmd
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(bool(os.getenv('OPENAI_API_KEY')))"
```

Expected:

```text
True
```

---

## Streamlit Import Error

Run Streamlit from the project root:

```cmd
streamlit run app.py
```

Do not execute `app.py` as a normal Python script.

---

# 🔐 Security

Never commit:

```text
.env
API keys
Neo4j passwords
Database credentials
```

Use environment variables instead.

Before pushing to GitHub:

```cmd
git status
```

Confirm `.env` is not listed.

---

# 📊 Project Outcome

The project demonstrates how modern RAG systems can combine:

```text
Web Scraping
      +
Data Engineering
      +
Knowledge Graph
      +
Vector Search
      +
Hybrid Retrieval
      +
LLM
      +
Streamlit
```

The resulting system provides a natural-language interface for discovering Tamil Nadu Government schemes while grounding responses in retrieved government data.

---

# 🎯 Learning Outcomes

Through this project, you will learn:

* Python project structure
* Playwright web scraping
* JSON data processing
* Data cleaning and normalization
* Neo4j fundamentals
* Cypher queries
* Knowledge Graph design
* Vector embeddings
* Vector indexes
* Semantic search
* Hybrid RAG
* Reciprocal Rank Fusion
* LLM integration
* Prompt engineering
* Streamlit application development
* RAG evaluation
* Basic application security

---

# 🏆 Buildathon Highlights

### Problem

Government scheme information can be difficult to discover using traditional keyword-based browsing.

### Solution

Build an AI-powered conversational assistant that retrieves relevant government schemes using both structured relationships and semantic similarity.

### Innovation

The solution combines:

```text
Knowledge Graph RAG
+
Vector RAG
+
Hybrid Retrieval
+
LLM
```

### Benefits

* Natural-language search
* Relationship-aware retrieval
* Semantic search
* Grounded answers
* Government source transparency
* Scalable architecture

---

# 📌 Data Source

Tamil Nadu Government official website:

```text
https://www.tn.gov.in/
```

The application should treat the official government website as the authoritative source for the scheme information collected by the scraper.

---

# 👩‍💻 Author

**TN Scheme Knowledge Graph RAG**

Built using:

```text
Python
Playwright
Neo4j Aura
OpenAI
LangChain
Streamlit
```

---

# 📄 License

This project is intended for educational, demonstration, and buildathon purposes.

Government scheme information may change over time. Users should verify important eligibility, benefit, and application details against the latest official Tamil Nadu Government information before taking action.
