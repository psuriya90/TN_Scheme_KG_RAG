import streamlit as st

from src.rag_pipeline import RAGPipeline


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Tamil Nadu Scheme Assistant",
    page_icon="🏛️",
    layout="wide"
)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🏛️ Tamil Nadu Government Scheme Assistant")

st.markdown(
    """
Ask questions about Tamil Nadu Government schemes.

Examples:

- What schemes are available for farmers?
- What schemes are available in Coimbatore?
- What benefits are available for farmers?
- How can I apply for Training to Farmers?
"""
)


# ---------------------------------------------------
# CREATE RAG PIPELINE
# ---------------------------------------------------

@st.cache_resource
def load_pipeline():

    return RAGPipeline()


pipeline = load_pipeline()


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------
# USER QUESTION
# ---------------------------------------------------

question = st.chat_input(
    "Ask about Tamil Nadu Government schemes..."
)


if question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Generate answer

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching government schemes..."
        ):

            try:

                result = pipeline.answer(
                    question
                )

                answer = result["answer"]

                st.markdown(answer)

                # Sources

                sources = result.get(
                    "sources",
                    []
                )

                if sources:

                    st.markdown(
                        "### Sources"
                    )

                    for source in sources:

                        st.markdown(
                            f"- {source}"
                        )

                # Debug information

                with st.expander(
                    "🔎 Retrieved schemes"
                ):

                    for item in result.get(
                        "retrieved_results",
                        []
                    ):

                        st.write(
                            item.get(
                                "scheme"
                            )
                        )

            except Exception as error:

                st.error(
                    f"Error: {error}"
                )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )