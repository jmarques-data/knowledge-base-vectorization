import os
import re
from collections import defaultdict

def categorizar_ticket(texto):
    texto_lower = texto.lower()
    
    # Pesos e heurísticas de palavras-chave para clusters de incidentes
    cat_mpv = ["ffmpeg", "timeout 900", "espaço insuficiente", "mpvservice", "converted", "112", "conversão"]
    cat_hardware = ["físico", "cabo", "fonte", "câmera", "nvr offline", "dvr", "hd", "disco c:"]
    cat_rede = ["conexão de transporte", "host remoto", "firewall", "antivírus", "compartilhamento", "rede"]
    cat_software = ["sivwin", "banco", "sivpp", "relatório", "mpvform", "forms", "gerencial", "states.json"]

    pontos = {
        "Falhas no Serviço MPV (FFmpeg e Conversão)": sum(1 for p in cat_mpv if p in texto_lower),
        "Problemas Físicos (Hardware/Câmera/DVR)": sum(1 for p in cat_hardware if p in texto_lower),
        "Falhas de Rede, Permissão e Conectividade": sum(1 for p in cat_rede if p in texto_lower),
        "Erros de Software (SivWin/Forms/SGV)": sum(1 for p in cat_software if p in texto_lower)
    }
    
    melhor_categoria = max(pontos, key=pontos.get)
    # Se nenhuma keyword bateu ou houve empate em zero
    if pontos[melhor_categoria] == 0:
        return "Outros Incidentes / Análise Manual"
    
    return melhor_categoria

def gerar_solucao_consolidada(categoria):
    matriz = {
        "Falhas no Serviço MPV (FFmpeg e Conversão)": "1. Pare o serviço MPVService.\n2. Verifique o espaço em disco (Erro 112) e limpe a pasta 'Converted'.\n3. Crie a Task de reinício automático (timeout /t 5).",
        "Problemas Físicos (Hardware/Câmera/DVR)": "1. Valide a alimentação (fonte/cabo RJ45) da câmera.\n2. Reinicie o DVR/NVR.\n3. Se o HD falhar, isolem a pasta no CMS/SGV provisoriamente.",
        "Falhas de Rede, Permissão e Conectividade": "1. Adicione exceções no Firewall/Antivírus para a pasta Temp e para o IP do storage.\n2. Conceda permissão de 'Controle Total' para a pasta de gravação.",
        "Erros de Software (SivWin/Forms/SGV)": "1. Verifique se o MPVForm está executando.\n2. Cheque a integridade do arquivo states.json e corrija quebras de array.\n3. Valide os logs de retorno (WebService Log)."
    }
    return matriz.get(categoria, "Analisar o histórico bruto no nível do ticket.")

def extrair_secoes(text):
    sintoma = "Não estruturado - leitura recomendada."
    causa = "Mapeamento pendente."
    solucao = "Consultar fluxo no corpo."
    
    m_sintoma = re.search(r'(Problema:|Diagnóstico Inicial:|Sintoma:)(.*?)(?=(Causa Raiz:|Análise de logs|Ações Corretivas|Solução:|Status Atual:|TRATATIVA|$))', text, re.IGNORECASE | re.DOTALL)
    if m_sintoma: sintoma = m_sintoma.group(2).strip()
    
    m_causa = re.search(r'(Causa Raiz:|Análise de logs e causa raiz:|Causa provável:)(.*?)(?=(Ações Corretivas|Solução:|Status Atual:|TRATATIVA|$))', text, re.IGNORECASE | re.DOTALL)
    if m_causa: causa = m_causa.group(2).strip()
        
    m_solucao = re.search(r'(Ações Corretivas Executadas:|Ações Realizadas:|Soluções e Prevenções Aplicadas:|Solução:|Status Atual:)(.*)', text, re.IGNORECASE | re.DOTALL)
    if m_solucao: solucao = m_solucao.group(2).strip()
    
    # Fallback para extrair algo útil se o analista não usou keywords
    if len(text) > 200 and "Não estruturado" in sintoma:
        sintoma = text[:250] + "..."
        solucao = "..." + text[-250:]
        
    return sintoma, causa, solucao

