import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

# Set page configuration
st.set_page_config(page_title="RAG Chunking and Embedding", layout="wide")

# Title
st.title("RAG Chunking and Embedding Application")

# Upload Section
st.header("1. Upload Document")
uploaded_file = st.file_uploader("Upload a .txt file for chunking and analysis", type="txt")

if uploaded_file:
    document = uploaded_file.read().decode("utf-8").strip()

    if not document:
        st.warning("Uploaded file is empty. Please upload a valid text document.")
        st.stop()

    # Initialize text splitters
    fixed_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    fixed_chunks = fixed_splitter.split_text(document)
    recursive_chunks = recursive_splitter.split_text(document)

    # Display chunking results
    st.header("2. Chunking Summary")
    st.write(f"Fixed-size Chunks: {len(fixed_chunks)}")
    st.write(f"Recursive Chunks: {len(recursive_chunks)}")

    # Define queries
    queries = [
        "What is carbon dioxide and methane?",
        "What is happening to glaciers and ice sheets?",
        "What are renewable energy solutions?",
        "What causes sea levels to rise?",
        "What is the greenhouse effect?"
    ]

    # Simple keyword match function
    def match_query(chunks, query):
        query_words = query.lower().split()
        best_index = 0
        highest_score = 0
        for idx, chunk in enumerate(chunks):
            score = sum(1 for word in query_words if word in chunk.lower())
            if score > highest_score:
                best_index = idx
                highest_score = score
        return best_index

    # Query Results Section
    st.header("3. Query Matching Results")

    with st.expander("View Matched Chunks"):
        for query in queries:
            st.subheader(f"Query: {query}")
            col1, col2 = st.columns(2)

            idx_fixed = match_query(fixed_chunks, query)
            idx_recursive = match_query(recursive_chunks, query)

            with col1:
                st.markdown("**Fixed-size Chunk Match:**")
                st.text(fixed_chunks[idx_fixed])

            with col2:
                st.markdown("**Recursive Chunk Match:**")
                st.text(recursive_chunks[idx_recursive])

    # Embedding Section
    st.header("4. Embedding Generation")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings_fixed = model.encode(fixed_chunks, show_progress_bar=False)
    embeddings_recursive = model.encode(recursive_chunks, show_progress_bar=False)

    st.write(f"Fixed-size Embedding Shape: {embeddings_fixed.shape}")
    st.write(f"Recursive Embedding Shape: {embeddings_recursive.shape}")

else:
    st.info("Please upload a `.txt` document to begin.")
