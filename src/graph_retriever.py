import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class GraphRetriever:

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

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def close(self):
        self.driver.close()

    # -----------------------------------------
    # Search by district
    # -----------------------------------------
    def get_schemes_by_district(self, district):

        query = """
        MATCH (s:Scheme)-[:AVAILABLE_IN]->(d:District)
        WHERE toLower(d.name) CONTAINS toLower($district)

        RETURN DISTINCT
            s.name AS scheme,
            s.description AS description,
            s.how_to_avail AS how_to_avail,
            s.source_url AS source_url
        ORDER BY s.name
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                district=district
            )

            return [record.data() for record in result]

    # -----------------------------------------
    # Search by beneficiary
    # -----------------------------------------
    def get_schemes_by_beneficiary(self, beneficiary):

        query = """
        MATCH (s:Scheme)-[:TARGETS]->(b:Beneficiary)

        WHERE toLower(b.name) CONTAINS toLower($beneficiary)

        RETURN DISTINCT
            s.name AS scheme,
            s.description AS description,
            s.source_url AS source_url
        ORDER BY s.name
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                beneficiary=beneficiary
            )

            return [record.data() for record in result]

    # -----------------------------------------
    # Search by scheme name
    # -----------------------------------------
    def get_scheme_by_name(self, scheme_name):

        query = """
        MATCH (s:Scheme)

        WHERE toLower(s.name) CONTAINS toLower($scheme_name)

        OPTIONAL MATCH (s)-[:AVAILABLE_IN]->(d:District)
        OPTIONAL MATCH (s)-[:TARGETS]->(b:Beneficiary)
        OPTIONAL MATCH (s)-[:HAS_BENEFIT]->(benefit:Benefit)
        OPTIONAL MATCH (s)-[:SPONSORED_BY]->(sp:Sponsor)

        RETURN
            s.name AS scheme,
            s.description AS description,
            s.funding_pattern AS funding_pattern,
            s.how_to_avail AS how_to_avail,
            s.validity AS validity,
            s.introduced_on AS introduced_on,
            s.scheme_type AS scheme_type,
            s.source_url AS source_url,
            collect(DISTINCT d.name) AS districts,
            collect(DISTINCT b.name) AS beneficiaries,
            collect(DISTINCT benefit.name) AS benefits,
            collect(DISTINCT sp.name) AS sponsors
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                scheme_name=scheme_name
            )

            return [record.data() for record in result]

    # -----------------------------------------
    # Get all schemes
    # -----------------------------------------
    def get_all_schemes(self):

        query = """
        MATCH (s:Scheme)

        RETURN
            s.name AS scheme,
            s.description AS description,
            s.source_url AS source_url

        ORDER BY s.name
        """

        with self.driver.session() as session:
            result = session.run(query)

            return [record.data() for record in result]


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    retriever = GraphRetriever()

    try:

        print("\n====================================")
        print("Testing Graph Retriever")
        print("====================================")

        print("\nSchemes available in Coimbatore:\n")

        schemes = retriever.get_schemes_by_district(
            "Coimbatore"
        )

        print(f"Found {len(schemes)} schemes\n")

        for scheme in schemes:
            print("-", scheme["scheme"])

        print("\n====================================")
        print("Graph Retriever Test Completed")
        print("====================================")

    finally:
        retriever.close()