def arquiteto_sgv_pipeline():
    from dotenv import load_dotenv
    load_dotenv()
    
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    knowledge_dir = os.getenv("KNOWLEDGE_PATH", os.path.join(ROOT_DIR, 'knowledge'))
    
    input_file = os.path.join(knowledge_dir, '001_Troubleshooting_SGV_Limpo.md')
    tickets_dir = os.path.join(knowledge_dir, 'tickets')
    os.makedirs(tickets_dir, exist_ok=True)
    output_file = os.path.join(tickets_dir, '002_SGV_KnowledgeBase_Consolidada.md')

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro crítico: Arquivo {input_file} não encontrado na raiz.")
        return

    raw_tickets = re.split(r'(?m)^## Ticket #', content)
    
    # Agrupador (Matriz de Erros)
    base_conhecimento = defaultdict(list)
    processados = 0

    for t in raw_tickets:
        if not t.strip(): continue
        
        lines = t.split('\n')
        ticket_id = lines[0].strip()
        body = '\n'.join(lines[1:])
        
        # Filtro de ruído e lixo (sem alterar o anterior)
        body_lower = body.lower()
        if any(w in body_lower for w in ["aguardando o cliente", "abandonado"]):
            continue
            
        cleaned_lines = []
        for line in body.split('\n'):
            if re.search(r'(Bot Otimiza|Clique no setor|1, 2, 3|VOLTAR|Aguarde um momento)', line, re.IGNORECASE): continue
            line = re.sub(r'Senha:\s*\S+', 'Senha: [REMOVIDA]', line, flags=re.IGNORECASE)
            line = re.sub(r'(\(?\d{2}\)?\s*\d{4,5}-?\d{4})', '[TELEFONE REMOVIDO]', line)
            if line.strip(): cleaned_lines.append(re.sub(r'^>\s*', '', line).strip())
                
        text_limpo = '\n'.join(cleaned_lines)
        if len(text_limpo) < 200: continue
        
        # Arquitetura de Dados: Categorização e Classificação
        categoria = categorizar_ticket(text_limpo)
        sintoma, causa, solucao = extrair_secoes(text_limpo)
        
        base_conhecimento[categoria].append({
            "id": ticket_id,
            "sintoma": sintoma,
            "causa": causa,
            "solucao": solucao
        })
        processados += 1

    # Geração do Arquivo Estruturado com Visão Macro
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# Base de Conhecimento SGV - Agrupada por Módulo (Arquitetura RAG)\n\n")
        
        for categoria, tickets in base_conhecimento.items():
            ids_tickets = [tk['id'] for tk in tickets]
            
            out.write(f"## Módulo/Erro: {categoria}\n")
            out.write(f"**Volume de Casos Encontrados:** {len(tickets)}\n")
            out.write(f"**Matriz de IDs Associados:** {', '.join(ids_tickets[:30])}{' ...' if len(ids_tickets)>30 else ''}\n\n")
            
            out.write("### Base de Soluções Consolidadas (Troubleshooting Padrão)\n")
            out.write(f"{gerar_solucao_consolidada(categoria)}\n\n")
            out.write("---\n\n")
            
            # Detalhamento Vetorial para o LLM consumir caso exija profundidade
            out.write("### Histórico e Contexto Vetorial\n")
            for tk in tickets:
                out.write(f"#### Ticket #{tk['id']}\n")
                out.write(f"**Sintoma:** {tk['sintoma']}\n")
                out.write(f"**Causa Raiz:** {tk['causa']}\n")
                out.write(f"**Solução Prática:** {tk['solucao']}\n\n")
            
            out.write("========================================================================\n\n")
            
    print(f"Arquitetura de Dados aplicada com sucesso. Tickets consolidados: {processados}")
    print(f"Acesse o arquivo estruturado em: {output_file}")

if __name__ == "__main__":
    arquiteto_sgv_pipeline()