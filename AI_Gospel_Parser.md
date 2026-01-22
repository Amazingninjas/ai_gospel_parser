# AI Gospel Parser Project

## Project Vision

Build a data parser and research assistant AI that uses ChromaDB for perfect recall of all previous interactions. This system will use the ancient Greek version of the Old and New Testaments with Thayer's Greek lexicon as an English translation device to answer questions.

### Hardware Setup
*   **GPUs:** 1x NVIDIA GeForce RTX 1660 Super, 1x NVIDIA GeForce RTX 2070 Super (later upgraded to 2x NVIDIA GeForce RTX 3090s for the final system)
*   **RAM:** 96 GB
*   **CPU:** AMD Ryzen 7 7800X3D
*   **Storage:** >2 TB NVMe

The goal is to use both GPUs for processing.

## Initial Feasibility Assessment

The project is highly feasible and a great use case for modern open-source LLMs and vector databases. The constrained domain (Biblical Greek texts) is ideal for high accuracy.

### Pros
*   **Perfect Recall:** ChromaDB can store every verse and lexicon entry for exact retrieval.
*   **Deep Contextual Analysis:** Enables complex queries about word usage, grammar, and context (e.g., "Compare the usage of *logos* in John vs. Stoic philosophy").
*   **Scholarly Rigor:** Grounding responses in original texts and a trusted lexicon provides a high level of academic integrity.
*   **Efficiency:** Fast and cost-effective querying once the database is built.

### Cons & Challenges
*   **Data Preparation:** Sourcing clean, machine-readable digital texts of the Greek Old Testament (Septuagint), Greek New Testament, and Thayer's Lexicon is the biggest hurdle.
*   **Chunking Strategy:** Deciding how to split the text (by verse, paragraph, chapter) is critical for retrieval quality.
*   **Metadata:** Rich metadata (book, chapter, verse, source) is essential for filtering.
*   **"Illusion of Understanding":** The AI uses pattern matching, not true comprehension. User judgment remains critical.
*   **Lexicon Limitations:** Thayer's is a 19th-century lexicon and doesn't include a century of modern philological discoveries.
*   **Multi-GPU Complexity:** Running a single model across two different GPUs (1660 Super & 2070 Super) is non-trivial.

## Recommended AI Models & System Architecture

### AI Model Tiers (for initial 1660S/2070S setup)
*   **Tier 1 (Heavyweights - CPU/RAM focused):** Llama 3 70B. Slow but powerful.
*   **Tier 2 (Sweet Spot - VRAM/RAM balanced):** Mixtral 8x7B or Llama 3 13B. Best balance of speed and intelligence.
*   **Tier 3 (Speed Demons - GPU focused):** Phi-3 Mini/Medium or Gemma 7B. Fast for quick lookups.

### System Architecture Plan
1.  **Data Ingestion (ChromaDB):**
    *   Use a lightweight sentence transformer model (e.g., `all-MiniLM-L6-v2`) for creating embeddings.
    *   This can run on the 1660 Super.
2.  **Inference & Reasoning (LLM):**
    *   Use Ollama or `text-generation-webui` for multi-GPU support.
    *   Run the main LLM (e.g., Llama 3 13B) across both the 2070 Super and 1660 Super to maximize VRAM usage and speed.

### Workflow
1.  User asks a question.
2.  The system queries ChromaDB to find relevant Greek text and lexicon entries.
3.  A detailed prompt is constructed with the retrieved context.
4.  The prompt is sent to the main LLM, which synthesizes an answer based *only* on the provided context.

## Corpus Foundation: Textual Sources

### Phase 1 Corpus
*   **Old Testament:** Rahlfs-Hanhart edition Septuagint (academic standard).
*   **New Testament:** Nestle-Aland 28th Edition (NA28) as the primary text, with Byzantine/Majority Text variants included as parallel data.
*   **Lexicon:** Thayer's Greek Lexicon (structured data).

