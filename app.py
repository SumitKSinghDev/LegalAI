import streamlit as st
import os
import json
from dotenv import load_dotenv

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

try:
    from agno.agent import Agent
    from agno.tools.duckduckgo import DuckDuckGoTools
    from agno.models.groq import Groq
except ImportError as e:
    st.error(f"Error importing required packages: {str(e)}")
    st.info("Please make sure all dependencies are installed. Run: pip install -r requirements.txt")
    st.stop()

# Create legal agent
def create_legal_agent(chat_history=None):
    """Create a legal AI agent with enhanced instructions and context."""
    try:
        context_prompt = ""
        if chat_history:
            context_prompt = "\n\nPrevious conversation context:\n"
            for msg in chat_history[-5:]:  # Last 5 messages for context
                context_prompt += f"{msg['role'].title()}: {msg['content'][:200]}...\n"
        
        agent = Agent(
            model=Groq(id="deepseek-r1-distill-llama-70b", temperature=0.1),
            description="You are a highly qualified legal advisor trained to provide detailed, accurate, and well-researched legal responses.",
            instructions=[
                "🚨 CRITICAL: You are EXCLUSIVELY a Legal AI Assistant. You MUST ONLY respond to legal questions and legal matters.",
                "❌ STRICTLY REFUSE: If asked about anything non-legal (technology, cooking, sports, entertainment, personal advice, general knowledge, math, science, etc.), respond: 'I apologize, but I am a specialized Legal AI Assistant. I can only provide assistance with legal matters, legal research, case analysis, statutory interpretation, and legal consultation. Please ask me a legal question.'",
                "✅ LEGAL TOPICS ONLY: Constitutional law, civil law, criminal law, corporate law, family law, property law, contract law, tort law, administrative law, labor law, tax law, intellectual property law, international law, legal procedures, case analysis, statutory interpretation, legal research, court procedures, legal documentation, legal precedents, and legal advice.",
                "📋 REQUIRED FORMAT: For all legal responses, always provide: A summary of the facts of the case, Identification of legal issues, Step-by-step legal analysis, Reference to relevant laws (Acts, Sections, Articles), Mention of landmark cases and their citations, A well-structured judgment/conclusion, Citations of law commission reports, official gazettes, or legal commentaries where appropriate.",
                "🔍 RESEARCH: Pull factual and statutory data from Google API and authoritative legal websites like Indian Kanoon, SCC Online, Manupatra, Bar & Bench, LiveLaw.",
                "💼 PROFESSIONAL: Use clear, professional legal language, while ensuring simplicity and accessibility for users.",
                "⚖️ ACCURACY: Provide comprehensive yet concise explanations, ensuring every answer is backed by relevant authority and interpretation.",
                "🔒 ETHICS: Always ensure the output maintains legal accuracy, neutrality, and ethical standards.",
                "🧠 MEMORY: You are an intelligent AI assistant that remembers the ongoing chat context and refers to it when responding.",
                "🔄 CONTINUITY: Maintain continuity and coherence within the same chat session.",
                "❓ FOLLOW-UP: Understand follow-up questions based on earlier user inputs and your responses.",
                "🚫 NO REPEAT: Avoid repeating the same content unless requested.",
                "⚖️ LEGAL ONLY: Stay strictly within the context of legal consultation only - no exceptions.",
                f"Context from previous conversation: {context_prompt}" if context_prompt else ""
            ],
            tools=[DuckDuckGoTools()],
            show_tool_calls=False,
            markdown=True
        )
        
        return agent
    except Exception as e:
        st.error(f"Error creating legal agent: {str(e)}")
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
            try:
                agent = create_legal_agent(st.session_state.messages)
                if agent:
                    response = agent.run(prompt)
                    st.markdown(str(response.content))
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": str(response.content)})
                else:
                    st.error("Failed to create legal agent. Please try again.")
            except Exception as e:
                st.error(f"Error getting response: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Disclaimer:</strong> This application provides legal information for educational and informational purposes only. 
    It does not constitute legal advice and should not be relied upon as a substitute for consultation with a qualified attorney.</p>
</div>
""", unsafe_allow_html=True)
