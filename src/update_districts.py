import json
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "processed",
    "normalized_schemes.json"
)


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def update_scheme_districts(tx, scheme):

    scheme_name = scheme.get("scheme_name")

    districts = scheme.get("districts", [])

    # Remove existing district relationships
    tx.run(
        """
        MATCH (s:Scheme {name: $scheme_name})
        MATCH (s)-[r:AVAILABLE_IN]->()
        DELETE r
        """,
        scheme_name=scheme_name
    )

    # Create normalized relationships
    for district in districts:

        tx.run(
            """
            MATCH (s:Scheme {name: $scheme_name})

            MERGE (d:District {name: $district})

            MERGE (s)-[:AVAILABLE_IN]->(d)
            """,
            scheme_name=scheme_name,
            district=district
        )


def main():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    print(f"Loaded {len(schemes)} schemes.")

    driver.verify_connectivity()

    print("Connected to Neo4j Aura.")

    with driver.session() as session:

        for index, scheme in enumerate(
            schemes,
            start=1
        ):

            print(
                f"[{index}/{len(schemes)}] "
                f"{scheme.get('scheme_name')}"
            )

            session.execute_write(
                update_scheme_districts,
                scheme
            )

    print()
    print("District relationships updated successfully.")


if __name__ == "__main__":

    try:

        main()

    finally:

        driver.close()