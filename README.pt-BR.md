# Knowledge Base — Pipeline de Ingestão e Vetorização de Dados

Pipeline desenvolvido em Python para transformar documentação técnica e tickets de suporte em representações vetoriais pesquisáveis, utilizando o ChromaDB como banco de dados vetorial local.

Este projeto explora os fundamentos de um futuro sistema de conhecimento baseado em IA: documentos não estruturados são processados, divididos em chunks, convertidos em embeddings e armazenados em um banco vetorial, criando a base para futuras aplicações de busca semântica, RAG e LLM.

> **Aviso:** Este é um projeto de portfólio. Todos os dados presentes no repositório são sintéticos e fictícios. Nenhum dado real de clientes, tickets ou informações internas de empresas está incluído.

---

## Arquitetura atual

```text
Documentos Markdown
        ↓
Ingestão de documentos
        ↓
Processamento de texto
        ↓
Chunking
        ↓
Geração de embeddings
        ↓
ChromaDB
        ↓
Armazenamento vetorial
```

### Implementado atualmente

* Ingestão de documentos Markdown
* Processamento e sanitização de texto
* Divisão de documentos em chunks
* Geração de embeddings
* Armazenamento vetorial utilizando ChromaDB
* Configuração de caminhos por variáveis de ambiente
* Dataset técnico sintético para demonstração
* Scripts para preparação da base de conhecimento

### Ainda não implementado

* RAG
* Integração com LLM
* PostgreSQL
* Agentes de IA
* Interface conversacional
* Camada de busca semântica

---

## Tecnologias

* **Python** — linguagem principal
* **ChromaDB** — banco de dados vetorial local
* **ONNX Runtime** — execução do modelo de embeddings
* **all-MiniLM-L6-v2** — modelo utilizado para geração de embeddings
* **python-dotenv** — gerenciamento de configurações por variáveis de ambiente
* **Regular Expressions (`re`)** — processamento e sanitização de texto
* **Markdown** — formato utilizado como fonte de conhecimento

---

## Como funciona

O pipeline recebe documentos Markdown contendo informações técnicas e os transforma em dados que podem ser armazenados e posteriormente pesquisados semanticamente.

### 1. Ingestão

Os arquivos Markdown presentes em `knowledge/` são localizados e carregados pelo pipeline.

### 2. Processamento

Os documentos passam por etapas de limpeza e processamento de texto.

### 3. Chunking

Documentos maiores são divididos em partes menores.

Atualmente, o projeto utiliza uma estratégia baseada em quantidade fixa de caracteres, com sobreposição entre os chunks.

```text
Documento
    ↓
Chunk 1
    ↓
Chunk 2
    ↓
Chunk 3
    ↓
...
```

A sobreposição ajuda a preservar o contexto entre partes consecutivas do documento.

### 4. Embeddings

Cada chunk é convertido em uma representação vetorial utilizando o modelo de embeddings.

Conceitualmente:

```text
"Erro de conexão com banco de dados"
              ↓
          Embedding
              ↓
     [representação vetorial]
```

Essa representação permite comparar diferentes textos com base em similaridade semântica.

### 5. ChromaDB

Os chunks e seus respectivos embeddings são armazenados no ChromaDB.

O banco vetorial é gerado localmente durante a execução e não faz parte do repositório Git.

---

## Estrutura do projeto

```text
project/
│
├── knowledge/
│   ├── tickets/
│   │   ├── ticket_7777_ssl_expired.md
│   │   ├── ticket_8834_db_lock.md
│   │   └── ticket_9912_camera_offline.md
│   │
│   ├── 000_Dicionario_Oficial.md
│   ├── 001_Troubleshooting_SGV_Limpo.md
│   └── dicionario_bruto.txt
│
├── scripts/
│   ├── estruturar_dicionario.py
│   ├── preparar_scripts_sql.py
│   └── sanitizar_tickets.py
│
├── src/
│   └── ingestion/
│       └── vetorizar_base.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Crie um ambiente virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o `.env.example` para `.env`.

#### Windows

```bash
copy .env.example .env
```

#### Linux / macOS

```bash
cp .env.example .env
```

Ajuste os caminhos caso seja necessário.

---

## Requisito adicional no Windows

O ChromaDB utiliza o ONNX Runtime para executar a geração de embeddings.

Dependendo do ambiente Windows, pode ser necessário instalar:

**Microsoft Visual C++ Redistributable 2015–2022**

Sem as bibliotecas necessárias do runtime do Visual C++, o ONNX Runtime pode apresentar erros relacionados ao carregamento de DLLs.

Esse requisito depende do ambiente local.

---

## Utilização

### 1. Preparação dos documentos

Execute os scripts de preparação:

```bash
python scripts/sanitizar_tickets.py
python scripts/estruturar_dicionario.py
python scripts/preparar_scripts_sql.py
```

Os scripts processam os documentos sintéticos presentes no diretório `knowledge/`.

### 2. Vetorização

Execute o pipeline principal:

```bash
python src/ingestion/vetorizar_base.py
```

O processo realiza:

```text
Markdown
   ↓
