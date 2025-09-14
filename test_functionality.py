#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from utils import extract_website_content, split_text_into_chunks, create_vectorstore

# Load environment variables
load_dotenv()

print("🧪 Testing RAG Chatbot Functionality")
print("=" * 50)

# Test 1: Check API Key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("✅ API Key found")
    print(f"   Key starts with: {api_key[:10]}...")
else:
    print("❌ API Key not found")

print()

# Test 2: Test website content extraction
test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
print(f"🌐 Testing website extraction with: {test_url}")

try:
    content = extract_website_content(test_url)
    if content:
        print(f"✅ Content extracted successfully")
        print(f"   Content length: {len(content)} characters")
        print(f"   First 200 chars: {content[:200]}...")
        
        # Test chunking
        print("\n📚 Testing text chunking...")
        chunks = split_text_into_chunks(content)
        print(f"✅ Created {len(chunks)} chunks")
        
        if chunks:
            # Test vector store creation
            print("\n🔍 Testing vector store creation...")
            vectorstore = create_vectorstore(chunks)
            print("✅ Vector store created successfully")
            
            # Test similarity search
            test_query = "What is artificial intelligence?"
            results = vectorstore.similarity_search(test_query, k=2)
            print(f"✅ Similarity search test: found {len(results)} results")
        
    else:
        print("❌ No content extracted")
        
except Exception as e:
    print(f"❌ Error during testing: {e}")

print("\n" + "=" * 50)
print("🎯 Test completed!")
