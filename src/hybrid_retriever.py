import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import OpenAIEmbeddings

load_dotenv()


class HybridRetriever:

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
                "OPENAI_API_KEY is not configured"
            )

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

    # ------------------------------------------------
    # GRAPH SEARCH
    # ------------------------------------------------

    def graph_search(self, question, limit=5):

        question_lower = question.lower()

        results = []

        # District-based search
        district_query = """
        MATCH (s:Scheme)-[:AVAILABLE_IN]->(d:District)

        WHERE toLower(d.name) CONTAINS toLower($question)

        RETURN DISTINCT
            s.name AS scheme,
            s.description AS description,
            s.how_to_avail AS how_to_avail,
            s.source_url AS source_url,
            collect(DISTINCT d.name) AS districts

        LIMIT $limit
        """

        with self.driver.session() as session:

            records = session.run(
                district_query,
                question=question_lower,
                limit=limit
            )

            results.extend(
                [record.data() for record in records]
            )

        # Beneficiary-based search
        beneficiary_query = """
        MATCH (s:Scheme)-[:TARGETS]->(b:Beneficiary)

        WHERE toLower(b.name) CONTAINS "farmer"

        RETURN DISTINCT
            s.name AS scheme,
            s.description AS description,
            s.how_to_avail AS how_to_avail,
            s.source_url AS source_url,
            [] AS districts

        LIMIT $limit
        """

        # Only use this broad beneficiary search when
        # the question appears related to farmers.
        if "farmer" in question_lower or "farmers" in question_lower:

            with self.driver.session() as session:

                records = session.run(
                    beneficiary_query,
                    limit=limit
                )

                results.extend(
                    [record.data() for record in records]
                )

        return results

    # ------------------------------------------------
    # VECTOR SEARCH
    # ------------------------------------------------

    def vector_search(self, question, limit=5):

        query_embedding = self.embeddings.embed_query(
            question
        )

        query = """
        MATCH (s:Scheme)

        SEARCH s IN (
            VECTOR INDEX scheme_embeddings
            FOR $embedding
            LIMIT $limit
        )
        SCORE AS score

        RETURN
            s.name AS scheme,
            s.description AS description,
            s.funding_pattern AS funding_pattern,
            s.how_to_avail AS how_to_avail,
            s.source_url AS source_url,
            score

        ORDER BY score DESC
        """

        with self.driver.session() as session:

            records = session.run(
                query,
                embedding=query_embedding,
                limit=limit
            )

            return [
                record.data()
                for record in records
            ]

    # ------------------------------------------------
    # RESULT FUSION
    # ------------------------------------------------

    def retrieve(self, question, top_k=5):

        graph_results = self.graph_search(
            question,
            limit=top_k
        )

        vector_results = self.vector_search(
            question,
            limit=top_k
        )

        combined = {}

        # Graph results receive a graph score.
        for rank, result in enumerate(graph_results):

            scheme = result["scheme"]

            combined[scheme] = {
                **result,
                "graph_rank": rank + 1,
                "vector_rank": None
            }

        # Add vector results.
        for rank, result in enumerate(vector_results):

            scheme = result["scheme"]

            if scheme not in combined:

                combined[scheme] = {
                    **result,
                    "graph_rank": None,
                    "vector_rank": rank + 1
                }

            else:

                combined[scheme]["vector_rank"] = rank + 1

                combined[scheme]["score"] = result.get(
                    "score"
                )

        # ---------------------------------------------
        # Reciprocal Rank Fusion
        # ---------------------------------------------

        for scheme, result in combined.items():

            graph_rank = result.get("graph_rank")
            vector_rank = result.get("vector_rank")

            rrf_score = 0

            if graph_rank:
                rrf_score += 1 / (60 + graph_rank)

            if vector_rank:
                rrf_score += 1 / (60 + vector_rank)

            result["rrf_score"] = rrf_score

        final_results = sorted(
            combined.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        return final_results[:top_k]

    # ------------------------------------------------

    def close(self):

        self.driver.close()


# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    retriever = HybridRetriever()

    try:

        question = (
            "What schemes are available "
            "for farmers in Coimbatore?"
        )

        print("\n====================================")
        print("HYBRID RAG TEST")
        print("====================================")

        print("\nQuestion:")
        print(question)

        results = retriever.retrieve(
            question,
            top_k=5
        )

        print("\nHybrid Results:")
        print("------------------------------------")

        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{index}. {result['scheme']}"
            )

            print(
                f"RRF Score: "
                f"{result['rrf_score']:.6f}"
            )

            print(
                f"Vector Score: "
                f"{result.get('score', 'N/A')}"
            )

            print(
                f"Graph Rank: "
                f"{result.get('graph_rank')}"
            )

            print(
                f"Vector Rank: "
                f"{result.get('vector_rank')}"
            )

    finally:

        retriever.close()