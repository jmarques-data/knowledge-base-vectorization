import os
from dotenv import load_dotenv

load_dotenv()

# Caminho onde estão os seus scripts brutos
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETORIO_SCRIPTS = os.getenv("SQL_SCRIPTS_PATH", os.path.join(ROOT_DIR, "knowledge", "sql_scripts"))

def adicionar_cabecalhos():
    print("Iniciando a padronização dos scripts SQL...")
    arquivos_alterados = 0

    for root, _, files in os.walk(DIRETORIO_SCRIPTS):
        for file in files:
            if file.endswith((".txt", ".sql")):
                caminho = os.path.join(root, file)
                nome_sem_extensao = os.path.splitext(file)[0]
                
                # Tenta ler o arquivo (tratando acentos e codificações antigas do Windows)
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                except UnicodeDecodeError:
                    with open(caminho, 'r', encoding='latin-1') as f:
                        conteudo = f.read()

                # Verifica se já tem a nossa marcação para não duplicar o cabeçalho
                if "-- SCRIPT REFERENTE A:" not in conteudo:
                    cabecalho = f"-- ==========================================\n"
                    cabecalho += f"-- SCRIPT REFERENTE A: {nome_sem_extensao}\n"
                    cabecalho += f"-- ==========================================\n\n"
                    
                    novo_conteudo = cabecalho + conteudo
                    
                    # Salva o arquivo atualizado (padronizando para utf-8 para a IA ler melhor)
                    with open(caminho, 'w', encoding='utf-8') as f:
                        f.write(novo_conteudo)
                    
                    print(f"Cabeçalho adicionado: {file}")
                    arquivos_alterados += 1

    print(f"\nOperação concluída! {arquivos_alterados} scripts foram preparados para a IA.")

if __name__ == "__main__":
    adicionar_cabecalhos()