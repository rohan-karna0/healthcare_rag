import streamlit as st

from config.settings import settings
from config.sources import get_source_names
from generation.answer_formatter import format_answer
from generation.generator import Generator
from ingestion.ingest import IngestionPipeline
from processing.indexing.index_pipeline import IndexPipeline
from retrieval.retriever import Retriever

st.set_page_config(page_title="Healthcare RAG", page_icon="🏥", layout="wide")
st.title("Healthcare RAG Assistant")
st.caption("Grounded healthcare Q&A using local Ollama and Qdrant retrieval.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Ollama model", [settings.ollama_model, "mistral", "qwen2.5"])
    mode = st.selectbox("Retrieval mode", ["hybrid", "dense", "bm25"])
    top_k = st.slider("Top K", min_value=1, max_value=10, value=settings.top_k)
    source_filter = st.multiselect("Source filter", get_source_names())

    if st.button("Ingest & Index Sample/Data"):
        with st.spinner("Running ingestion pipeline..."):
            result = IngestionPipeline().ingest(sources=source_filter or None, index=True)
        st.success(
            f"Processed {result.documents_processed} documents, "
            f"created {result.chunks_created} chunks."
        )

    if st.button("Re-index Existing Chunks"):
        with st.spinner("Indexing chunks..."):
            count = IndexPipeline().run()
        st.success(f"Indexed {count} chunks.")

retriever = Retriever()
generator = Generator(model=model)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f"**[{source['index']}] {source['title']}** ({source['source']})")
                    st.markdown(source["url"])

if prompt := st.chat_input("Ask a healthcare question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not generator.check_health():
            st.error("Ollama is not running. Start Ollama and pull a model (e.g. llama3.2).")
        else:
            chunks = retriever.retrieve(
                query=prompt,
                top_k=top_k,
                sources=source_filter or None,
                mode=mode,
            )
            with st.spinner("Generating answer..."):
                result = generator.generate(prompt, chunks)
            formatted = format_answer(result.answer, result.sources)
            st.markdown(formatted)

            from generation.citations import build_citations

            citations = build_citations(result.sources)
            with st.expander("Retrieved Sources"):
                for citation in citations:
                    st.markdown(
                        f"**[Source {citation['index']}]** {citation['title']} "
                        f"({citation['source']}) — score: {citation['score']:.3f}"
                    )
                    st.markdown(citation["url"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": formatted,
                    "sources": citations,
                }
            )
