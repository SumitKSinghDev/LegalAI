import streamlit as st

# Set page config - must be the first Streamlit command
st.set_page_config(
    page_title="LegalAI - Professional Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import json
from dotenv import load_dotenv
import requests
import httpx

# Load environment variables
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .content {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 1rem;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        flex: 1;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2b313e;
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

def get_legal_response(prompt, chat_history=None):
    """Get response from Groq API with legal context."""
    try:
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": """You are a highly qualified legal advisor trained to provide detailed, accurate, and well-researched legal responses.
                You MUST ONLY respond to legal questions and legal matters.
                For all legal responses, always provide:
                - A summary of the facts
                - Identification of legal issues
                - Step-by-step legal analysis
                - Reference to relevant laws
                - Mention of landmark cases
                - A well-structured conclusion
                """
            }
        ]
        
        # Add chat history if available
        if chat_history:
            messages.extend(chat_history)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})
        
        # Make API request to Groq (updated endpoint)
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-r1-distill-llama-70b",
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return None

# Main container
with st.container():
    # App title and description
    st.title("⚖️ LegalAI - Professional Legal Assistant")
    st.markdown("""
    A sophisticated legal chatbot powered by advanced AI technology, featuring memory management and professional legal consultation capabilities.
    """)

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI-powered legal assistant provides:
    - Professional legal analysis
    - Case law references
    - Statutory interpretation
    - Legal research assistance
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
with st.container():
    if prompt := st.chat_input("Ask your legal question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your legal query..."):
                response = get_legal_response(prompt, st.session_state.messages)
                if response:
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to get response. Please try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Disclaimer:</strong> This application provides legal information for educational and informational purposes only. 
    It does not constitute legal advice and should not be relied upon as a substitute for consultation with a qualified attorney.</p>
</div>
""", unsafe_allow_html=True)
