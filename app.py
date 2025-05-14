import streamlit as st
from utils import extract_website_content, split_text_into_chunks, create_vectorstore, generate_rag_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Chat with Any Website",
    page_icon="🌐",
    layout="wide",
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #f0f0f0;
    }
    .chat-message.bot {
        background-color: #e6f7ff;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .content {
        width: 80%;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .stTextInput > div > div > input {
        background-color: white;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "website_content" not in st.session_state:
    st.session_state.website_content = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "process_clicked" not in st.session_state:
    st.session_state.process_clicked = False
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

# Main app layout
st.title("🌐 Chat with Any Website")

# Sidebar
with st.sidebar:
    st.header("Website Input")
    website_url = st.text_input("Enter website URL:", "https://example.com")
    
    api_key = st.session_state.groq_api_key
    if api_key:
        st.session_state.groq_api_key = api_key
    
    process_button = st.button("Process Website")
    
    if process_button:
        if not st.session_state.groq_api_key:
            st.error("Please enter your GROQ API key.")
        else:
            with st.spinner("Processing website content..."):
                # Extract website content
                st.session_state.website_content = extract_website_content(website_url)
                
                if st.session_state.website_content:
                    # Split into chunks
                    st.session_state.chunks = split_text_into_chunks(st.session_state.website_content)
                    
                    # Create vector store
                    st.session_state.vectorstore = create_vectorstore(st.session_state.chunks)
                    
                    st.session_state.process_clicked = True
                    st.success(f"Website processed! Found {len(st.session_state.chunks)} chunks of content.")
                else:
                    st.error("Failed to process website.")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app allows you to chat with any website using RAG (Retrieval Augmented Generation) with the GROQ API.
    
    1. Enter a website URL
    2. Click "Process Website"
    3. Ask questions about the website content
    """)

# Chat interface
if st.session_state.process_clicked:
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_query = st.chat_input("Ask something about the website...")
    
    if user_query:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_rag_response(user_query, st.session_state.vectorstore)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("👈 Enter a website URL in the sidebar and click 'Process Website' to start chatting.")

# Sample questions section
if st.session_state.process_clicked:
    st.markdown("### Sample questions to ask:")
    col1, col2 = st.columns(2)
    
    sample_questions = [
        "What is the main topic of this website?",
        "Can you summarize the key information?",
        "What products or services are mentioned?",
        "Who is the target audience for this website?"
    ]
    
    with col1:
        for i in range(0, len(sample_questions), 2):
            if st.button(sample_questions[i]):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": sample_questions[i]})
                
                # Generate response
                response = generate_rag_response(sample_questions[i], st.session_state.vectorstore)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Force a rerun to display the messages
                st.experimental_rerun()
    
    with col2:
        for i in range(1, len(sample_questions), 2):
            if st.button(sample_questions[i]):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": sample_questions[i]})
                
                # Generate response
                response = generate_rag_response(sample_questions[i], st.session_state.vectorstore)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Force a rerun to display the messages
                st.experimental_rerun()
