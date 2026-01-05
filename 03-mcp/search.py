import sys
from indexer import extract_and_index_docs, search_docs

# Get query from command line argument
if len(sys.argv) < 2:
    print("Usage: python search.py <query>")
    print("Example: python search.py 'demo'")
    sys.exit(1)

query = sys.argv[1]

# Index the documentation
print("Starting indexing process...")
print("=" * 80)
index = extract_and_index_docs("fastmcp-main.zip")

# Test search with user-provided query
print("\n" + "=" * 80)
print(f"Testing search with query: '{query}'")
print("=" * 80)

results = search_docs(index, query, num_results=5)

print(f"\nFound {len(results)} results:")
print("=" * 80)

for i, doc in enumerate(results, 1):
    print(f"\n{i}. Filename: {doc['filename']}")
    print(f"   Content preview: {doc['content'][:200]}...")
    print("-" * 80)

# Show the first result
if results:
    first_file = results[0]['filename']
    print("\n" + "=" * 80)
    print(f"ANSWER: The first file returned for query '{query}' is:")
    print(f">>> {first_file}")
    print("=" * 80)
else:
    print("\nNo results found for this query.")
