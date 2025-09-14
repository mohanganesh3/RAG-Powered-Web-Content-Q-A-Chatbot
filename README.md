# 🌐 RAG-Powered Web Content Q\&A Chatbot

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-ff4b4b?logo=streamlit&logoColor=white)](https://rag-powered-web-content-q-a-chatbot-lfbp5fwkgnppgdnfpyae8v.streamlit.app/)

Imagine a chatbot that can dive into any website and answer your questions with precision, pulling insights directly from the site’s content. This project creates an AI-powered chatbot that does just that, using **Retrieval-Augmented Generation (RAG)** to deliver accurate and contextually relevant responses based on website content.

---

## 🚀 What We Will Build

In this project, we will build an AI chatbot that can:

* Extract and process content from any given website.
* Answer user queries based on the retrieved website content.
* Use RAG to enhance response quality by combining retrieved information with generative AI capabilities.

---

## 🧠 Brief Explanation of How RAG Works

**Retrieval-Augmented Generation (RAG)** combines three key steps:

1. **Retrieval**: The system fetches relevant information from an external source (a website).
2. **Augmentation**: The retrieved information is used to enrich the AI’s prompt.
3. **Generation**: The language model generates a response combining its knowledge with the augmented context.

---

## 🔍 How Does RAG Work?

* **Text Vectorization**: Website content is converted into vector representations.
* **Similarity Search**: Vectors are compared to find chunks most relevant to the query.
* **Augmentation**: Retrieved chunks are added to the AI’s prompt to guide generation.

This ensures the chatbot provides answers that are both informed by the website’s content and enhanced by the AI’s understanding.

---

## 🛠️ Step-by-Step Guide to Building the Chatbot

### ✅ Step 1: Set Up Your Environment

Install required libraries:

```bash
pip install -r requirements.txt
```

### 🔐 Create a `.env` File

To securely store your API key, create a `.env` file in your project directory and add the following line:

```env
GROQ_API_KEY=your_groq_api_key
```

> ⚠️ **Note:** Never share your `.env` file publicly or commit it to version control.

---

### ✅ Step 2: Load and Process Website Content

The chatbot uses requests and BeautifulSoup to extract text from a website. The content is then split into smaller chunks using langchain-text-splitters and stored in a FAISS vector store with custom embeddings.

```python
from utils import extract_website_content, split_text_into_chunks, create_vectorstore

website_content = extract_website_content(website_url)
chunks = split_text_into_chunks(website_content)
vectorstore = create_vectorstore(chunks)
```

---

### ✅ Step 3: Set Up the Conversational AI Chain

The chatbot uses langchain-groq with the llama3-70b-8192 model to generate responses. A RAG pipeline retrieves relevant chunks and augments the AI’s prompt.

```python
from utils import generate_rag_response

response = generate_rag_response(user_query, vectorstore)
```

---

### ✅ Step 4: Build the Streamlit Interface

Create an interactive web interface using Streamlit. Users can input a URL, process the content, and chat with the bot.

```python
import streamlit as st

st.title("🌐 Chat with Any Website")
website_url = st.text_input("Enter website URL:", "https://example.com")
process_button = st.button("Process Website")

if process_button:
    st.session_state.website_content = extract_website_content(website_url)
    st.session_state.chunks = split_text_into_chunks(st.session_state.website_content)
    st.session_state.vectorstore = create_vectorstore(st.session_state.chunks)
    st.session_state.process_clicked = True
```

---

### ✅ Step 5: Testing and Demo

Run the Streamlit app:

```bash
streamlit run app.py
```

Enter a website URL, click "Process Website", and start asking questions.

**Example:**

* Website: [https://example.com](https://example.com)
* Query: “What is the main topic of this website?”
* Response: “The main topic of the website is to provide a placeholder example for web development and testing purposes.”

---

## ✨ Features

* ✅ **Website Processing**: Extracts and processes content from any accessible website.
* ✅ **Interactive Chat**: Maintains chat history and supports dynamic Q\&A.
* ✅ **Sample Questions**: Provides suggested questions for easy exploration.
* ✅ **Custom Styling**: Clean and user-friendly interface with custom CSS.

---

## 🔧 Extending the Chatbot

You can enhance the chatbot by:

* Supporting multiple websites at once.
* Adding other data sources (PDFs, APIs).
* Customizing for use cases like e-commerce, education, or customer support.
* Adding voice input or multilingual support.

---

## 📦 Requirements

Check `requirements.txt` for full list:

```text
streamlit==1.31.1
langchain-groq==0.1.2
faiss-cpu==1.7.4
requests==2.31.0
beautifulsoup4==4.12.2
```

---

## ⚠️ Notes

* Make sure your `.env` file includes a valid `GROQ_API_KEY`.
* We use a simple deterministic embedding function to avoid external dependencies. For better results, consider using models from Hugging Face or OpenAI.
* Some websites may restrict scraping—always follow their terms of service.

---

🌍 Explore the web like never before with this RAG-powered chatbot!
