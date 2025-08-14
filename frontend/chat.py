import streamlit as st
import requests
import uuid
import streamlit.components.v1 as components
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Bank of Ceylon - Virtual Assistant", 
    page_icon="🏦", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hello! I'm your Bank of Ceylon virtual assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M")
    }]

# API Configuration
BASE_URL = 'http://127.0.0.1:8000'
OPENAI_RESPONSE_URL = f"{BASE_URL}/query"
SESSION_DELETE_URL = f"{BASE_URL}/history/{st.session_state.session_id}"

# Session cleanup on window close
delete_session_js = f"""
<script>
window.addEventListener('beforeunload', function (e) {{
    fetch('{SESSION_DELETE_URL}', {{
        method: 'DELETE'
    }});
}});
</script>
"""
components.html(delete_session_js, height=0, width=0)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom header */
    .boc-header {
        background: linear-gradient(135deg, #FDBE10 0%, #C69C05 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .boc-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .boc-subtitle {
        color: #e0e7ff;
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #FDBE10 0%, #D4A017 100%);
        color: black;
        padding: 1rem 1.2rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem auto;
        max-width: 80%;
        width: fit-content;
        margin-left: auto;
        display: block;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #374151;
        padding: 1rem 1.2rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem auto 1rem 0;
        max-width: 80%;
        width: fit-content;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .message-time {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Quick actions */
    .quick-actions {
        background: transparent;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
    }
    
    /* Input styling */
    .stChatInput {
        border-radius: 25px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #FDBE10 0%, #D4A017 100%);
        color: black;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem;
        color: #6b7280;
    }
    
    .typing-dots {
        display: inline-flex;
        margin-left: 10px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #9ca3af;
        display: inline-block;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out both;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0);
        } 40% {
            transform: scale(1);
        }
    }
    
    /* Status indicator */
    .status-online {
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Functions
def start_new_chat():
    try:
        requests.delete(SESSION_DELETE_URL, timeout=5)
    except:
        pass
    st.session_state.session_id = str(uuid.uuid4())
    clear_chat_history()
    st.rerun()

def get_response(session_id, user_input):
    try:
        payload = {"session_id": session_id, "input": user_input}
        response = requests.post(OPENAI_RESPONSE_URL, json=payload, timeout=30)
        return response.json().get("answer", "I apologize, but I'm having trouble processing your request right now. Please try again.")
    except requests.exceptions.Timeout:
        return "I'm taking longer than usual to respond. Please try asking your question again."
    except requests.exceptions.ConnectionError:
        return "I'm currently unable to connect to the server. Please check your connection and try again."
    except Exception as e:
        return "I encountered an error while processing your request. Please try again or contact support if the issue persists."

def clear_chat_history():
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hello! I'm your Bank of Ceylon virtual assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M")
    }]

def add_message(role, content):
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    st.session_state.messages.append(message)

# Header
st.markdown("""
<div class="boc-header">
    <h1 class="boc-title">🏦 Bank of Ceylon</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Chat Controls")
    
    # Status indicator
    st.markdown("""
    <div style="margin: 1rem 0;">
        <span class="status-online"></span>
        <span style="color: #10b981; font-weight: 600;">Online</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('New Chat', use_container_width=True):
            start_new_chat()
    with col2:
        if st.button('Clear Chat', use_container_width=True):
            clear_chat_history()
            st.rerun()
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    quick_actions = [
    "Open an account with Bank of Ceylon?",
    "Contact Bank of Ceylon customer service?",
    "Register for BOC Smart Online Banking",
    "How often should I change my password?",
    "Who can apply for a Credit Card?",
    "Is SmartPay only for QR payments?",
    "Access BOC WhatsApp banking",
    "Can I change my PIN?",
    "Check my credit card account balance",
    "My credit card is lost or stolen?"
    ]
    
    for action in quick_actions:
        if st.button(f"{action}", use_container_width=True, key=f"quick_{action}"):
            add_message("user", action)

            session_id = st.session_state.session_id
            response = get_response(session_id, action)

            if isinstance(response, list):
                full_response = ''.join(response)
            else:
                full_response = str(response)

            add_message("assistant", full_response)

            st.rerun()

# Main chat area
chat_col1, chat_col2, chat_col3 = st.columns([1, 10, 1])

with chat_col2:
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    {message["content"]}
                    <div class="message-time">{message["timestamp"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    {message["content"]}
                    <div class="message-time">BOC Assistant • {message["timestamp"]}</div>
                </div>
                """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message here...", key="user_input"):
    # Add user message
    add_message("user", prompt)
    
    # Show typing indicator
    with st.spinner(""):
        # Get response
        session_id = st.session_state.session_id
        response = get_response(session_id, prompt)
        
        # Handle response
        if isinstance(response, list):
            full_response = ''.join(response)
        else:
            full_response = str(response)
        
        # Add assistant response
        add_message("assistant", full_response)
    
    # Rerun to update the chat
    st.rerun()