#This File consist of Frontend in streamlit
import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# Page setting
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utility functions
def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id, f"New Chat {len(st.session_state['chat_threads'])+1}")
    st.session_state['message_history'] = []
    st.rerun()

def add_thread(thread_id, name="New Chat"):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = {
            "name": name,
            "editing": False
        }

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# Setup session
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {}

add_thread(st.session_state['thread_id'], "New Chat 1")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main {
    background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
    padding: 0 !important;
}

.stMain {
    background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar toggle button - make it visible and styled */
button[kind="header"] {
    visibility: visible !important;
    display: block !important;
    opacity: 1 !important;
    z-index: 999999 !important;
    position: fixed !important;
    left: 0 !important;
}

section[data-testid="stSidebar"] button[kind="header"] {
    background: #1f2937 !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 0.5rem !important;
    transition: all 0.3s ease !important;
}

section[data-testid="stSidebar"] button[kind="header"]:hover {
    background: #374151 !important;
    transform: translateX(3px) !important;
}

/* Ensure collapsed sidebar toggle button is always visible */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: block !important;
    opacity: 1 !important;
    z-index: 999999 !important;
    position: fixed !important;
    left: 0 !important;
    top: 0.5rem !important;
}

[data-testid="collapsedControl"] button {
    background: #1f2937 !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 0.5rem !important;
    visibility: visible !important;
    display: block !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent;
    padding-top: 2rem;
}

[data-testid="stSidebar"] h1 {
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
    padding: 1rem 1rem 0.5rem 1rem;
    margin: 0;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] h2 {
    color: #9ca3af;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 1.5rem 1rem 0.5rem 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.75rem 1rem;
    margin: 0 1rem 1rem 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

[data-testid="stSidebar"] button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
}

[data-testid="stSidebar"] .element-container {
    padding: 0 0.5rem;
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent;
    color: #e5e7eb;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 0.3rem;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(4px);
}

[data-testid="stSidebar"] button[kind="primary"][key^="btn_"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    border: none !important;
}

/* Fixed alignment for edit and delete buttons */
[data-testid="stSidebar"] button[key^="edit_"],
[data-testid="stSidebar"] button[key^="delete_"] {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #9ca3af !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 0 !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    width: 36px !important;
    height: 36px !important;
    min-height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
}

[data-testid="stSidebar"] button[key^="edit_"]:hover {
    background: rgba(59, 130, 246, 0.2) !important;
    color: #60a5fa !important;
    border-color: #3b82f6 !important;
    transform: scale(1.1) !important;
}

[data-testid="stSidebar"] button[key^="delete_"]:hover {
    background: rgba(239, 68, 68, 0.2) !important;
    color: #f87171 !important;
    border-color: #ef4444 !important;
    transform: scale(1.1) !important;
}

[data-testid="stSidebar"] button[key^="save_"] {
    background: rgba(34, 197, 94, 0.2);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] button[key^="save_"]:hover {
    background: rgba(34, 197, 94, 0.3);
    transform: scale(1.02);
}

[data-testid="stSidebar"] input {
    background: rgba(255, 255, 255, 0.08);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 0.6rem;
    font-size: 0.9rem;
}

[data-testid="stSidebar"] input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    outline: none;
}

/* Column alignment fix */
[data-testid="stSidebar"] [data-testid="column"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.stChatMessage {
    background: transparent !important;
    padding: 0.8rem 1.5rem !important;
    margin-bottom: 1rem !important;
    border: none !important;
    box-shadow: none !important;
}

.stChatMessage[data-testid="user-message"] {
    background: transparent !important;
}

.stChatMessage[data-testid="user-message"] > div {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 18px 18px 4px 18px;
    padding: 1rem 1.25rem;
    margin-left: auto;
    margin-right: 1rem;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.stChatMessage[data-testid="assistant-message"] {
    background: transparent !important;
}

.stChatMessage[data-testid="assistant-message"] > div {
    background: #1f2937;
    border-radius: 18px 18px 18px 4px;
    padding: 1rem 1.25rem;
    margin-left: 1rem;
    margin-right: auto;
    max-width: 70%;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.stChatMessage p {
    color: #ffffff !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
    font-weight: 400 !important;
}

.stChatMessage > div > div:first-child {
    margin-top: 0.5rem;
}

.stChatMessage img {
    border-radius: 50% !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
}

.stChatInput {
    position: fixed !important;
    bottom: 0 !important;
    left: 260px !important;
    right: 0 !important;
    background: #0d1117 !important;
    padding: 1rem 2rem 1.5rem 2rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    z-index: 1000 !important;
    transition: left 0.3s ease !important;
}

.stChatInput > div {
    max-width: 900px !important;
    margin: 0 auto !important;
}

.stChatInput input {
    background: #1f2937 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 24px !important;
    padding: 0.9rem 3rem 0.9rem 1.5rem !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stChatInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    outline: none !important;
}

.stChatInput input::placeholder {
    color: #6b7280 !important;
}

.stChatInput button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    position: absolute !important;
    right: 0.4rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    transition: all 0.2s ease !important;
}

.stChatInput button:hover {
    transform: translateY(-50%) scale(1.1) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5) !important;
}

.welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    padding: 2rem;
}

