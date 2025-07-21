import streamlit as st
import google.generativeai as genai
import os
import time
from googletrans import Translator

# Load environment variables and configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("⚠️ GEMINI_API_KEY not found. Please add your API key to continue.")
    st.stop()

# Streamlit UI setup
st.set_page_config(
    page_title="Saanchari-Andhra Pradesh Tourism Chatbot", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        /* Main layout styling */
        .main-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 1rem;
            border-bottom: 2px solid #07546B;
        }
        
        /* Language selector styling (right side) */
        .lang-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            justify-content: flex-end;
        }
        
        .lang-select {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 0.3rem 0.6rem;
            min-width: 120px;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Title styling (left side) */
        .title-container {
            text-align: left;
        }
        
        .main-title {
            font-size: 2.2rem;
            font-weight: bold;
            color: #07546B;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        /* Chat container styling */
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 1rem;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background: #fafafa;
            margin-bottom: 1rem;
        }
        
        /* Avatar styling */
        .chat-message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1.2rem;
            gap: 0.5rem;
            animation: fadeIn 0.3s ease-in-out;
        }
        
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }
        
        .user-avatar {
            background: #007bff;
            color: white;
        }
        
        .bot-avatar {
            background: #28a745;
            color: white;
        }
        
        .message-content {
            flex: 1;
            padding: 0.8rem 1rem;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        
        .bot-message {
            background: #f1f8e9;
            border-left: 4px solid #4caf50;
        }
        
        /* Typing indicator */
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.8rem 1rem;
            background: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .typing-dots {
            display: flex;
            gap: 0.2rem;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #6c757d;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typingAnimation {
            0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
            40% { opacity: 1; transform: scale(1); }
        }
        
        /* Quick questions styling */
        .quick-questions {
            margin: 1.5rem 0;
        }
        
        .question-btn {
            margin: 0.25rem;
            padding: 0.5rem 1rem;
            border: 1px solid #07546B;
            border-radius: 20px;
            background: white;
            color: #07546B;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .question-btn:hover {
            background: #07546B;
            color: white;
        }
        
        /* Footer styling */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-top: 1px solid #e0e0e0;
            padding: 0.5rem;
            text-align: center;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        
        /* Blinking cursor animation */
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        /* Enhanced scrollbar for chat container */
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: #07546B;
            border-radius: 4px;
        }
        
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: #054152;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Language selector improvements */
        .stSelectbox > div > div {
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
    </style>
""", unsafe_allow_html=True)

# Language mapping
lang_map = {
    "English": "en",
    "Hindi": "hi", 
    "Telugu": "te"
}

# Initialize translator
translator = Translator()

# Header layout with title on left and language selector on right
header_left, header_right = st.columns([2, 1])

with header_left:
    st.markdown("""
        <div class='title-container'>
            <h1 class='main-title'>🗺️ Saanchari Chatbot</h1>
            <p style='color: #666; margin: 0; text-align: left;'>Your Andhra Pradesh Tourism Guide</p>
        </div>
    """, unsafe_allow_html=True)

with header_right:
    st.markdown("<div class='lang-container'>", unsafe_allow_html=True)
    st.markdown("**🌐 Language:**")
    selected_lang = st.selectbox(
        "Select Language", 
        list(lang_map.keys()), 
        index=0, 
        label_visibility="collapsed",
        key="language_selector"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Built-in questions (2 in English + 1 in Telugu)
builtin_questions = [
    "What are the top tourist attractions in Andhra Pradesh?",
    "Tell me about the famous food in Andhra Pradesh.", 
    "ఆంధ్రప్రదేశ్‌లో ప్రసిద్ధ ఆహారం గురించి చెప్పండి"  # Telugu: Tell me about famous food in Andhra Pradesh
]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# Quick Questions section
st.markdown("<div class='quick-questions'>", unsafe_allow_html=True)
st.subheader("🚀 Quick Questions")
cols = st.columns(len(builtin_questions))
for i, question in enumerate(builtin_questions):
    if cols[i].button(f"❓ {question[:30]}...", key=f"q_{i}", help=question):
        st.session_state.messages.append({"role": "user", "content": question})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Display chat history
chat_placeholder = st.empty()

def display_chat_history():
    chat_html = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_html += f"""
                <div class='chat-message'>
                    <div class='avatar user-avatar'>👤</div>
                    <div class='message-content user-message'>
                        {message['content']}
                    </div>
                </div>
            """
        else:
            chat_html += f"""
                <div class='chat-message'>
                    <div class='avatar bot-avatar'>🤖</div>
                    <div class='message-content bot-message'>
                        {message['content']}
                    </div>
                </div>
            """
    return chat_html

# Display existing messages in scrollable container
st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)
with chat_placeholder.container():
    st.markdown(display_chat_history(), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# System prompt for tourism queries
SYSTEM_PROMPT = (
    "You are an expert on Andhra Pradesh tourism, culture, and cuisine. "
    "Provide detailed, helpful information about tourist destinations, food, culture, "
    "transportation, accommodation, and travel tips for Andhra Pradesh. "
    "Be enthusiastic and informative in your responses. "
    "When discussing food, include regional specialties and where to find them."
)

def stream_text_response(text, chat_placeholder, delay=0.05):
    """Stream text word by word with realistic typing effect"""
    words = text.split()
    displayed_text = ""
    
    # Show typing indicator first
    typing_html = display_chat_history() + """
        <div class='chat-message'>
            <div class='avatar bot-avatar'>🤖</div>
            <div class='typing-indicator'>
                <span>Saanchari is typing</span>
                <div class='typing-dots'>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                </div>
            </div>
        </div>
    """
    chat_placeholder.markdown(typing_html, unsafe_allow_html=True)
    time.sleep(1.5)  # Show typing indicator
    
    # Stream words one by one
    for i, word in enumerate(words):
        displayed_text += word + " "
        
        # Create streaming message HTML with cursor
        streaming_message_html = f"""
            <div class='chat-message'>
                <div class='avatar bot-avatar'>🤖</div>
                <div class='message-content bot-message'>
                    {displayed_text}<span style='animation: blink 1s infinite;'>▋</span>
                </div>
            </div>
        """
        
        # Combine with existing chat history
        full_chat_html = display_chat_history() + streaming_message_html
        chat_placeholder.markdown(full_chat_html, unsafe_allow_html=True)
        
        # Variable delay for more natural typing
        word_delay = delay + (0.01 if len(word) > 6 else 0)
        time.sleep(word_delay)
    
    # Return final text without cursor
    return displayed_text.strip()

# Chat input
if prompt := st.chat_input("Ask me anything about Andhra Pradesh tourism... 🏛️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Generate response for new user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.is_generating:
    st.session_state.is_generating = True
    
    try:
        user_prompt = st.session_state.messages[-1]["content"]
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser question: {user_prompt}"
        
        response = model.generate_content(full_prompt)
        reply = response.text.strip()
        
        # Translate reply if needed
        if lang_map[selected_lang] != "en":
            reply = translator.translate(reply, dest=lang_map[selected_lang]).text
        
        # Stream the response word by word
        final_reply = stream_text_response(reply, chat_placeholder)
        
        # Add to session state
        st.session_state.messages.append({"role": "assistant", "content": final_reply})
        
    except Exception as e:
        error_msg = f"⚠️ Sorry, I encountered an error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    finally:
        st.session_state.is_generating = False
        # Final display of complete chat
        with chat_placeholder.container():
            st.markdown(display_chat_history(), unsafe_allow_html=True)

# Add some spacing for the footer
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Sticky footer
st.markdown("""
<div class='footer'>
    <small style='color: #07546B;'>
        © 2025 Kshipani Tech Ventures Pvt Ltd. All rights reserved. | 
        Powered by Gemini AI 🤖
    </small>
</div>
""", unsafe_allow_html=True)

# Enhanced Auto-scroll JavaScript
st.markdown("""
<script>
    // Enhanced scroll function with smooth animation
    function smoothScrollToBottom() {
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
    
    // Initialize scroll functionality
    function initializeScrolling() {
        const chatContainer = document.querySelector('.chat-container');
        if (!chatContainer) {
            setTimeout(initializeScrolling, 100);
            return;
        }
        
        // Scroll to bottom initially
        setTimeout(smoothScrollToBottom, 300);
        
        // Observer for new content
        const observer = new MutationObserver(function(mutations) {
            let shouldScroll = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    shouldScroll = true;
                }
            });
            
            if (shouldScroll) {
                setTimeout(smoothScrollToBottom, 50);
            }
        });
        
        // Observe chat container for changes
        observer.observe(chatContainer, { 
            childList: true, 
            subtree: true 
        });
        
        // Also observe parent containers
        const mainContainer = document.querySelector('[data-testid="stVerticalBlock"]');
        if (mainContainer) {
            observer.observe(mainContainer, { 
                childList: true, 
                subtree: true 
            });
        }
    }
    
    // Start initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeScrolling);
    } else {
        initializeScrolling();
    }
    
    // Backup scroll triggers
    setTimeout(smoothScrollToBottom, 1000);
    setInterval(function() {
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer && chatContainer.children.length > 0) {
            const lastChild = chatContainer.lastElementChild;
            if (lastChild && !lastChild.dataset.scrolled) {
                smoothScrollToBottom();
                lastChild.dataset.scrolled = 'true';
            }
        }
    }, 500);
</script>
""", unsafe_allow_html=True)