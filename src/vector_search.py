import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class VectorSearch:

    def __init__(self):

        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    def search(self, question, top_k=5):

        query_embedding = self.embeddings.embed_query(
            question
        )

        query = """
        CALL db.index.vector.queryNodes(
            'scheme_embeddings',
            $top_k,
            $embedding
        )
        YIELD node, score

        RETURN
            node.name AS scheme,
            node.description AS description,
            node.source_url AS source_url,
            score

        ORDER BY score DESC
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                top_k=top_k,
                embedding=query_embedding
            )

            return [record.data() for record in result]

    def close(self):

        self.driver.close()


if __name__ == "__main__":

    searcher = VectorSearch()

    try:

        question = (
            "What government schemes are available "
            "for farmers?"
        )

        print("\nQuestion:")
        print(question)

        print("\nVector Search Results:")
        print("------------------------------------")

        results = searcher.search(
            question,
            top_k=5
        )

        for index, result in enumerate(results, start=1):

            print(f"\n{index}. {result['scheme']}")
            print(f"Score: {result['score']}")
            print(f"Source: {result['source_url']}")

    finally:

        searcher.close()