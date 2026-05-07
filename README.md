# Book Interpreter.

> Converse sobre qualquer livro em PDF usando Inteligência Artificial.

Book Interpreter é um assistente de leitura inteligente desenvolvido em Python. Ele permite que você faça perguntas sobre qualquer livro em formato PDF e receba respostas precisas baseadas **exclusivamente no conteúdo da obra** — sem invenções, sem achismos.

---

## Como funciona.

O programa utiliza a técnica **RAG (Retrieval-Augmented Generation)**:

```
PDF;
 ↓
Texto extraído página por página;
 ↓
Dividido em chunks de 1000 caracteres (com 200 de sobreposição);
 ↓
Cada chunk convertido em vetor semântico (embedding);
 ↓
Vetores armazenados no ChromaDB;
 ↓
Usuário faz uma pergunta;
 ↓
Pergunta convertida em vetor → busca os 22 trechos mais relevantes;
 ↓
Trechos + pergunta enviados ao LLaMA 3.3 70B via Groq;
 ↓
Resposta baseada apenas no conteúdo do livro.
```

---

## Tecnologias.

| Biblioteca | Versão | Função |
|---|---|---|
| `PyMuPDF` | ≥ 1.23 | Extração de texto do PDF |
| `ChromaDB` | ≥ 0.4 | Banco de dados vetorial |
| `sentence-transformers` | ≥ 2.2 | Geração de embeddings semânticos |
| `Groq` | ≥ 0.9 | Comunicação com a API do LLaMA 3.3 70B |

**Modelo de IA:** `llama-3.3-70b-versatile` via [Groq](https://console.groq.com) (gratuito)  
**Modelo de embedding:** `all-MiniLM-L6-v2` (leve, rápido, eficiente)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/KauaLasco/BOOK-INTERPRETER
cd BOOK-INTERPRETER
```

### 2. Instale as dependências

```bash
pip install pymupdf chromadb groq sentence-transformers
```

### 3. Configure sua API Key do Groq

Crie uma conta gratuita em [console.groq.com](https://console.groq.com), gere uma API Key e insira no código:

```python
client = Groq(api_key="sua-chave-aqui")
```

> ⚠️ **Nunca suba sua API Key para o GitHub.** Use variáveis de ambiente ou um arquivo `.env`.

### 4. Adicione o livro

Coloque o arquivo PDF na pasta do projeto com o nome `livro.pdf`, ou altere a variável `caminho` no código:

```python
caminho = "seu_livro.pdf"
```

---

## Como usar

```bash
python main.py
```

O programa irá:
1. Extrair e processar o texto do PDF;
2. Criar o banco de vetores;
3. Aguardar suas perguntas no terminal.

```
Extraindo texto...
187 chunks criados. Indexando vetores...
Pronto! Você já pode realizar as suas perguntas.

Realize sua pergunta ou digite 'sair' para encerrar o programa: Qual é o tema central do livro?

 O tema central aborda...
```

Digite `sair` para encerrar o programa.

---

## Requisitos

- Python 3.9 ou superior;
- Conexão com a internet (para a API do Groq);
- Chave de API gratuita do Groq;
- Arquivo PDF do livro na pasta do projeto.

---

## Estrutura do projeto

```
book-interpreter/
├── main.py        # Código principal
├── livro.pdf      # Seu livro (não suba para o GitHub)
├── .gitignore     # Ignora o PDF e a API Key
└── README.md      # Este arquivo
```

### `.gitignore` recomendado

```
livro.pdf
.env
__pycache__/
*.pyc
```

---

## Limitações

- O programa lê apenas PDFs com texto selecionável. PDFs escaneados (imagens) precisam de OCR;
- O banco de vetores é criado em memória e resetado a cada execução;
- O contexto enviado à IA é limitado aos 22 trechos mais relevantes por pergunta.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
