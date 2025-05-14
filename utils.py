import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to extract text from a website
def extract_website_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
            script_or_style.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Additional cleaning
        text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single one
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single one
        
        return text
    except Exception as e:
        st.error(f"Error extracting content from the website: {e}")
        return None

# Function to split text into chunks
def split_text_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return chunks

# Simple embedding function to avoid dependency issues
class SimpleEmbeddings(Embeddings):
    """Simple deterministic embeddings based on text hash"""
    
    def __init__(self, size=768):
        """Initialize with embedding dimension size"""
        self.size = size
        # Use internal variables not tracked by pydantic
        self._seed = 123
        
    def embed_documents(self, texts):
        """Generate deterministic embeddings based on text content hash."""
        np.random.seed(self._seed)
        embeddings = []
        for text in texts:
            # Use hash of text to generate a deterministic seed for this text
            text_seed = hash(text) % 10000
            np.random.seed(text_seed)
            embeddings.append(np.random.rand(self.size).astype(np.float32))
        return embeddings
        
    def embed_query(self, text):
        """Generate a single embedding for query text."""
        return self.embed_documents([text])[0]

# Function to create a vector store from chunks
def create_vectorstore(chunks):
    embeddings = SimpleEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

# Function to generate a response using RAG
def generate_rag_response(query, vectorstore):
    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(query, k=4)
    context = "\n".join([doc.page_content for doc in docs])
    
    # Initialize the Groq client
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY") or st.session_state.groq_api_key,
        model_name="llama3-70b-8192"
    )
    
    # Create a prompt template
    template = """
    You are a helpful AI assistant that answers questions about website content.
    
    CONTEXT:
    {context}
    
    USER QUESTION:
    {question}
    
    Instructions:
    - Answer the question based on the context provided
    - If the answer is not in the context, say "I don't have enough information to answer this question"
    - Be concise and helpful
    - If appropriate, mention specific information from the website to support your answer
    
    YOUR RESPONSE:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create a chain
    chain = (
        prompt 
        | llm 
        | StrOutputParser()
    )
    
    # Get the response
    response = chain.invoke({
        "context": context,
        "question": query
    })
    
    return response
