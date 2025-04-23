import os
import streamlit as st
import numpy as np
import google.generativeai as genai
import uuid
import datetime
import json
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Custom CSS for a modern chat interface
def local_css():
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        background-color: #f9f9fc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat container styling */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Message styling */
    .stChatMessage {
        padding: 0.5rem 0;
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent"] {
        border-radius: 18px;
        padding: 0.8rem 1rem;
        line-height: 1.5;
    }
    
    /* User avatar */
    .stChatMessageAvatar {
        background-color: #1f75fe !important;
    }
    
    /* Assistant avatar */
    [data-testid="stChatMessageAvatar"][data-testid*="assistant"] {
        background-color: #10a37f !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e6e6e6;
        padding: 1rem;
    }
    
    /* Chat history item styling */
    .chat-history-item {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.2s;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .chat-history-item:hover {
        background-color: #f0f0f5;
    }
    
    .chat-history-active {
        background-color: #e6f0ff;
        border-left: 3px solid #1f75fe;
    }
    
    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 10px 15px;
        border: 1px solid #e0e0e0;
        background-color: #f9f9fc;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 20px;
        padding: 0.3rem 1rem;
        background-color: #1f75fe;
        color: white;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }
    
    /* Custom header */
    .custom-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .custom-header h1 {
        margin: 0;
        font-size: 1.8rem;
        color: #333;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        padding: 10px 15px;
        background-color: #f0f0f5;
        border-radius: 18px;
        width: fit-content;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        margin: 0 1px;
        background-color: #a0a0a0;
        border-radius: 50%;
        display: inline-block;
        animation: typing 1.4s infinite ease-in-out both;
    }
    
    .typing-indicator span:nth-child(1) {
        animation-delay: 0s;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0% { transform: scale(1); }
        50% { transform: scale(1.5); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chat_sessions' not in st.session_state:
        st.session_state.chat_sessions = {}
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = str(uuid.uuid4())
    if 'session_name' not in st.session_state:
        st.session_state.session_name = f"Chat {datetime.datetime.now().strftime('%b %d, %H:%M')}"

# Save and load chat sessions
def save_chat_session():
    if st.session_state.current_session_id:
        st.session_state.chat_sessions[st.session_state.current_session_id] = {
            "name": st.session_state.session_name,
            "messages": st.session_state.messages,
            "timestamp": datetime.datetime.now().isoformat()
        }

def load_chat_session(session_id):
    if session_id in st.session_state.chat_sessions:
        st.session_state.current_session_id = session_id
        st.session_state.messages = st.session_state.chat_sessions[session_id]["messages"]
        st.session_state.session_name = st.session_state.chat_sessions[session_id]["name"]

def create_new_chat():
    st.session_state.current_session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.session_name = f"Chat {datetime.datetime.now().strftime('%b %d, %H:%M')}"

# Configure Gemini and Groq models
def setup_models(groq_api_key, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_api_key
    )
    
    direct_prompt = PromptTemplate(
        input_variables=["question"],
        template="""
        Answer the question in detailed form.
        
        Question: {question}
        Answer:
        """
    )
    direct_chain = LLMChain(llm=llm, prompt=direct_prompt)
    
    search_prompt = PromptTemplate(
        input_variables=["web_results", "question"],
        template="""
        Use these web search results to give a comprehensive answer:
        
        Search Results:
        {web_results}
        
        Question: {question}
        Answer:
        """
    )
    search_chain = LLMChain(llm=llm, prompt=search_prompt)
    
    return direct_chain, search_chain

def get_gemini_model(name="gemini-1.5-pro"):
    return genai.GenerativeModel(name)

def gen_content(model, prompt, temperature=0.4, max_tokens=512):
    cfg = {"temperature": temperature, "top_p":1, "top_k":50, "max_output_tokens": max_tokens}
    safety = [{"category":c, "threshold":"BLOCK_NONE"} for c in [
        "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"
    ]]
    res = model.generate_content(prompt, generation_config=cfg, safety_settings=safety)
    return res.candidates[0].content.parts[0].text if res.candidates else ""

def decide_search(query: str):
    model = get_gemini_model()
    decision_prompt = f"Decide if this requires web search. If yes, reply '<SEARCH> keywords'. Otherwise 'NO_SEARCH'.\nQuery: {query}"
    response = gen_content(model, decision_prompt, max_tokens=32)
    if "<SEARCH>" in response:
        return True, response.split("<SEARCH>")[1].strip()
    return False, None

@st.cache_data
def perform_search(keywords: str) -> str:
    return DuckDuckGoSearchRun().run(keywords)

# Main application
def main():
    # Page configuration
    st.set_page_config(
        page_title="General Knowledge Assistant", 
        page_icon="🧭", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    local_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar: API keys and chat history
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🧭 Knowledge Assistant</h2>", unsafe_allow_html=True)
        
        # API Key inputs
        st.subheader("🔑 API Keys")
        groq_api_key = os.environ.get("GROQ_API_KEY") or st.text_input("Groq API Key", type="password")
        gemini_api_key = os.environ.get("GEMINI_API_KEY") or st.text_input("Gemini API Key", type="password")
        
        if not groq_api_key or not gemini_api_key:
            st.warning("Please provide both API keys to proceed.")
            st.stop()
        
        # Chat history management
        st.subheader("💬 Chat History")
        
        # New chat button
        if st.button("➕ New Chat", key="new_chat"):
            create_new_chat()
        
        # Current chat name editor
        new_name = st.text_input("Chat Name", value=st.session_state.session_name)
        if new_name != st.session_state.session_name:
            st.session_state.session_name = new_name
            save_chat_session()
        
        # Display chat history
        st.markdown("#### Previous Chats")
        
        # Sort sessions by timestamp (newest first)
        sorted_sessions = sorted(
            st.session_state.chat_sessions.items(),
            key=lambda x: x[1].get("timestamp", ""),
            reverse=True
        )
        
        for session_id, session in sorted_sessions:
            # Display first message or default text
            preview = "New conversation"
            if session["messages"] and len(session["messages"]) > 0:
                first_msg = session["messages"][0]
                if isinstance(first_msg, dict) and "content" in first_msg:
                    preview = first_msg["content"]
                elif isinstance(first_msg, (list, tuple)) and len(first_msg) > 1:
                    preview = first_msg[1]  # Assuming content is at index 1
                
                if len(preview) > 30:
                    preview = preview[:30] + "..."
            
            # Highlight current session
            is_current = session_id == st.session_state.current_session_id
            style = "chat-history-item chat-history-active" if is_current else "chat-history-item"
            
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                if st.button(session["name"], key=f"load_session_{session_id}"):
                    load_chat_session(session_id)
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{session_id}", help="Delete this chat"):
                    if session_id in st.session_state.chat_sessions:
                        del st.session_state.chat_sessions[session_id]
                        if session_id == st.session_state.current_session_id:
                            create_new_chat()
                        st.rerun()
    
    # Main chat interface
    direct_chain, search_chain = setup_models(groq_api_key, gemini_api_key)
    
    # Custom header with logo and title
    st.markdown("""
    <div class="custom-header">
        <h1>🧭 General Knowledge Assistant</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    # Chat input area (placed before displaying messages for better UX)
    user_input = st.chat_input("Ask me anything...")
    
    # Process user input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Save current state
        save_chat_session()
        
        # Show typing indicator
        with chat_container:
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """, unsafe_allow_html=True)
        
        # Process the query
        try:
            # Determine need for search
            needs_search, terms = decide_search(user_input)
            
            if needs_search:
                web_results = perform_search(terms)
                answer = search_chain.run({"web_results": web_results, "question": user_input})
            else:
                answer = direct_chain.run({"question": user_input})
            
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            
            save_chat_session()
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            save_chat_session()
        
        # Remove typing indicator
        typing_placeholder.empty()
        st.rerun()
    
    # Display chat messages
    with chat_container:
        if not st.session_state.messages:
            st.markdown("""
            <div style="text-align: center; padding: 50px 20px;">
                <h3>👋 Welcome to the General Knowledge Assistant!</h3>
                <p>Ask me anything about general knowledge, facts, or concepts.</p>
                <p>I can search the web when needed to provide you with up-to-date information.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display all messages
            for msg in st.session_state.messages:
                # Ensure we're handling the message correctly based on its type
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])
                else:
                    st.error(f"Invalid message format: {msg}")

if __name__ == "__main__":
    main()
