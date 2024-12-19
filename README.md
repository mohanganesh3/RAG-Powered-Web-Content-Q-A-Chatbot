

# RAG-Powered Web Content Q&A Chatbot

Think of a chatbot that can read and understand any website you give it. Imagine asking this chatbot questions based on the content of the website, and receiving accurate, insightful answers. In this project, we aim to create an AI-powered chatbot that can interact with users and answer their questions based on the content of any given website.

# What We Will Build

In this project, we will use Langchain, Google Generative AI, and Groq to build an AI chatbot that can:
	•	Load and process the content of any website.
	•	Answer user queries based on the content retrieved from the website.
	•	Leverage Retrieval-Augmented Generation (RAG) to improve the quality and relevance of responses.

# Brief explanation of how RAG works

A RAG bot is short for Retrieval-Augmented Generation. This means that we are going to "augment" the knowledge of our LLM with new information that we are going to pass in our prompt. We first vectorize all the text that we want to use as "augmented knowledge" and then look through the vectorized text to find the most similar text to our prompt. We then pass this text to our LLM as a prefix

<img width="1088" alt="Screenshot 2024-12-14 at 7 54 19 AM" src="https://github.com/user-attachments/assets/d8d0fcef-bf03-41fe-a272-61ab8addc98f" />

Retrieval-Augmented Generation (RAG) combines two processes:
	1.	Retrieval: The system retrieves relevant information from an external source (e.g., a document, database, or website).
	2.	Augmentation: This retrieved information is then used to enrich the model’s response.
	3.	Generation: The language model combines its pre-trained knowledge with the augmented context to generate a contextually accurate response.

 # How Does RAG Work?
 
  •	Text Vectorization: The external text is converted into vector representations, making it easier to compare and retrieve similar content.
	•	Similarity Search: The system searches for text most relevant to the user’s query by comparing vectors.
	•	Augmentation: The retrieved text is included as a prefix in the prompt to guide the LLM’s response generation.

This dual approach allows RAG bots to bridge the gap between static, pre-trained knowledge and dynamic, real-time data, ensuring accurate and timely responses.

This process ensures that the chatbot answers based on both its internal understanding and the real-time data it fetches, resulting in more accurate and relevant responses.

# Step-by-Step Guide to Building the Chatbot

## Step 1: Set Up Your Environment

First, we need to install the required libraries. Run the following command:

pip install streamlit langchain langchain_groq langchain_google_genai langchain_community

Then, create a .env file to securely store your API keys:

    GROQ_API_KEY=your_groq_api_key
    GOOGLE_API_KEY=your_google_api_key

## Step 2: Load and Process Website Content

We will use Langchain’s WebBaseLoader to load the website’s content. This content will be split into smaller chunks to make it easier to process. After that, we will generate embeddings using Google Generative AI to create a vector store for the content.

    from langchain_community.document_loaders import WebBaseLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_community.vectorstores import Chroma

    def get_vectorstore_from_url(url):
        loader = WebBaseLoader(url)
        document = loader.load()
    
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)
    
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = Chroma.from_documents(document_chunks, embeddings)

        return vector_store

## Step 3: Set Up the Conversational AI Chain

Now, integrate Groq’s ChatGroq model to handle the conversation. We will create a retriever chain to fetch relevant content and a generation chain to provide answers based on that content.

    from langchain_groq import ChatGroq
    from langchain.chains import create_history_aware_retriever, create_retrieval_chain

    def get_context_retriever_chain(vector_store):
        llm = ChatGroq(groq_api_key="your_groq_api_key", model_name="Llama3-8b-8192")
        retriever = vector_store.as_retriever()
    
        retriever_chain = create_history_aware_retriever(llm, retriever)
        return retriever_chain

## Step 4: Build the Streamlit Interface

We will use Streamlit to create an interactive web interface where users can input a website URL and ask questions. The chatbot will then generate answers based on the website’s content.

    import streamlit as st

    st.set_page_config(page_title="Chat with Websites", page_icon="🤖")
    st.title("Chat with Websites")

    website_url = st.text_input("Enter a website URL")
    if website_url:
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = get_vectorstore_from_url(website_url)
    
        user_query = st.text_input("Ask me something about the website...")
        if user_query:
            response = get_response(user_query)
            st.session_state.chat_history.append({"role": "Human", "content": user_query})
            st.session_state.chat_history.append({"role": "AI", "content": response})

        for message in st.session_state.chat_history:
            st.write(f"{message['role']}: {message['content']}")

## Step 5: Testing and Demo

Once everything is set up, run the Streamlit app with:

  streamlit run app.py

Now, you can enter a website URL and start interacting with the chatbot. Ask it questions related to the website’s content, and it will provide relevant answers.

Demo

Try entering different websites and ask questions about their content. The chatbot will retrieve relevant information from the website and generate responses accordingly.

<img width="1435" alt="Screenshot 2024-12-19 at 6 30 37 PM" src="https://github.com/user-attachments/assets/81db8487-cc65-41e0-93ef-d39ea8181ed9" />
**Website Used** : https://madewithml.com/courses/mlops/setup/

You can now engage with the AI chatbot to explore and retrieve insights about the website or delve into specific details contained within its content.
<img width="1438" alt="Screenshot 2024-12-19 at 6 31 44 PM" src="https://github.com/user-attachments/assets/980102bc-9d9a-4a65-a8c2-ba43baafa097" />

Example,
Here i am asking about Cluster 
**Query**= What is Cluster

**Response**:
<img width="1436" alt="Screenshot 2024-12-19 at 6 35 05 PM" src="https://github.com/user-attachments/assets/5d3b5568-6eb3-4107-b7b7-cace33127fcb" />

### Chatbot will remember your previous questions you can even ask like tell me more about it 
**Response**:

<img width="1440" alt="Screenshot 2024-12-19 at 6 37 27 PM" src="https://github.com/user-attachments/assets/35b806f1-c543-4bde-b74a-272326e690d2" />

You can explore even more by extending this chatbot to handle multiple websites, integrate additional data sources, or customize it for specific use cases like e-commerce, education, or customer support. The possibilities are endless!