Processamento
   ↓
Chunking
   ↓
Embeddings
   ↓
ChromaDB
```

O diretório `vector_db/` será criado localmente durante a execução.

Esse diretório é um artefato gerado e está configurado no `.gitignore`.

---

## Dataset

Para evitar exposição de informações privadas, o projeto utiliza exclusivamente dados sintéticos.

Os exemplos simulam cenários técnicos como:

* problemas de rede;
* câmeras indisponíveis;
* expiração de certificados SSL;
* bloqueios de firewall;
* deadlocks em bancos de dados;
* procedimentos de troubleshooting.

Os dados foram criados especificamente para demonstrar o funcionamento do pipeline e não representam clientes ou ambientes reais.

---

## Segurança

A versão pública do projeto não contém:

* tickets reais;
* dados de clientes;
* documentação interna;
* credenciais;
* API keys;
* tokens;
* bancos vetoriais de produção;
* informações proprietárias;
* caminhos pessoais da máquina de desenvolvimento.

Dados reais utilizados durante o desenvolvimento permanecem fora do repositório público.

O `.gitignore` também impede que artefatos locais, como `.env`, ambientes virtuais e `vector_db/`, sejam adicionados ao Git.

---

## Limitações atuais

O projeto ainda está em uma etapa inicial de construção.

### Testes automatizados

A estrutura de testes existe, mas uma suíte completa de testes automatizados ainda não foi implementada.

### Chunking

A estratégia atual utiliza divisão baseada em quantidade de caracteres.

Isso funciona para a demonstração, mas pode dividir frases ou estruturas Markdown em pontos pouco naturais.

Uma futura implementação poderá utilizar chunking baseado em:

* títulos Markdown;
* parágrafos;
* seções;
* estrutura semântica;
* tamanho combinado com contexto.

### Busca semântica

O pipeline atual gera e armazena os embeddings, mas ainda não possui uma camada completa de busca semântica voltada ao usuário.

### RAG

O projeto ainda não possui uma implementação de Retrieval-Augmented Generation.

### LLM

Nenhum modelo de linguagem está integrado atualmente.

---

# Roadmap

O objetivo futuro é transformar o pipeline em um sistema completo de conhecimento baseado em IA.

## 1. Busca semântica

Implementar uma camada de retrieval capaz de receber uma consulta e encontrar os chunks mais relevantes no ChromaDB.

```text
Pergunta
   ↓
Embedding da pergunta
   ↓
Busca no ChromaDB
   ↓
Chunks relevantes
```

## 2. RAG

Adicionar uma arquitetura de Retrieval-Augmented Generation.

```text
Pergunta
   ↓
Busca semântica
   ↓
Contexto relevante
   ↓
Construção do prompt
   ↓
LLM
   ↓
Resposta
```

## 3. Integração com LLM

Adicionar um modelo de linguagem para gerar respostas utilizando o contexto recuperado da base de conhecimento.

Possíveis provedores incluem:

* OpenAI
* Anthropic
* Gemini
* outros modelos compatíveis

## 4. Banco de dados híbrido

Adicionar PostgreSQL para armazenar informações estruturadas enquanto o ChromaDB continua responsável pelo armazenamento vetorial e pela busca semântica.

Arquitetura planejada:

```text
             Sistema de Conhecimento
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        PostgreSQL            ChromaDB
     Dados estruturados    Dados semânticos
             │                   │
             └─────────┬─────────┘
                       ↓
                Hybrid Retrieval
                       ↓
                      RAG
                       ↓
                      LLM
```

## 5. Interface de agente

Criar uma interface conversacional capaz de utilizar a base de conhecimento como um assistente técnico.

---

## Objetivo do projeto

Este projeto faz parte do meu estudo prático sobre a integração entre:

```text
Python
   +
Processamento de dados
   +
Bases de conhecimento
   +
Embeddings
   +
Bancos vetoriais
   +
RAG
   +
LLMs
```

A implementação atual representa a fundação dessa arquitetura.

O objetivo é evoluir o projeto gradualmente, validando cada camada antes de adicionar a próxima.

---

## Status

**Em desenvolvimento**

### Implementado

* [x] Ingestão de Markdown
* [x] Processamento de texto
* [x] Chunking
* [x] Geração de embeddings
* [x] Integração com ChromaDB
* [x] Dataset sintético
* [x] Configuração por ambiente

### Roadmap

* [ ] Busca semântica
* [ ] RAG
* [ ] Integração com LLM
* [ ] PostgreSQL
* [ ] Hybrid Retrieval
* [ ] Agente de IA
* [ ] Testes automatizados
