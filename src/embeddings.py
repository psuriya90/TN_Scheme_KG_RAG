import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class SchemeEmbeddings:

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured in .env"
            )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    def create_embedding(self, text):

        return self.embeddings.embed_query(text)