
# 🗡️ The HashiraMart AI Platform

### *Personalization • Business Intelligence • Conversational AI • Operational Excellence*

-----

## ⚔️ 1. Overview

**HashiraMart** is an advanced e-commerce platform demonstrating a comprehensive suite of AI capabilities that drive business value across the entire customer lifecycle. The platform integrates four distinct AI systems into a unified architecture:

1.  **AI Recommender System (Personalization):** A classic machine learning model that provides personalized product recommendations to users, trained on synthetically generated interaction data.

2.  **AI Sales Forecaster (Business Intelligence):** A time-series model that predicts future product sales, enabling smarter inventory and marketing decisions.

3.  **Conversational AI Chatbot (Customer Experience):** An intelligent, RAG-powered chatbot that uses **Google's Gemini** to answer user questions about products in a natural, context-aware manner, acting as an AI sales assistant.

4.  **Conversation Summarizer (Operational Excellence):** An internal tool that uses a **Flan-T5** model to summarize customer support conversations, enabling rapid quality assurance and identification of agent training needs.

This documentation covers the full technical design, from large-scale data processing with Spark to the real-time deployment of these diverse AI models.

-----

## 🧠 2. System Architecture

The architecture integrates real-time ML services, offline training pipelines, and large-language model (LLM) components into a cohesive system.

```plaintext
                                    .------------------------.
                                    |  Cloud Database        |
                                    |  (Neon/Supabase)       |
                                    `----------+-------------'
                                               | (App Data, Product Info)
 .---------------------------------------------+----------------------------------------------.
 |                                             |                                              |
 |  (1) MLOps & Application Stack              |        (2) Big Data Stack                    |
 |                                             |                                              |
 | .----------------------------------------.  | .-----------------.  .--------------------.  |
 | | FastAPI App                            |  | | Spark Job API   |--| YARN Cluster / Spark |  |
 | | - /recommendations (ML)                |  | `-----------------'  `--------------------'  |
 | | - /forecasts (ML)                      |  |                            | (Raw Data)      |
 | | - /chat (LLM)                          |  |                            v                 |
 | `---------+--------------------+---------'  |                  .------------------.        |
 |           |                    |             |                  | Data Lake (HDFS) |        |
 |           | (Product Info)     | (Vector Search) |                  `------------------'        |
 | .---------v----------. .-------v--------.  |                                              |
 | | External LLM API   | | Vector DB      |  |                                              |
 | | (Gemini)           | | (ChromaDB)     |  |                                              |
 | `--------------------' `----------------'  |                                              |
 `---------------------------------------------|----------------------------------------------'
                                               |
 .-------------------------------------.       | (Clean Data)
 | MLflow Server & MinIO Artifact Store| <---- '
 `-------------------------------------'
```

-----

## ⚙️ 3. Core ML Systems (Recommender & Forecaster)

These systems follow a traditional MLOps lifecycle, beginning with large-scale data processing.

1.  **Data Generation & Processing:** Synthetic user interaction and sales data are generated and uploaded to the **HDFS Data Lake**. A **PySpark** job, triggered by an API, reads this raw data, cleans it, engineers features, and writes the final, model-ready datasets to **MinIO**.
2.  **Model Training (DVC & MLflow):** A `dvc repro` pipeline, triggered by an API, pulls the clean data from MinIO and trains two separate models:
      * **Recommender:** A **LightGBM** model trained on user-item interaction counts.
      * **Forecaster:** A **Scikit-learn** model trained on time-series sales data.
3.  **Deployment:** Both models are logged to **MLflow**. The FastAPI application loads the "Production" stage models to serve live predictions via the `/recommendations/me` and `/forecasts/sales` endpoints.

-----

## 🤖 4. Conversational AI: The RAG-Powered Product Chatbot

To provide an exceptional customer experience, the platform includes an intelligent chatbot that acts as a product expert. This is currently prototyped in Google Colab.

### Purpose

Acts as an AI sales assistant, answering user questions about products ("Does this sword work well with Water Breathing?", "What is the blade made of?") to increase engagement and drive conversions.

### How It Works (Retrieval-Augmented Generation)

The chatbot uses a RAG architecture to provide accurate answers based on our product catalog, preventing the LLM from making things up.

1.  **Indexing (Offline Process):** When a new product is added to our e-commerce store, its description is passed through an **embedding model** to create a numerical vector. This vector, which represents the semantic meaning of the description, is stored in a **ChromaDB vector database**.

2.  **Querying (Real-Time):**

      * A user asks a question in the chat interface.
      * The question is converted into a vector using the same embedding model.
      * **ChromaDB** is searched to find the product description vectors that are most similar to the question vector.
      * The user's question and the retrieved product descriptions are combined into a detailed prompt.
      * This prompt is sent to **Google's Gemini API**, which generates a natural, accurate answer based on the provided context.

-----

## 📈 5. Operational AI: Support Conversation Summarizer

To ensure high-quality customer service without requiring managers to read through hours of transcripts, we use a summarization model. This is currently prototyped in Google Colab using the `knkarthick/dialogsum` dataset.

### Purpose

Automate the quality assurance process for customer support. It provides quick, concise summaries of conversations, allowing managers to review agent performance, identify issues, and find training opportunities much more efficiently.

### How It Works (Prompt-Based Summarization)

1.  A conversation transcript between a customer and a support agent is retrieved.
2.  The transcript is inserted into a predefined prompt template, such as: `Summarize the following customer support conversation and identify the key issue and the resolution:`
3.  This prompt is fed to a fine-tuned **Flan-T5 model**.
4.  The model generates a structured summary, which can be stored in a database and displayed on an internal quality assurance dashboard.

-----

## 💡 6. Project Status & Integration Roadmap

This project combines a fully containerized core system with two advanced AI features currently in the prototyping phase.

  * **Integrated Core System:** The Recommender, Forecaster, and the complete MLOps/Big Data pipeline (FastAPI, DVC, MLflow, Spark, Hadoop) are fully containerized and functional.
  * **Prototypes (Google Colab):** The **RAG Chatbot** and the **Conversation Summarizer** have been developed and validated as proofs-of-concept in a Google Colab environment.

### Integration Roadmap

The next steps to fully integrate all features into the main application are:

1.  **Chatbot Integration:**
      * Add **ChromaDB** as a new service in the `docker-compose-mlops.yml` file.
      * Create an offline script to perform the indexing step (reading from the product database and populating ChromaDB).
      * Build the `POST /chat` endpoint in the FastAPI application to implement the real-time querying logic.
2.  **Summarizer Integration:**
      * Containerize the Flan-T5 model into its own microservice (e.g., using a simple FastAPI wrapper or a dedicated tool like TorchServe).
      * Build an internal API endpoint (e.g., `POST /summarize/conversation`) that the main application can call.
      * Develop a simple internal-facing dashboard to display the generated summaries.