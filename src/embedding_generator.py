import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class SchemeEmbeddingGenerator:

    def __init__(self):

        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not self.uri:
            raise ValueError("NEO4J_URI is not configured")

        if not self.username:
            raise ValueError("NEO4J_USERNAME is not configured")

        if not self.password:
            raise ValueError("NEO4J_PASSWORD is not configured")

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY is not configured in .env"
            )

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    def get_schemes(self):

        query = """
        MATCH (s:Scheme)

        RETURN
            elementId(s) AS id,
            s.name AS scheme,
            s.description AS description,
            s.funding_pattern AS funding_pattern,
            s.sponsored_by AS sponsored_by,
            s.scheme_type AS scheme_type,
            s.validity AS validity,
            s.introduced_on AS introduced_on,
            s.how_to_avail AS how_to_avail
        ORDER BY s.name
        """

        with self.driver.session() as session:
            result = session.run(query)

            return [record.data() for record in result]

    def create_embedding_text(self, scheme):

        text = f"""
Scheme Name:
{scheme.get("scheme", "")}

Description:
{scheme.get("description", "")}

Funding Pattern:
{scheme.get("funding_pattern", "")}

Sponsored By:
{scheme.get("sponsored_by", "")}

Scheme Type:
{scheme.get("scheme_type", "")}

Validity:
{scheme.get("validity", "")}

Introduced On:
{scheme.get("introduced_on", "")}

How To Avail:
{scheme.get("how_to_avail", "")}
"""

        return text.strip()

    def save_embedding(self, node_id, embedding):

        query = """
        MATCH (s:Scheme)
        WHERE elementId(s) = $node_id

        SET s.embedding = $embedding

        RETURN s.name AS scheme
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                node_id=node_id,
                embedding=embedding
            )

            record = result.single()

            return record["scheme"] if record else None

    def generate(self):

        print("\n====================================")
        print("Starting Scheme Embedding Generation")
        print("====================================")

        schemes = self.get_schemes()

        print(f"Found {len(schemes)} schemes.")

        for index, scheme in enumerate(schemes, start=1):

            scheme_name = scheme["scheme"]

            print(
                f"[{index}/{len(schemes)}] "
                f"Creating embedding: {scheme_name}"
            )

            text = self.create_embedding_text(scheme)

            embedding = self.embeddings.embed_query(text)

            saved_scheme = self.save_embedding(
                scheme["id"],
                embedding
            )

            print(
                f"    Saved embedding for: {saved_scheme}"
            )

        print("\n====================================")
        print("Embedding generation completed!")
        print("====================================")

    def close(self):

        self.driver.close()


if __name__ == "__main__":

    generator = SchemeEmbeddingGenerator()

    try:
        generator.generate()

    finally:
        generator.close()