.welcome-icon {
    font-size: 5rem;
    margin-bottom: 1.5rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

.welcome-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.welcome-message {
    font-size: 1.3rem;
    color: #e5e7eb;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.welcome-subtitle {
    font-size: 1rem;
    color: #9ca3af;
    margin-top: 0.5rem;
}

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}

.main > div {
    padding-bottom: 100px !important;
}

@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 100% !important;
        max-width: 280px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        max-width: 280px !important;
    }
    
    .stChatInput {
        left: 0 !important;
        padding: 0.8rem 1rem 1rem 1rem !important;
    }
    
    .stChatInput input {
        padding: 0.75rem 3rem 0.75rem 1rem !important;
        font-size: 0.9rem !important;
    }
    
    .stChatInput button {
        width: 36px !important;
        height: 36px !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div,
    .stChatMessage[data-testid="assistant-message"] > div {
        max-width: 85% !important;
        padding: 0.9rem 1rem !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div {
        margin-right: 0.5rem !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] > div {
        margin-left: 0.5rem !important;
    }
    
    .welcome-icon {
        font-size: 3.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .welcome-title {
        font-size: 1.8rem !important;
    }
    
    .welcome-message {
        font-size: 1.1rem !important;
    }
    
    .welcome-subtitle {
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.3rem !important;
        padding: 0.8rem 0.8rem 0.4rem 0.8rem !important;
    }
    
    [data-testid="stSidebar"] h2 {
        font-size: 0.7rem !important;
        margin: 1rem 0.8rem 0.4rem 0.8rem !important;
    }
    
    [data-testid="stSidebar"] button[kind="primary"] {
        margin: 0 0.8rem 0.8rem 0.8rem !important;
        padding: 0.65rem 0.8rem !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSidebar"] button[kind="secondary"] {
        padding: 0.7rem 0.8rem !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSidebar"] button[key^="edit_"],
    [data-testid="stSidebar"] button[key^="delete_"] {
        width: 32px !important;
        height: 32px !important;
        min-height: 32px !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0 0.15rem !important;
    }
}

@media (max-width: 480px) {
    .stChatInput input {
        padding: 0.65rem 2.8rem 0.65rem 0.9rem !important;
        font-size: 0.85rem !important;
        border-radius: 20px !important;
    }
    
    .stChatInput button {
        width: 32px !important;
        height: 32px !important;
        right: 0.3rem !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div,
    .stChatMessage[data-testid="assistant-message"] > div {
        max-width: 90% !important;
        padding: 0.8rem 0.9rem !important;
        font-size: 0.9rem !important;
    }
    
    .welcome-icon {
        font-size: 3rem !important;
    }
    
    .welcome-title {
        font-size: 1.5rem !important;
    }
    
    .welcome-message {
        font-size: 1rem !important;
    }
    
    .welcome-subtitle {
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSidebar"] button[key^="edit_"],
    [data-testid="stSidebar"] button[key^="delete_"] {
        width: 30px !important;
        height: 30px !important;
        min-height: 30px !important;
        font-size: 0.85rem !important;
    }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .stChatInput {
        left: 280px !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div,
    .stChatMessage[data-testid="assistant-message"] > div {
        max-width: 75% !important;
    }
}

@media (min-width: 1025px) and (max-width: 1440px) {
    .stChatInput > div {
        max-width: 800px !important;
    }
}

@media (min-width: 1441px) {
    .stChatInput > div {
        max-width: 1000px !important;
    }
    
    .stChatMessage[data-testid="user-message"] > div,
    .stChatMessage[data-testid="assistant-message"] > div {
        max-width: 65% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# JavaScript to clear browser state and ensure sidebar is always expanded on rerun
st.markdown("""
<script>
// Clear Streamlit's session storage to reset sidebar state
window.addEventListener('load', function() {
    // Clear session storage that Streamlit uses to remember sidebar state
    try {
        sessionStorage.clear();
    } catch(e) {
        console.log('Could not clear session storage:', e);
    }
    
    // Function to make toggle button visible and ensure sidebar is expanded
    function ensureToggleVisible() {
        // Find all buttons with kind="header" (sidebar toggle)
        const toggleButtons = document.querySelectorAll('button[kind="header"]');
        toggleButtons.forEach(btn => {
            btn.style.visibility = 'visible';
            btn.style.display = 'block';
            btn.style.opacity = '1';
            btn.style.zIndex = '999999';
        });
        
        // Find collapsed control
        const collapsedControl = document.querySelector('[data-testid="collapsedControl"]');
        if (collapsedControl) {
            collapsedControl.style.visibility = 'visible';
            collapsedControl.style.display = 'block';
            collapsedControl.style.opacity = '1';
            collapsedControl.style.zIndex = '999999';
        }
        
        // Ensure sidebar is expanded
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.setAttribute('aria-expanded', 'true');
        }
    }
    
    // Run immediately
    ensureToggleVisible();
    
    // Run every 500ms to catch any dynamically added elements
    setInterval(ensureToggleVisible, 500);
    
    // Also run on any DOM mutations
    const observer = new MutationObserver(ensureToggleVisible);
    observer.observe(document.body, { childList: true, subtree: true });
});
</script>
""", unsafe_allow_html=True)

# Sidebar UI
with st.sidebar:
    st.title('🤖 AI Chatbot')
    
    if st.button('➕ New Chat', use_container_width=True, type="primary"):
        reset_chat()
    
    st.header('💬 My Conversations')
    
    for thread_id, thread_info in list(st.session_state['chat_threads'].items())[::-1]:
        col1, col2, col3 = st.columns([0.70, 0.15, 0.15], gap="small")
        
        with col1:
            if thread_info["editing"]:
                new_name = st.text_input(
                    "Rename",
                    value=thread_info["name"],
                    key=f"rename_{thread_id}",
                    label_visibility="collapsed"
                )
                if st.button("💾", key=f"save_{thread_id}", use_container_width=True):
                    st.session_state['chat_threads'][thread_id]["name"] = new_name
                    st.session_state['chat_threads'][thread_id]["editing"] = False
                    st.rerun()
            else:
                is_active = thread_id == st.session_state['thread_id']
                button_label = thread_info["name"]
                
                if st.button(
                    button_label,
                    key=f"btn_{thread_id}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state['thread_id'] = thread_id
                    messages = load_conversation(thread_id)
                    
                    temp_messages = []
                    for msg in messages:
                        role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                        temp_messages.append({'role': role, 'content': msg.content})
                    
                    st.session_state['message_history'] = temp_messages
                    st.rerun()
        
        with col2:
            if not thread_info["editing"]:
                if st.button("✏️", key=f"edit_{thread_id}"):
                    st.session_state['chat_threads'][thread_id]["editing"] = True
                    st.rerun()
        
        with col3:
            if not thread_info["editing"]:
                if st.button("🗑️", key=f"delete_{thread_id}"):
                    if len(st.session_state['chat_threads']) == 1:
                        del st.session_state['chat_threads'][thread_id]
                        reset_chat()
                    else:
                        was_active = st.session_state['thread_id'] == thread_id
                        del st.session_state['chat_threads'][thread_id]
                        
                        if was_active:
                            remaining_threads = list(st.session_state['chat_threads'].keys())
                            st.session_state['thread_id'] = remaining_threads[0]
                            messages = load_conversation(st.session_state['thread_id'])
                            temp_messages = []
                            for msg in messages:
                                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                                temp_messages.append({'role': role, 'content': msg.content})
                            st.session_state['message_history'] = temp_messages
                        
                        st.rerun()

# Main UI
if not st.session_state['message_history']:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-title">Welcome!</div>
            <div class="welcome-message">Hi, how can I help you?</div>
            <div class="welcome-subtitle">Start a conversation by typing a message below</div>
        </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state['message_history']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

user_input = st.chat_input('Type your message here...')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)
    
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content
        
        ai_message = st.write_stream(ai_only_stream())
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})