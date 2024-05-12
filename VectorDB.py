import chromadb

client = chromadb.PersistentClient("C:/Users/engel/Escritorio/Universidad/Sem6/Crypto/Reto/VectorDB")

collection = client.get_or_create_collection(
        name="Usuarios",
        metadata={"hnsw:space": "l2"}
    )

def agregarEmbedding(usuario):
    try:
        if collection.get(ids = usuario["id"])["ids"]  != []:
            return {"success":False, "result":"id repetido"}
        collection.add(
            embeddings=usuario["encoding"],
            ids = usuario["id"]
        )
        return {"success":True, "result":"all good"}
    except Exception as e:
        return {"success":False, "result":e}
    
def getUsers(embedding):
    try:
        result = {}
        users = collection.query(
            query_embeddings= embedding
        )
        result["ids"] = users["ids"]
        result["distances"] = users["distances"]
        return {"success":True, "result": result}
    except Exception as e:
        return {"success":False, "result":e}
    
def getEmbeddings(id):
    try:
        user = collection.get(ids = id, include=['embeddings'])
        return {"success":True, "result": user["embeddings"][0]}
    except Exception as e:
        return {"success":False, "result":e}
