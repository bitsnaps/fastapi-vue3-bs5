#!pip install chromadb
import chromadb
import numpy as np

client = chromadb.Client()
collection = client.create_collection("example_collection")

collections = client.list_collections()
print(collections)

embeddings = np.random.rand(10, 128).astype("float32")
ids = [f"example-{i}" for i in range(10)]

# Convert embeddings to a list of lists
embeddings_list = embeddings.tolist()

# Add embeddings and ids to the collection
collection.add(
    embeddings=embeddings_list,
    ids=ids
)

query_embedding = np.random.rand(1, 128).astype("float32")
# Convert query_embedding to a list
query_embedding_list = query_embedding.tolist()

results = collection.query(
    query_embeddings=query_embedding_list,
    n_results=5
)

print(results)