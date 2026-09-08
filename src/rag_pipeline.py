import os

from dotenv import load_dotenv
from openai import OpenAI

from .hybrid_retriever import HybridRetriever


load_dotenv()


class RAGPipeline:

    def __init__(self):

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY is not configured"
            )

        self.client = OpenAI()

        self.retriever = HybridRetriever()

        self.model = os.getenv(
            "OPENAI_CHAT_MODEL",
            "gpt-5.6-luna"
        )

    # ------------------------------------------------

    def build_context(self, results):

        context_parts = []

        for index, result in enumerate(
            results,
            start=1
        ):

            context = f"""
SOURCE {index}

Scheme:
{result.get("scheme", "")}

Description:
{result.get("description", "")}

Funding:
{result.get("funding_pattern", "")}

How to Avail:
{result.get("how_to_avail", "")}

Districts:
{", ".join(result.get("districts", []))}

Source URL:
{result.get("source_url", "")}
"""

            context_parts.append(
                context.strip()
            )

        return "\n\n".join(context_parts)

    # ------------------------------------------------

    def answer(self, question):

        results = self.retriever.retrieve(
            question,
            top_k=5
        )

        if not results:

            return {
                "answer": (
                    "I could not find relevant Tamil Nadu "
                    "Government scheme information."
                ),
                "sources": []
            }

        context = self.build_context(results)

        prompt = f"""
You are a Tamil Nadu Government Schemes assistant.

Answer the user's question using ONLY the
information provided in the retrieved context.

Do not invent:
- scheme names
- eligibility rules
- benefits
- application procedures
- funding details
- government departments

If the context does not contain enough information,
clearly say that the available data does not provide
the answer.

Keep the answer clear and useful.

Whenever possible:
1. Mention the scheme name.
2. Explain the relevant benefit.
3. Explain eligibility or target beneficiaries if available.
4. Explain how to apply if available.
5. Provide the official source URL.

USER QUESTION:
{question}

RETRIEVED CONTEXT:
{context}
"""

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        answer = response.output_text

        sources = []

        for result in results:

            source_url = result.get(
                "source_url"
            )

            if source_url and source_url not in sources:

                sources.append(source_url)

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_results": results
        }

    # ------------------------------------------------

    def close(self):

        self.retriever.close()


# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    pipeline = RAGPipeline()

    try:

        question = (
            "What schemes are available "
            "for farmers in Coimbatore?"
        )

        result = pipeline.answer(question)

        print("\n====================================")
        print("RAG ANSWER")
        print("====================================")

        print("\n")
        print(result["answer"])

        print("\n====================================")
        print("SOURCES")
        print("====================================")

        for source in result["sources"]:

            print(source)

    finally:

        pipeline.close()