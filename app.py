import streamlit as st
from utils import extract_website_content, split_text_into_chunks, create_vectorstore, generate_rag_response
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="🤖 AI Website Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add modern, clean CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Consistent Colors */
    :root {
        --primary-color: #2563eb;      /* blue-600 */
        --primary-hover: #1d4ed8;      /* blue-700 */
        --secondary-color: #0ea5e9;    /* sky-500 */
        --success-color: #16a34a;      /* green-600 */
        --error-color: #dc2626;        /* red-600 */
        --warning-color: #d97706;      /* amber-600 */
        --background-color: #f5f7fb;   /* subtle neutral */
        --card-background: #ffffff;
        --text-primary: #111827;       /* gray-900 */
        --text-secondary: #374151;     /* gray-700 */
        --border-color: #e5e7eb;       /* gray-200 */
        --border-radius: 12px;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Reset and Global Styles */
    .main {
        padding: 1rem 2rem;
        font-family: 'Inter', sans-serif;
        background: var(--background-color);
        color: var(--text-primary);
    }
    
    /* Header */
    .app-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .app-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .app-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin: 0;
        font-weight: 400;
    }
    
    /* Cards */
    .card {
        background: var(--card-background);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }
    
    /* Status Messages */
    .status-success {
        background: #ecfdf5;
        border: 1px solid var(--success-color);
        color: #14532d;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-error {
        background: #fef2f2;
        border: 1px solid var(--error-color);
        color: #7f1d1d;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-info {
        background: #eff6ff;
        border: 1px solid var(--primary-color);
        color: #1e40af;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Chat Messages */
    .chat-message {
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .chat-message.user {
        flex-direction: row-reverse;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 1rem 1.25rem;
        border-radius: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .message-bubble.user {
        background: var(--primary-color);
        color: white;
        border-bottom-right-radius: 0.5rem;
    }
    
    .message-bubble.assistant {
        background: var(--card-background);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-bottom-left-radius: 0.5rem;
        box-shadow: var(--shadow-sm);
    }
    
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        font-weight: 600;
        flex-shrink: 0;
    }
    
    .avatar.user {
        background: linear-gradient(135deg, var(--success-color), #15803d);
        color: white;
    }
    
    .avatar.assistant {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Primary Button Variant */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-color) !important;
        border-radius: var(--border-radius) !important;
        padding: 0.875rem 1.25rem !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        background: white !important;
        color: var(--text-primary) !important;
        min-height: 48px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        outline: none !important;
        transform: translateY(-1px) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.7 !important;
    }
    
    /* Sidebar specific styling */
    .stTextInput label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Chat Input */
    .stChatInput > div > div > div > div > input {
        border: 2px solid var(--border-color) !important;
        border-radius: 2rem !important;
        padding: 1rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sample Questions */
    .sample-questions {
        background: var(--card-background);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }
    
    .sample-questions h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--card-background) !important;
    }
    
    /* Sidebar headers */
    .sidebar h2, .sidebar h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar sections */
    .sidebar hr {
        border: none !important;
        height: 1px !important;
        background: var(--border-color) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Current website info styling */
    .website-info {
        background: var(--background-color);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .website-info p {
        margin: 0.5rem 0 !important;
        font-size: 0.9rem !important;
        color: var(--text-secondary) !important;
    }
    
    /* Welcome Section */
    .welcome-card {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--background-color) 0%, #e2e8f0 100%);
        border-radius: var(--border-radius);
        margin: 2rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .welcome-card h2 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 1.875rem;
        font-weight: 700;
    }
    
    .welcome-card p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .feature-list {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
        margin: 1rem 0;
        text-align: left;
    }
    
    .feature-list h3 {
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    .feature-list ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-list li {
        margin: 0.75rem 0;
        color: var(--text-secondary);
        font-size: 0.95rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .app-header {
            padding: 2rem 1rem;
        }
        
        .app-header h1 {
            font-size: 2rem;
        }
        
        .message-bubble {
            max-width: 90%;
        }
        
        .welcome-card {
            padding: 2rem 1rem;
        }
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
if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = os.getenv("GOOGLE_API_KEY") or (st.secrets.get("GOOGLE_API_KEY") if hasattr(st, "secrets") else "")
if "current_url" not in st.session_state:
    st.session_state.current_url = ""

# Main header
st.markdown("""
<div class="app-header">
    <h1>🤖 AI Website Chat Assistant</h1>
    <p>Transform any website into an intelligent conversation partner</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌐 **Website Setup**")
    
    # Sample website suggestions
    st.markdown("### 📱 **Quick Start - Try These:**")
    col1, col2 = st.columns(2)
    
    sample_sites = {
        "🏦️ Wikipedia": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "📰 Medium Article": "https://medium.com/3streams/teaching-charlie-kirk-in-my-classroom-satire-on-august-27-death-on-september-10-87ab89f1de49",
        "🧠 OpenAI Research": "https://openai.com/research",
        "📊 BBC Technology": "https://www.bbc.com/news/technology"
    }
    
    selected_sample = None
    with col1:
        for i, (name, url) in enumerate(list(sample_sites.items())[:2]):
            if st.button(name, key=f"sample_{i}"):
                selected_sample = url
                st.session_state.current_url = url
    
    with col2:
        for i, (name, url) in enumerate(list(sample_sites.items())[2:], 2):
            if st.button(name, key=f"sample_{i}"):
                selected_sample = url
                st.session_state.current_url = url
    
    st.markdown("---")
    
    # URL input
    default_value = selected_sample if selected_sample else st.session_state.get('current_url', '')
    website_url = st.text_input(
        "🔗 **Or enter your own URL:**",
        value=default_value,
        placeholder="https://medium.com/your-article-here",
        help="Enter any website URL you'd like to chat with"
    )
    
    # Debug info (remove this in production)
    if website_url:
        st.info(f"Debug: URL to process: {website_url}")
    
    # Debug API key status
    api_status = "✅ API Key Found" if st.session_state.google_api_key else "❌ API Key Missing"
    st.info(f"Debug: {api_status}")
    
    # Process button
    process_button = st.button("🚀 **Process Website**", type="primary")
    
    # Processing logic
    if process_button:
        if not website_url:
            st.markdown('<div class="status-error">❌ Please enter a website URL first!</div>', unsafe_allow_html=True)
        elif not st.session_state.google_api_key:
            st.markdown('<div class="status-error">❌ Google API key not found! Please check your .env file.</div>', unsafe_allow_html=True)
        else:
            # Show processing status
            progress_placeholder = st.empty()
            
            try:
                with progress_placeholder:
                    st.markdown('<div class="status-info">🔄 Processing website content...</div>', unsafe_allow_html=True)
                
                # Extract website content
                st.session_state.website_content = extract_website_content(website_url)
                
                if st.session_state.website_content and len(st.session_state.website_content.strip()) > 50:
                    with progress_placeholder:
                        st.markdown('<div class="status-info">⚙️ Analyzing and chunking content...</div>', unsafe_allow_html=True)
                    
                    # Split into chunks
                    st.session_state.chunks = split_text_into_chunks(st.session_state.website_content)
                    
                    if st.session_state.chunks:
                        # Create vector store
                        st.session_state.vectorstore = create_vectorstore(st.session_state.chunks)
                        
                        st.session_state.process_clicked = True
                        st.session_state.current_url = website_url
                        
                        # Success message
                        progress_placeholder.markdown(
                            f'<div class="status-success">✅ Success! Found {len(st.session_state.chunks)} content chunks.<br/>🎯 Ready to chat!</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        progress_placeholder.markdown(
                            '<div class="status-error">❌ No meaningful content found to process.<br/>Please try a different URL.</div>',
                            unsafe_allow_html=True
                        )
                else:
                    progress_placeholder.markdown(
                        '<div class="status-error">❌ Failed to extract content from website.<br/>Please check the URL and try again.</div>',
                        unsafe_allow_html=True
                    )
            except Exception as e:
                progress_placeholder.markdown(
                    f'<div class="status-error">❌ Error processing website: {str(e)}<br/>Please try again or use a different URL.</div>',
                    unsafe_allow_html=True
                )
    
    # Current website info
    if st.session_state.process_clicked:
        st.markdown("---")
        st.markdown(
            f"""
            <div class="website-info">
                <p><strong>🌐 Current Website:</strong></p>
                <p>🔗 {st.session_state.current_url}</p>
                <p>📄 {len(st.session_state.chunks)} content chunks processed</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # About section
    st.markdown("---")
    st.markdown("### ℹ️ **How It Works**")
    st.markdown("""
    1. **🔗 Enter URL** - Paste any website link
    2. **⚡ Process** - AI extracts and analyzes content  
    3. **💬 Chat** - Ask questions about the content
    4. **🤖 Get Answers** - Powered by Google Gemini AI
    """)

# Main chat interface
if st.session_state.process_clicked:
    
    # Sample questions section
    st.markdown("""
    <div class="sample-questions">
        <h3>💡 <strong>Sample Questions to Get Started</strong></h3>
        <p>Click on any question below to ask the AI:</p>
    </div>
    """, unsafe_allow_html=True)
    
    sample_questions = [
        "🎯 What is the main topic of this website?",
        "📋 Can you summarize the key information?", 
        "🛍️ What products or services are mentioned?",
        "👥 Who is the target audience?",
        "💡 What are the key insights or takeaways?",
        "📊 What data or statistics are presented?"
    ]
    
    # Display sample questions in a grid
    col1, col2, col3 = st.columns(3)
    
    for i, question in enumerate(sample_questions):
        col_index = i % 3
        if col_index == 0:
            current_col = col1
        elif col_index == 1:
            current_col = col2
        else:
            current_col = col3
            
        with current_col:
            if st.button(question, key=f"sample_q_{i}", help=f"Ask: {question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                with st.spinner("🤖 AI is thinking..."):
                    response = generate_rag_response(question, st.session_state.vectorstore)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.markdown("---")
    
    # Chat history display
    st.markdown("### 💬 **Chat Conversation**")
    
    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.messages:
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="message-bubble user">
                            {message["content"]}
                        </div>
                        <div class="avatar user">👤</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <div class="avatar assistant">🤖</div>
                        <div class="message-bubble assistant">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-info">👋 Ask your first question to get started!</div>', unsafe_allow_html=True)
    
    # User input at the bottom
    st.markdown("---")
    user_query = st.chat_input("💭 Type your question about the website here...")
    
    if user_query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Generate response
        with st.spinner("🤖 AI is analyzing and responding..."):
            response = generate_rag_response(user_query, st.session_state.vectorstore)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to show new messages
        st.rerun()

else:
    # Welcome message when no website is processed
    st.markdown("""
    <div class="welcome-card">
        <h2>🚀 Ready to Chat with Any Website?</h2>
        <p>Get started by selecting a sample website or entering your own URL in the sidebar.</p>
        <div class="feature-list">
            <h3>✨ What can you do?</h3>
            <ul>
                <li>🔍 <strong>Ask questions</strong> about website content</li>
                <li>📊 <strong>Get summaries</strong> of key information</li>
                <li>💡 <strong>Extract insights</strong> from articles or pages</li>
                <li>🎯 <strong>Find specific</strong> products, services, or data</li>
            </ul>
        </div>
        <p style="color: var(--text-secondary); font-style: italic; margin-top: 1rem;">👈 Start by clicking "Process Website" in the sidebar</p>
    </div>
    """, unsafe_allow_html=True)
