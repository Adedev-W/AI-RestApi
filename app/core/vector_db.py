from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType
import os
from dotenv import load_dotenv

load_dotenv()

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = "face_embeddings"
EMBEDDING_DIM = 512  # Sesuai dengan model insightface
MATCH_THRESHOLD = 0.5  # Cosine similarity threshold for a match

class MilvusService:
    def __init__(self):
        try:
            connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
            self._create_collection_if_not_exists()
        except Exception as e:
            print(f"Error connecting to Milvus: {e}")
            self.collection = None

    def _create_collection_if_not_exists(self):
        if not utility.has_collection(COLLECTION_NAME):
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="person_name", dtype=DataType.VARCHAR, max_length=255),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
            ]
            schema = CollectionSchema(fields, "Face embeddings collection")
            self.collection = Collection(COLLECTION_NAME, schema)
            
            # Buat index untuk pencarian cepat
            index_params = {"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 1024}}
            self.collection.create_index("embedding", index_params)
        else:
            self.collection = Collection(COLLECTION_NAME)
        self.collection.load()

    def insert_embedding(self, person_name: str, embedding: list):
        if self.collection is None:
            raise ConnectionError("Not connected to Milvus collection.")
        data = [[person_name], [embedding]]
        self.collection.insert(data)
        self.collection.flush()
        print(f"Inserted embedding for {person_name}")

    def has_embeddings(self, person_name: str) -> bool:
        if self.collection is None: return False
        results = self.collection.query(f'person_name == "{person_name}"', limit=1)
        return len(results) > 0

    def search_and_compare(self, person_name: str, query_embedding: list, top_k: int = 1):
        if self.collection is None: raise ConnectionError("Not connected to Milvus.")
        
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
        expr = f'person_name == "{person_name}"'

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=expr
        )
        
        if not results or not results[0]:
            return {"match": False, "similarity": 0.0}

        similarity_score = results[0][0].distance
        return {
            "match": bool(similarity_score > MATCH_THRESHOLD),
            "similarity": float(similarity_score)
        }

# Inisialisasi service sebagai singleton
milvus_service = MilvusService() 