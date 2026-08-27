import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIGURAÇÕES =================
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = os.getenv("KNOWLEDGE_PATH", os.path.join(ROOT_DIR, "knowledge"))
DB_DIR = os.getenv("CHROMA_PATH", os.path.join(ROOT_DIR, "vector_db"))
SCRIPTS_DIR = os.getenv("SQL_SCRIPTS_PATH", os.path.join(ROOT_DIR, "knowledge", "sql_scripts"))
# Removida chave externa por compliance corporativo 
# =================================================
def fragmentar_texto(texto, tamanho_chunk=1000, sobreposicao=200):
    """Fatia textos gigantes mantendo contexto (overlap) para a IA não perder o raciocínio."""
    chunks = []
    inicio = 0
    tamanho_texto = len(texto)

    while inicio < tamanho_texto:
        fim = inicio + tamanho_chunk
        chunks.append(texto[inicio:fim])
        inicio += (tamanho_chunk - sobreposicao)

    return chunks

def carregar_arquivos():
    documentos = []
    ids = []
    metadados = []
    
    diretorios_para_ler = [BASE_DIR, SCRIPTS_DIR]
    
    print("Vasculhando, lendo e fragmentando arquivos...")
    for diretorio in diretorios_para_ler:
        if not os.path.exists(diretorio):
            continue

        for root, _, files in os.walk(diretorio):
            if "vector_db" in root or "venv" in root:
                continue
                
            for file in files:
                if file.endswith((".md", ".txt", ".sql")):
                    caminho = os.path.join(root, file)
                    conteudo = None
                    
                    try:
                        with open(caminho, "r", encoding="utf-8") as f:
                            conteudo = f.read()
                    except UnicodeDecodeError:
                        try:
                            with open(caminho, "r", encoding="latin-1") as f:
                                conteudo = f.read()
                        except:
                            continue

                    if conteudo:
                        pedacos = fragmentar_texto(conteudo, tamanho_chunk=1000, sobreposicao=200)
                        for i, pedaco in enumerate(pedacos):
                            documentos.append(pedaco)
                            ids.append(f"{caminho}_chunk_{i}") 
                            metadados.append({"fonte": file, "caminho": caminho, "chunk": i})
                    
    return documentos, ids, metadados

def indexar_base():
    from chromadb.config import Settings
    print("Iniciando chromadb client...", flush=True)
    client = chromadb.PersistentClient(path=DB_DIR, settings=Settings(anonymized_telemetry=False))
    
    print("Iniciando embedding function...", flush=True)
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    
    try:
        client.delete_collection("base_conhecimento_ti")
    except Exception:
        pass
        
    print("Criando collection...", flush=True)
    collection = client.create_collection(
        name="base_conhecimento_ti",
        embedding_function=emb_fn
    )
    
    docs, ids, metadados = carregar_arquivos()
    
    if not docs:
        print("Nenhum documento encontrado.")
        return

    print(f"Indexando {len(docs)} fragmentos via API...")
    batch_size = 100
    for i in range(0, len(docs), batch_size):
        fim = min(i + batch_size, len(docs))
        print(f"Processando lote {i} até {fim}...")
        collection.upsert(
            documents=docs[i:fim],
            ids=ids[i:fim],
            metadatas=metadados[i:fim]
        )
        
    print(f"Sucesso absoluto! Banco vetorial atualizado e fragmentado em: {DB_DIR}")

if __name__ == "__main__":
    indexar_base()