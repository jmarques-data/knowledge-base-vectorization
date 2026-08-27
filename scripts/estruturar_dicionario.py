import os
from dotenv import load_dotenv

load_dotenv()

def formatar_dicionario():
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    knowledge_dir = os.getenv("KNOWLEDGE_PATH", os.path.join(ROOT_DIR, 'knowledge'))
    
    caminho_bruto = os.path.join(knowledge_dir, "dicionario_bruto.txt")
    caminho_oficial = os.path.join(knowledge_dir, "000_Dicionario_Oficial.md")
    
    if not os.path.exists(caminho_bruto):
        print(f"Erro: Crie o arquivo {caminho_bruto} com o texto do PDF primeiro.")
        return

    with open(caminho_bruto, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    print("Estruturando dados para o motor da IA...")
    with open(caminho_oficial, "w", encoding="utf-8") as out:
        out.write("# Dicionário Oficial de Dados MPV/SIVWIN\n\n")
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            
            # Limpa o lixo de formatação do PDF
            if not linha or "DICIONÁRIO DE DADOS" in linha or "Funções não documentadas" in linha or "Tabela Módulo" in linha or linha == "T":
                continue
                
            # Identifica o bloco de uma nova tabela
            if "Schema: dbo" in linha:
                # O nome da tabela sempre está na linha anterior neste PDF
                nome_tabela = linhas[i-1].strip()
                out.write(f"\n## Tabela: {nome_tabela}\n")
                out.write(f"> {linha}\n\n")
                
            elif "Coluna Tipo Req. Chave" in linha:
                out.write("**Estrutura de Colunas:**\n")
                
            else:
                # Se for o nome de uma tabela (que já foi capturado), pula
                if i < len(linhas) - 1 and "Schema: dbo" in linhas[i+1]:
                    continue 
                
                # Formata as colunas como itens de lista (o melhor formato para o RAG não se perder)
                partes = linha.split()
                tipos_dados = ['int', 'varchar', 'decimal', 'datetime', 'bit', 'float', 'uniqueidentifier', 'char', 'tinyint', 'bigint', 'numeric', 'varbinary', 'text', 'image', 'nvarchar']
                
                # Verifica se a linha é a declaração de uma coluna
                if len(partes) >= 3 and any(tipo in linha.lower() for tipo in tipos_dados):
                    coluna = partes[0]
                    tipo = partes[1]
                    detalhes = ' '.join(partes[2:])
                    out.write(f"- **{coluna}** (`{tipo}`): {detalhes}\n")
                else:
                    # Descrições adicionais da tabela
                    out.write(f"{linha}\n")

    print(f"Sucesso! Arquivo gerado: {caminho_oficial}")

if __name__ == "__main__":
    formatar_dicionario()