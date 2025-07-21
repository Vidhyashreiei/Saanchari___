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

# Brand colors from your color scheme
# F75768 (Pink), FB6957 (Orange), 07546B (Teal), CFD1D1 (Light Gray)

st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global app styling */
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Header with brand gradient */
        .brand-header {
            background: linear-gradient(135deg, #F75768 0%, #FB6957 30%, #07546B 100%);
            padding: 2rem 0;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 25px 25px;
            box-shadow: 0 8px 32px rgba(7, 84, 107, 0.2);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Title styling */
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, white 0%, #CFD1D1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.2rem;
            font-weight: 400;
            margin: 0.5rem 0 0 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Language selector styling */
        .lang-section {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 0.5rem;
        }
        
        .lang-label {
            color: white;
            font-weight: 500;
            font-size: 1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.95);
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            font-weight: 500;
            min-width: 140px;
        }
        
        /* Quick questions with brand colors */
        .quick-questions {
            max-width: 900px;
            margin: 0 auto 3rem auto;
            padding: 0 1rem;
        }
        
        .questions-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #07546B;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .question-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .question-card {
            background: linear-gradient(135deg, rgba(251, 105, 87, 0.1) 0%, rgba(7, 84, 107, 0.1) 100%);
            border: 2px solid rgba(7, 84, 107, 0.2);
            border-radius: 15px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            font-weight: 500;
            color: #07546B;
        }
        
        .question-card:hover {
            background: linear-gradient(135deg, #F75768 0%, #FB6957 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(247, 87, 104, 0.3);
            border-color: transparent;
        }
        
        /* ChatGPT-like message styling - NO CONTAINER */
        .chat-area {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .message-wrapper {
            margin-bottom: 2rem;
            width: 100%;
        }
        
        .message-container {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            max-width: 100%;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .user-avatar {
            background: linear-gradient(135deg, #F75768 0%, #FB6957 100%);
            color: white;
        }
        
        .bot-avatar {
            background: linear-gradient(135deg, #07546B 0%, #0a6b85 100%);
            color: white;
        }
        
        .message-content {
            flex: 1;
            padding: 1.2rem 1.5rem;
            border-radius: 18px;
            font-size: 1rem;
            line-height: 1.6;
            max-width: calc(100% - 60px);
        }
        
        .user-message {
            background: linear-gradient(135deg, rgba(247, 87, 104, 0.1) 0%, rgba(251, 105, 87, 0.1) 100%);
            border: 1px solid rgba(247, 87, 104, 0.2);
            color: #2c3e50;
        }
        
        .bot-message {
            background: linear-gradient(135deg, rgba(7, 84, 107, 0.05) 0%, rgba(207, 209, 209, 0.1) 100%);
            border: 1px solid rgba(7, 84, 107, 0.15);
            color: #2c3e50;
        }
        
        /* Typing indicator */
        .typing-container {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .typing-indicator {
            background: linear-gradient(135deg, rgba(7, 84, 107, 0.1) 0%, rgba(207, 209, 209, 0.2) 100%);
            border: 1px solid rgba(7, 84, 107, 0.15);
            border-radius: 18px;
            padding: 1.2rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            color: #07546B;
            font-weight: 500;
        }
        
        .typing-dots {
            display: flex;
            gap: 0.3rem;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #07546B;
            animation: typingPulse 1.5s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        .typing-dot:nth-child(3) { animation-delay: 0s; }
        
        @keyframes typingPulse {
            0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
            40% { opacity: 1; transform: scale(1.2); }
        }
        
        /* Blinking cursor */
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .typing-cursor {
            color: #07546B;
            font-weight: bold;
        }
        
        /* Enhanced chat input */
        .stChatInput > div {
            background: white;
            border: 2px solid rgba(7, 84, 107, 0.2);
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .stChatInput > div:focus-within {
            border-color: #F75768;
            box-shadow: 0 4px 20px rgba(247, 87, 104, 0.2);
        }
        
        /* Footer */
        .brand-footer {
            background: linear-gradient(90deg, #F75768 0%, #FB6957 50%, #07546B 100%);
            color: white;
            text-align: center;
            padding: 1.5rem;
            margin: 3rem -1rem -1rem -1rem;
            border-radius: 25px 25px 0 0;
            font-weight: 500;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Smooth animations */
        .message-wrapper {
            animation: slideIn 0.4s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 1.5rem;
                text-align: center;
            }
            
            .main-title {
                font-size: 2.2rem;
            }
            
            .question-grid {
                grid-template-columns: 1fr;
            }
            
            .message-content {
                padding: 1rem;
                font-size: 0.95rem;
            }
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

# Brand Header
st.markdown("""
    <div class='brand-header'>
        <div class='header-content'>
            <div>
                <h1 class='main-title'>🗺️ Saanchari Chatbot</h1>
                <p class='subtitle'>Your Intelligent Andhra Pradesh Tourism Guide</p>
            </div>
            <div class='lang-section'>
                <div class='lang-label'>🌐 Choose Language</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Language selector (positioned after header for proper styling)
selected_lang = st.selectbox(
    "Select Language", 
    list(lang_map.keys()), 
    index=0, 
    label_visibility="collapsed",
    key="language_selector"
)

# Built-in questions with interactive cards
builtin_questions = [
    "What are the top tourist attractions in Andhra Pradesh?",
    "Tell me about the famous food in Andhra Pradesh.", 
    "ఆంధ్రప్రదేశ్‌లో ప్రసిద్ధ ఆహారం గురించి చెప్పండి"  # Telugu
]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# Interactive Quick Questions
st.markdown("<div class='quick-questions'>", unsafe_allow_html=True)
st.markdown("<h2 class='questions-title'>🚀 Explore Andhra Pradesh</h2>", unsafe_allow_html=True)

cols = st.columns(len(builtin_questions))
for i, question in enumerate(builtin_questions):
    with cols[i]:
        if st.button(
            question, 
            key=f"q_{i}", 
            use_container_width=True,
            help=f"Ask: {question}"
        ):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Chat Area (ChatGPT-like, no container box)
st.markdown("<div class='chat-area'>", unsafe_allow_html=True)

def display_message(role, content, is_streaming=False):
    avatar_class = "user-avatar" if role == "user" else "bot-avatar"
    message_class = "user-message" if role == "user" else "bot-message"
    avatar_icon = "👤" if role == "user" else "🤖"
    
    cursor = "<span class='typing-cursor' style='animation: blink 1s infinite;'>▋</span>" if is_streaming else ""
    
    return f"""
        <div class='message-wrapper'>
            <div class='message-container'>
                <div class='message-avatar {avatar_class}'>{avatar_icon}</div>
                <div class='message-content {message_class}'>
                    {content}{cursor}
                </div>
            </div>
        </div>
    """

def display_typing_indicator():
    return """
        <div class='typing-container'>
            <div class='message-avatar bot-avatar'>🤖</div>
            <div class='typing-indicator'>
                <span>Saanchari is thinking</span>
                <div class='typing-dots'>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                    <div class='typing-dot'></div>
                </div>
            </div>
        </div>
    """

# Display all messages
chat_html = ""
for message in st.session_state.messages:
    chat_html += display_message(message["role"], message["content"])

chat_placeholder = st.empty()
chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# System prompt
SYSTEM_PROMPT = (
    "You are Saanchari, an expert AI guide for Andhra Pradesh tourism, culture, and cuisine. "
    "Provide detailed, helpful, and enthusiastic information about tourist destinations, food, culture, "
    "transportation, accommodation, and travel tips for Andhra Pradesh. "
    "Be conversational, friendly, and informative in your responses. "
    "When discussing food, include regional specialties and where to find them."
)

def stream_response(text, delay=0.04):
    """Stream text word by word with realistic typing effect"""
    words = text.split()
    displayed_text = ""
    
    # Show typing indicator first
    typing_html = chat_html + display_typing_indicator()
    chat_placeholder.markdown(typing_html, unsafe_allow_html=True)
    time.sleep(1.2)
    
    # Stream words one by one
    for word in words:
        displayed_text += word + " "
        
        # Update with streaming message
        streaming_html = chat_html + display_message("assistant", displayed_text, is_streaming=True)
        chat_placeholder.markdown(streaming_html, unsafe_allow_html=True)
        
        time.sleep(delay + (0.01 if len(word) > 6 else 0))
    
    return displayed_text.strip()

# Chat input
if prompt := st.chat_input("Ask me anything about Andhra Pradesh tourism... 🏛️"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Generate response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and not st.session_state.is_generating:
    st.session_state.is_generating = True
    
    try:
        user_prompt = st.session_state.messages[-1]["content"]
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser question: {user_prompt}"
        
        response = model.generate_content(full_prompt)
        reply = response.text.strip()
        
        # Translate if needed
        if lang_map[selected_lang] != "en":
            reply = translator.translate(reply, dest=lang_map[selected_lang]).text
        
        # Stream the response
        final_reply = stream_response(reply)
        
        # Add to session state
        st.session_state.messages.append({"role": "assistant", "content": final_reply})
        
    except Exception as e:
        error_msg = f"⚠️ Sorry, I encountered an error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    finally:
        st.session_state.is_generating = False
        # Final display
        final_chat_html = ""
        for message in st.session_state.messages:
            final_chat_html += display_message(message["role"], message["content"])
        chat_placeholder.markdown(final_chat_html, unsafe_allow_html=True)

# Brand Footer
st.markdown("""
    <div class='brand-footer'>
        © 2025 Kshipani Tech Ventures Pvt Ltd. All rights reserved. | 
        Powered by Gemini AI 🤖 | Designed with ❤️ for Andhra Pradesh
    </div>
""", unsafe_allow_html=True)