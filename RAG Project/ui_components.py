import streamlit as st

def load_custom_css():
    """Load all custom CSS styles with professional dark/night mode and updated colors"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        .stApp {
            font-family: 'Inter', sans-serif;
            background: #121417;
            color: #e0e6f1;
            min-height: 100vh;
        }
        .main-header {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            padding: 2.5rem;
            border-radius: 20px;
            color: #e0e6f1;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .main-header h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
        }
        .main-header p {
            font-weight: 400;
            font-size: 1.2rem;
            opacity: 0.8;
            color: #cbd5e1;
        }
        .user-message {
            background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
            color: #f9fafb;
            padding: 15px 20px;
            border-radius: 25px 25px 8px 25px;
            margin: 15px 0;
            margin-left: 15%;
            box-shadow: 0 8px 25px rgba(55, 65, 81, 0.8);
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.15);
        }
        .ai-message {
            background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
            color: #e0e6f1;
            padding: 20px;
            border-radius: 25px 25px 25px 8px;
            margin: 15px 0;
            margin-right: 15%;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            border-left: 4px solid #10b981;
            font-weight: 400;
            line-height: 1.6;
        }
        .metrics-card {
            background: #111827;
            color: #a5b4fc;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.8);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .metrics-card h5 {
            color: #10b981;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .welcome-container, .setup-container {
            text-align: center;
            padding: 3rem;
            background: #111827;
            border-radius: 20px;
            margin: 2rem 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.8);
            color: #cbd5e1;
        }
        .welcome-container h4, .setup-container h3 {
            color: #e0e6f1;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .loading-modal {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(12px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        .loading-content {
            background: #111827;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
            color: #d1d5db;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
            border: 1px solid rgba(255,255,255,0.15);
            max-width: 400px;
        }
        .loading-spinner {
            width: 50px; height: 50px;
            border: 4px solid rgba(255,255,255,0.15);
            border-top: 4px solid #10b981;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% {transform: rotate(0deg);}
            100% {transform: rotate(360deg);}
        }
        .answer-badge {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.7);
            user-select: none;
        }
        .stChatInput > div {
            background: #1f2937 !important;
            border-radius: 25px;
            border: 2px solid #10b981 !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.7) !important;
            color: #d1d5db !important;
        }
        .stChatInput input {
            border: none !important;
            background: transparent !important;
            color: #d1d5db !important;
            font-family: 'Inter', sans-serif;
            font-weight: 400;
            padding: 15px 20px;
        }
        .stChatInput input::placeholder {
            color: #6b7280 !important;
        }
        .css-1d391kg {
            background: #1f2937 !important;
            color: #d1d5db !important;
            border: none !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_main_header():
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI Medical Research Assistant</h1>
        <p>Your intelligent companion for advanced medical research and analysis</p>
    </div>
    """, unsafe_allow_html=True)


def render_loading_modal(message="Processing documents..."):
    st.markdown(f"""
    <div class="loading-modal">
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <h3>{message}</h3>
            <p>Please wait while we prepare your medical research environment</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_message(message):
    st.markdown(f"""
    <div class="user-message">
        <strong>You:</strong> {message}
    </div>
    """, unsafe_allow_html=True)


def render_ai_message(message, answer_type="Basic Answer"):
    st.markdown(f"""
    <div class="ai-message">
        <div class="answer-badge">{answer_type}</div>
        <div>{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_ai_message_with_metrics(message, answer_type, precision, recall, f1):
    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.markdown(f"""
        <div class="ai-message">
            <div class="answer-badge">{answer_type}</div>
            <div>{message}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metrics-card">
            <h5>📊 Evaluation Metrics</h5>
            <div style="margin: 8px 0;"><strong>Precision:</strong> {precision:.3f}</div>
            <div style="margin: 8px 0;"><strong>Recall:</strong> {recall:.3f}</div>
            <div style="margin: 8px 0;"><strong>F1 Score:</strong> {f1:.3f}</div>
        </div>
        """, unsafe_allow_html=True)


def render_welcome_message():
    st.markdown("""
    <div class="welcome-container">
        <h4>👋 Welcome to AI Medical Research Assistant!</h4>
        <p>Ask me any medical question, request research analysis, or just say hello to get started.</p>
        <p><em>Powered by advanced AI and comprehensive medical knowledge</em></p>
    </div>
    """, unsafe_allow_html=True)


def render_setup_message():
    st.markdown("""
    <div class="setup-container">
        <h3>⚡ Initializing Medical Research Environment...</h3>
        <p>Loading and indexing medical documents for optimal search and analysis</p>
    </div>
    """, unsafe_allow_html=True)


def create_chat_controls():
    """Chat controls with always-on gold answer input"""
    if 'answer_type' not in st.session_state:
        st.session_state.answer_type = "Basic Answer"
    if 'gold_standard' not in st.session_state:
        st.session_state.gold_standard = ""

    with st.sidebar:
        st.markdown("### 🎛️ Chat Controls")

        st.markdown("**Answer Type:**")
        st.session_state.answer_type = st.selectbox(
            "Select Answer Type",
            options=["Basic Answer", "Chain of Thought"],
            index=0 if st.session_state.answer_type == "Basic Answer" else 1,
            key="answer_type_select"
        )

        st.markdown("**Evaluation:**")
        st.session_state.gold_standard = st.text_area(
            "Expected Answer:",
            value=st.session_state.gold_standard,
            height=80,
            placeholder="Enter the expected answer for evaluation...",
            help="This will be used to calculate precision, recall, and F1 score",
            key="gold_standard_input"
        )

    return st.session_state.answer_type, st.session_state.gold_standard


def create_clear_chat_button():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Clear Chat History", key="clear_chat", help="Clear all conversation history", use_container_width=True):
            return True
    return False


def render_document_success_popup(num_docs):
    st.success(f"""
    ✅ **Successfully loaded {num_docs} medical documents!**
    
    Your AI Medical Research Assistant is now ready with:
    - Advanced document search and retrieval
    - Contextual medical knowledge
    - Intelligent answer generation
    """)
