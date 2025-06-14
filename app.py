import streamlit as st
import os
import json
from dotenv import load_dotenv
import groq
import requests

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="LegalAI - Professional Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

# Initialize Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

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
        
        # Get response from Groq
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=messages,
            temperature=0.1,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return None

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

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
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