### Textual Choices Explained
*   **Nestle-Aland 28 (Critical Text):**
    *   **What:** An eclectic text compiled by scholars evaluating the earliest available manuscripts (e.g., Codex Vaticanus, Sinaiticus). It's the standard for modern academia and translations (ESV, NIV).
    *   **Why:** Aligns with a research-oriented approach, and its critical apparatus (showing textual variants) is valuable data for the AI.
*   **Byzantine/Majority Text (Traditional Text):**
    *   **What:** Based on the reading found in the vast majority (90%+) of later Greek manuscripts (9th-15th century).
    *   **Why Include:** Represents the stable text used by the church for over a millennium. Including its variants allows the AI to analyze significant textual differences (e.g., the Johannine Comma, Mark's longer ending).

### Sourcing Clean Texts
*   **Primary Source:** German Bible Society (Deutsche Bibelgesellschaft) for official digital versions of Rahlfs-Hanhart and NA28, likely in XML/TEI format.
*   **Other Sources:** Academic repositories like Thesaurus Linguae Graecae (TLG), Perseus Digital Library, and university archives (UPenn CCAT, Tyndale House).

## Core Logic: The Context System

### Initial Idea: Three-Paragraph Context
The initial idea was to capture the paragraph before a word, the paragraph containing the word, and the paragraph after it to provide rich context.

### Refined Hybrid Approach
This approach was adopted to be more flexible and efficient.
*   **Store at Sentence Level:** Store text at the sentence level but tag it with paragraph and section metadata.
*   **Dynamic Context Windows:** Allow the AI to dynamically pull context at different scales (immediate sentence, local sentences, full paragraph, or chapter).
*   **Reference-Based Storage:** Store each paragraph/sentence once and use references to avoid massive data duplication, especially for common words.

```python
# Example of reference-based storage
paragraphs_db = {
    "para_001": "Full paragraph text...",
    "para_002": "Next paragraph text..."
}

word_occurrences = {
    "word_id": "logos_001",
    "target_word": "λόγος", 
    "paragraphs": ["para_023", "para_024", "para_025"],
    "position": {"paragraph": "para_024", "sentence": 2, "word_index": 5}
}
```

## Final System: Dual-GPU Evaluation Architecture (2x 3090s)

For the final project phase, where new texts are evaluated for inclusion in the corpus.

*   **GPU 1: "Textual Critic AI"**
    *   **Focus:** Source evaluation, textual integrity, manuscript affinity, linguistic coherence, and stylometric analysis.
*   **GPU 2: "Theological Harmonizer AI"**
    *   **Focus:** Doctrinal coherence, conceptual alignment with the existing corpus, and hermeneutical value.

### Real-Time Evaluation Pipeline
A candidate text is processed by both AIs in parallel. A decision matrix then determines whether to automatically add the text, reject it, or flag it for human review based on the confidence scores from both models.

## Deployment Strategy for Multi-User Access (20+ Users)

A local server architecture is required, as a CLI is not suitable for concurrent users.

### Recommended Server Architecture
*   **Web Interface/API Server:** FastAPI to handle user requests.
*   **Model Serving:** A dedicated model serving framework (like vLLM or TGI) to host multiple AI models.
*   **Load Balancer:** To route queries to the appropriate model based on complexity and traffic.
*   **Vector Database:** ChromaDB running in client-server mode.
*   **Caching:** Redis for caching results of frequent queries.

### Model Deployment on 2x 3090s (48GB total VRAM)
*   **Primary Model (for complex queries):** Llama 3 70B (4-bit quantized) running across both GPUs using tensor parallelism. Can handle 5-8 concurrent users.
*   **Secondary Model (for general queries):** Mixtral 8x7B (4-bit quantized). Excellent balance of quality and throughput. Can handle 12-15 concurrent users.
*   **Specialized Model (for simple lookups):** A fine-tuned 7B or 8B model for tasks like grammar analysis. Can handle 20+ concurrent users.

This tiered model approach, combined with smart routing, ensures the system can handle a high volume of concurrent users efficiently while dedicating its most powerful model to the most complex research questions.
