import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# ---------------------------------------------------------
# Validate configuration
# ---------------------------------------------------------

if not NEO4J_URI:
    raise ValueError(
        "NEO4J_URI is not configured in .env"
    )

if not NEO4J_USERNAME:
    raise ValueError(
        "NEO4J_USERNAME is not configured in .env"
    )

if not NEO4J_PASSWORD:
    raise ValueError(
        "NEO4J_PASSWORD is not configured in .env"
    )


# ---------------------------------------------------------
# Create Neo4j driver
# ---------------------------------------------------------

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )
)


def verify_connection():

    print("Connecting to Neo4j Aura...")

    driver.verify_connectivity()

    print("Successfully connected to Neo4j Aura!")


if __name__ == "__main__":

    try:

        verify_connection()

    finally:

        driver.close()