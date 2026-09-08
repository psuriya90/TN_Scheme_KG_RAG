import json
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# --------------------------------------------------
# Validate configuration
# --------------------------------------------------

if not NEO4J_URI:
    raise ValueError("NEO4J_URI is not configured")

if not NEO4J_USERNAME:
    raise ValueError("NEO4J_USERNAME is not configured")

if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD is not configured")


# --------------------------------------------------
# Create Neo4j driver
# --------------------------------------------------

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


# --------------------------------------------------
# Load JSON data
# --------------------------------------------------

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "processed",
    "cleaned_schemes.json"
)


def load_schemes():
    print("Loading scheme data...")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        schemes = json.load(file)

    print(f"Loaded {len(schemes)} schemes.")

    return schemes


# --------------------------------------------------
# Create graph
# --------------------------------------------------

def create_scheme(tx, scheme):

    query = """
    MERGE (d:Department {name: $department})

    MERGE (s:Scheme {name: $scheme_name})
    SET s.description = $description,
        s.funding_pattern = $funding_pattern,
        s.sponsored_by = $sponsored_by,
        s.scheme_type = $scheme_type,
        s.validity = $validity,
        s.introduced_on = $introduced_on,
        s.how_to_avail = $how_to_avail,
        s.source_url = $source_url

    MERGE (d)-[:OFFERS]->(s)
    """

    tx.run(
        query,
        department=scheme.get("department", ""),
        scheme_name=scheme.get("scheme_name", ""),
        description=scheme.get("description", ""),
        funding_pattern=scheme.get("funding_pattern", ""),
        sponsored_by=scheme.get("sponsored_by", ""),
        scheme_type=scheme.get("scheme_type", ""),
        validity=scheme.get("validity", ""),
        introduced_on=scheme.get("introduced_on", ""),
        how_to_avail=scheme.get("how_to_avail", ""),
        source_url=scheme.get("source_url", "")
    )


# --------------------------------------------------
# Add relationships
# --------------------------------------------------

def create_relationships(tx, scheme):

    scheme_name = scheme.get("scheme_name", "")

    # ----------------------------------------------
    # Beneficiary
    # ----------------------------------------------

    beneficiary = scheme.get("beneficiaries", "").strip()

    if beneficiary:

        tx.run(
            """
            MATCH (s:Scheme {name: $scheme_name})

            MERGE (b:Beneficiary {name: $beneficiary})

            MERGE (s)-[:TARGETS]->(b)
            """,
            scheme_name=scheme_name,
            beneficiary=beneficiary
        )

    # ----------------------------------------------
    # Benefit
    # ----------------------------------------------

    benefit = scheme.get("benefits", "").strip()

    if benefit:

        tx.run(
            """
            MATCH (s:Scheme {name: $scheme_name})

            MERGE (b:Benefit {name: $benefit})

            MERGE (s)-[:HAS_BENEFIT]->(b)
            """,
            scheme_name=scheme_name,
            benefit=benefit
        )

    # ----------------------------------------------
    # Sponsor
    # ----------------------------------------------

    sponsor = scheme.get("sponsored_by", "").strip()

    if sponsor:

        tx.run(
            """
            MATCH (s:Scheme {name: $scheme_name})

            MERGE (sp:Sponsor {name: $sponsor})

            MERGE (s)-[:SPONSORED_BY]->(sp)
            """,
            scheme_name=scheme_name,
            sponsor=sponsor
        )

    # ----------------------------------------------
    # Districts
    # ----------------------------------------------

    districts = scheme.get("districts", [])

    for district in districts:

        district = district.strip()

        if not district:
            continue

        tx.run(
            """
            MATCH (s:Scheme {name: $scheme_name})

            MERGE (d:District {name: $district})

            MERGE (s)-[:AVAILABLE_IN]->(d)
            """,
            scheme_name=scheme_name,
            district=district
        )


# --------------------------------------------------
# Main loading function
# --------------------------------------------------

def load_into_neo4j():

    schemes = load_schemes()

    print("Connecting to Neo4j Aura...")

    driver.verify_connectivity()

    print("Connected successfully.")

    with driver.session() as session:

        for index, scheme in enumerate(schemes, start=1):

            print(
                f"[{index}/{len(schemes)}] "
                f"Loading: {scheme.get('scheme_name')}"
            )

            session.execute_write(
                create_scheme,
                scheme
            )

            session.execute_write(
                create_relationships,
                scheme
            )

    print()
    print("====================================")
    print("Knowledge Graph loading completed!")
    print("====================================")


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":

    try:

        load_into_neo4j()

    except Exception as error:

        print()
        print("ERROR:")
        print(error)

    finally:

        driver.close()