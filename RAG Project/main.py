import streamlit as st
import zipfile, os, shutil
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from evaluation import evaluate_f1  
import nltk
from langchain.schema import Document
from dotenv import load_dotenv  # <-- NEW

# Import enhanced UI components
from ui_components import (
    load_custom_css, render_main_header, create_chat_controls,
    create_clear_chat_button, render_user_message, render_ai_message,
    render_ai_message_with_metrics, render_welcome_message, 
    render_setup_message, render_document_success_popup,
    render_loading_modal
)

# Load environment variables
load_dotenv()  # <-- NEW


def sentence_chunk_documents(documents, sentences_per_chunk=3):
    """Split documents into sentence-based chunks"""
    chunked_docs = []

    for doc in documents:
        sentences = nltk.sent_tokenize(doc.page_content)

        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_sentences = sentences[i:i + sentences_per_chunk]
            if chunk_sentences:
                chunk_text = ' '.join(chunk_sentences)
                chunked_doc = Document(
                    page_content=chunk_text,
                    metadata=doc.metadata.copy()
                )
                chunked_docs.append(chunked_doc)

    return chunked_docs


def get_prompt_template(answer_type):
    """Get prompt template based on answer type"""
    base_context = """
You are a highly skilled medical research assistant with expertise in analyzing complex medical information. Use the following context to provide accurate, evidence-based answers.

IMPORTANT: Only refer to chat history or previous questions when the user specifically asks about their conversation history, previous questions, or what they asked before. For casual greetings like "hello", "hi", etc., respond naturally without mentioning conversation history.

Context: {context}
Chat History: {chat_history}
Question: {question}
"""

    if answer_type == "Basic Answer":
        template = base_context + """
IMPORTANT: If the question is asking about previous questions, conversation history, or what was asked before, refer ONLY to the chat history and ignore the document context.

Provide a clear, concise, and medically accurate answer based on the context provided. Focus on key information that directly addresses the question.

Answer:"""

    elif answer_type == "Chain of Thought":
        template = base_context + """
Think through this medical question systematically and show your detailed reasoning process:

1. **Question Analysis**: What specific medical information is being requested?
2. **Context Review**: What relevant information is available in the provided context?
3. **Medical Reasoning**: How do the medical facts connect and what conclusions can be drawn?
4. **Evidence Synthesis**: What does the evidence collectively indicate?
5. **Final Answer**: Comprehensive response based on the systematic analysis

Let me work through this step by step:

**Analysis**: [Analyze what the question is asking medically]
**Relevant Medical Information**: [Extract key medical facts from context]
**Clinical Reasoning**: [Connect medical information logically]
**Evidence-Based Conclusion**: [Final medical answer based on evidence]

Answer:"""

    return template


# --- Configuration ---
st.set_page_config(
    page_title="🧠 AI Medical Research Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load enhanced CSS
load_custom_css()

# Constants
TEMP_DIR = "extracted_files"
VECTOR_DB_DIR = "vector_store"
EMBED_MODEL = "BAAI/bge-base-en-v1.5"
ZIP_PATH = r"D:\\data.zip" 

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectordb_ready" not in st.session_state:
    st.session_state.vectordb_ready = False
if "num_documents" not in st.session_state:
    st.session_state.num_documents = 0
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer"
    )

# --- Header ---
render_main_header()

