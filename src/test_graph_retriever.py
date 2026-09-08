from graph_retriever import GraphRetriever


retriever = GraphRetriever()

try:

    print("\nSearching for Training to Farmers...\n")

    results = retriever.get_scheme_by_name(
        "Training to Farmers"
    )

    for result in results:

        print("Scheme:")
        print(result["scheme"])

        print("\nDescription:")
        print(result["description"])

        print("\nDistricts:")
        print(result["districts"])

        print("\nBeneficiaries:")
        print(result["beneficiaries"])

        print("\nBenefits:")
        print(result["benefits"])

        print("\nFunding:")
        print(result["funding_pattern"])

        print("\nHow to Apply:")
        print(result["how_to_avail"])

        print("\nSource:")
        print(result["source_url"])

finally:

    retriever.close()