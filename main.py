from orchestrator import run_orchestrator

if __name__ == "__main__":
    # Example task — change this to anything
    task = """
    Analyze the competitive landscape of table tennis coaching apps.
    Research what exists, analyze the gaps and opportunities, 
    then write a concise summary I can use for product planning.
    """

    result = run_orchestrator(task)

    print("\n" + "=" * 60)
    print("📄 FINAL OUTPUT")
    print("=" * 60)
    print(result)
