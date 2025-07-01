from pymilvus import connections, Collection

# Ganti dengan parameter koneksi milvus kamu
connections.connect("default", host="localhost", port="19530")

# Ganti dengan nama collection kamu
collection_name = "face_embeddings"

collection = Collection(collection_name)
print("Total vectors:", collection.num_entities)

# Menampilkan beberapa data vector (misal 5 vector pertama)
results = collection.query(expr="*", output_fields=["*"], limit=5)
for r in results:
    print(r)