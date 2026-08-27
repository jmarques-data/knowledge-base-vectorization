import os
from chromadb.config import Settings
import chromadb
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.getenv("CHROMA_PATH", os.path.join(ROOT_DIR, "vector_db"))

def testar_busca():
    print(f"Lendo ChromaDB em: {DB_DIR}")
    client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(anonymized_telemetry=False))
    
    try:
        collection = client.get_collection("base_conhecimento_ti")
    except Exception as e:
        print(f"Erro: Collection não encontrada. {e}")
        return
        
    query = "O NVR continua pingando na rede mas a câmera IP está offline."
    print(f"\nBuscando por: '{query}'")
    
    resultados = collection.query(
        query_texts=[query],
        n_results=1
    )
    
    if resultados and resultados['documents'] and len(resultados['documents'][0]) > 0:
        print("\n=== Resultado Encontrado ===")
        print(f"Distância: {resultados['distances'][0][0]}")
        print(f"Metadados: {resultados['metadatas'][0][0]}")
        print(f"Trecho: {resultados['documents'][0][0][:200]}...")
        print("============================")
        print("TESTE_OK")
    else:
        print("Nenhum resultado encontrado.")
        print("TESTE_FALHOU")

if __name__ == "__main__":
    testar_busca()
