
import pandas as pd
import streamlit as st
from pathlib import Path

from rag_engine import RAGEngine


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CloudMentor AI",
    page_icon="☁️",
    layout="wide"
)


# --------------------------------------------------
# LOAD RAG ENGINE ONCE
# --------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_rag_engine():
    return RAGEngine()


# --------------------------------------------------
# DISPLAY RETRIEVED SOURCES
# --------------------------------------------------

def display_sources(
    sources,
    key_suffix="current",
    show_player=True
):

    if isinstance(sources, list):
        sources = pd.DataFrame(sources)

    st.markdown("### 📚 Retrieved lecture sources")

    playable_sources = []

    for index, row in sources.iterrows():

        title = row["title"]
        day = row["day"]
        score = float(row["similarity"])

        with st.expander(
            f"SOURCE {index + 1} | {day} | {title} | Score: {score:.3f}"
        ):

            st.write(f"**Lecture:** {title}")
            st.write(f"**Course day:** {day}")

            start = float(row["start"])
            end = float(row["end"])

            st.write(f"**Timestamp:** {start:.2f}s – {end:.2f}s")
            st.write(f"**Similarity:** {score:.4f}")

            st.markdown("**Retrieved lecture content:**")
            st.write(row["text"])

            video_path = row.get("video_path")
            youtube_url = row.get("youtube_url")

            if isinstance(video_path, str) and Path(video_path).is_file():

                st.caption("Original MP4 video available.")
                playable_sources.append(
                    (index, row, "local")
                )

            elif (
                isinstance(youtube_url, str)
                and youtube_url.startswith(("https://", "http://"))
            ):

                st.caption("Original YouTube video available.")
                playable_sources.append(
                    (index, row, "youtube")
                )

    # Load only one video player at a time
    if show_player and playable_sources:

        st.markdown("### ▶ Watch original lecture")

        options = {
            (
                f"Source {index + 1} | {row['day']} | "
                f"{row['title']} | {float(row['start']):.1f}s"
            ): (row, video_type)
            for index, row, video_type in playable_sources
        }

        selected = st.selectbox(
            "Choose a lecture segment",
            list(options.keys()),
            key=f"video_selector_{key_suffix}"
        )

        selected_row, video_type = options[selected]

        if video_type == "local":

            st.video(
                selected_row["video_path"],
                start_time=int(float(selected_row["start"]))
            )

        else:

            st.video(
                selected_row["youtube_url"],
                start_time=int(float(selected_row["start"]))
            )

    elif show_player:

        st.info("No playable video was found for these sources.")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("☁️ CloudMentor AI")

    st.caption("Your personal AWS & DevOps learning assistant")

    st.divider()

    st.markdown("### Knowledge Base")

    st.write("📚 25 recorded lectures")
    st.write("🧩 624 searchable chunks")
    st.write("🧠 BGE-small embeddings")
    st.write("🤖 Gemini API")

    st.divider()

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=1,
        max_value=8,
        value=5
    )

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("CloudMentor AI | RAG-based learning assistant")


# --------------------------------------------------
# MAIN INTERFACE
# --------------------------------------------------

st.title("☁️ CloudMentor AI")

st.markdown(
    """
    Ask questions about AWS, DevOps, Kubernetes, Docker,
    Terraform and cloud infrastructure.

    Answers are generated using your recorded lectures
    and Gemini's language model.
    """
)

st.divider()


# --------------------------------------------------
# INITIALIZE ENGINE
# --------------------------------------------------

try:

    with st.spinner("Initializing AI knowledge base..."):

        rag_engine = load_rag_engine()

except Exception as error:

    st.error("Unable to initialize the RAG engine.")

    st.exception(error)

    st.stop()


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message_index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources")

            if sources:
                display_sources(
                    sources,
                    key_suffix=f"history_{message_index}",
                    show_player=False
                )


# --------------------------------------------------
# USER QUESTION
# --------------------------------------------------

question = st.chat_input(
    "Ask something about AWS or DevOps..."
)


if question:

    # Display user message
    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching your lectures and generating an answer..."
        ):

            try:

                result = rag_engine.answer(
                    question,
                    top_k=top_k
                )

                answer = result["answer"]

                sources = result["sources"]

                st.markdown(answer)

                display_sources(sources,
                    key_suffix="current",
                    show_player=True
                )

                # Save conversation
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources.to_dict("records")
                })

            except Exception as error:

                st.error(
                    "Something went wrong while generating your answer."
                )

                st.exception(error)


st.divider()

st.caption(
    "Powered by Retrieval-Augmented Generation, "
    "BGE-small embeddings and Google Gemini."
)