# --- Document Loading (Background Process) ---
if not st.session_state.vectordb_ready:
    if os.path.exists(ZIP_PATH):
        # Show loading modal
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            render_loading_modal("Processing medical documents...")

        with st.spinner("🔄 Loading medical knowledge base..."):
            try:
                # Step 1: Extract ZIP
                shutil.rmtree(TEMP_DIR, ignore_errors=True)
                os.makedirs(TEMP_DIR, exist_ok=True)
                with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
                    zip_ref.extractall(TEMP_DIR)

                # Step 2: Load all .txt files
                documents = []
                for file_path in Path(TEMP_DIR).rglob("*.txt"):
                    try:
                        loader = TextLoader(str(file_path), encoding="utf-8")
                        documents.extend(loader.load())
                    except Exception as e:
                        st.error(f"Error loading {file_path}: {e}")

                if documents:
                    # Step 3: Apply sentence chunking
                    chunked_documents = sentence_chunk_documents(documents)

                    # Step 4: Create embeddings and vector store
                    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
                    shutil.rmtree(VECTOR_DB_DIR, ignore_errors=True)
                    vectordb = Chroma.from_documents(chunked_documents, embedding, persist_directory=VECTOR_DB_DIR)
                    vectordb.persist()

                    # Update session state
                    st.session_state.vectordb_ready = True
                    st.session_state.num_documents = len(documents)

                    # Clear loading modal
                    loading_placeholder.empty()

                    # Show success popup
                    render_document_success_popup(len(documents))
                    st.rerun()
                else:
                    loading_placeholder.empty()
                    st.error("❌ No .txt files found in the ZIP!")
            except Exception as e:
                loading_placeholder.empty()
                st.error(f"❌ Error processing ZIP file: {e}")
    else:
        st.error(f"❌ ZIP file not found: {ZIP_PATH}")

# --- Main Chat Interface ---
if st.session_state.vectordb_ready:
    # Initialize vector database
    vectordb = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=HuggingFaceEmbeddings(model_name=EMBED_MODEL))
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # --- Chat Controls (Answer Type & Evaluation) ---
    answer_type, gold_standard = create_chat_controls()

    # --- Dynamic Prompt Template ---
    template = get_prompt_template(answer_type)
    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"], 
        template=template
    )

    # --- Groq LLM Setup ---
    groq_key = os.getenv("GROQ_API_KEY")  # <-- fetch from env
    llm = ChatGroq(
        api_key=groq_key,
        model_name="llama3-70b-8192"
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=st.session_state.memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    # --- Chat History Display ---
    st.markdown("### 💬 Medical Research Conversation")

    if not st.session_state.chat_history:
        render_welcome_message()

    for item in st.session_state.chat_history:
        role = item[0]
        msg = item[1]

        if role == "user":
            render_user_message(msg)

        elif role == "ai":
            ans_type = item[2] if len(item) > 2 else "Basic Answer"
            gold_std = item[3] if len(item) > 3 and item[3] else None

            if gold_std:
                # Calculate evaluation metrics and render with metrics
                precision, recall, f1 = evaluate_f1(gold_std, msg)
                render_ai_message_with_metrics(msg, ans_type, precision, recall, f1)
            else:
                render_ai_message(msg, ans_type)

    # --- Chat Input ---
    st.markdown("### 💭 Ask Your Medical Question")
    user_question = st.chat_input("Type your medical question here... (e.g., 'What are the symptoms of diabetes?')")

    # --- Clear Chat Button (Below Input) ---
    if create_clear_chat_button():
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.success("🗑️ Chat history cleared!")
        st.rerun()

    # --- Process User Input ---
    if user_question:
        # Check if this is a conversation history question
        history_keywords = ["first question", "previous question", "what did i ask", "conversation history", "before", "earlier"]
        is_history_question = any(keyword in user_question.lower() for keyword in history_keywords)

        if is_history_question and st.session_state.chat_history:
            # Handle history questions directly
            user_questions = [item[1] for item in st.session_state.chat_history if item[0] == "user"]
            if "first" in user_question.lower() and user_questions:
                answer = f"Your first question was: '{user_questions[0]}'"
            elif user_questions:
                answer = "Your previous questions were: " + ", ".join([f"'{q}'" for q in user_questions])
            else:
                answer = "You haven't asked any questions yet in this conversation."
        else:
            # Handle normal medical questions
            result = qa_chain({"question": user_question})
            answer = result["answer"]

        # Add to display history
        st.session_state.chat_history.append(("user", user_question))
        st.session_state.chat_history.append(("ai", answer, answer_type, gold_standard))
        st.rerun()

else:
    # Show setup message when documents are not ready
    render_setup_message()