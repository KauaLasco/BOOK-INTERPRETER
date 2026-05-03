import fitz #Usado para abrir e ler arquivos PDF, extraindo o texto de cada página.
import chromadb #Banco de dados vetorial. Armazena os chunks do livro convertidos em vetores numéricos.
from groq import Groq #SDK oficial do Groq. Comunica com a API do Groq e envia perguntas.
from sentence_transformers import SentenceTransformer #Classe importada da biblioteca "sentence_transformers".
#Carrega um modelo de linguagens capaz de converter textos em vetores numéricos (embeddings), representando
#o significa semântico  de cada trecho.

#Extrai os caracteres do livros em chunks de 1000 caracteres. Repete 200 caracteres do chunk anterior no ínicio
#do próximo para que uma ideia não seja cortada no meio de dois chunks.
def extrair_chunks(caminho_pdf, tamanho_chunk=1000, sobreposicao=200):
    doc = fitz.open(caminho_pdf)
    texto_total = ""

    for pagina in doc:
        texto_total += pagina.get_text()
    doc.close()

    chunks = []
    inicio = 0
    while inicio < len(texto_total):
        fim = inicio + tamanho_chunk
        chunk = texto_total[inicio:fim]
        chunks.append(chunk)
        inicio += tamanho_chunk - sobreposicao
    
    return chunks

#Converte os chunks em vetores (embedding), tornando temas/contextos semelhantes matemáticamente próximos
#e os adiciona no banco.
def criar_banco(chunks):
    modelo = SentenceTransformer("all-MiniLM-L6-v2") #Carrega um modelo de embedding leve e eficiente.
    client = chromadb.Client()
    colecao = client.create_collection("livro")

    for i, chunk in enumerate(chunks):
        embedding = modelo.encode(chunk).tolist()
        colecao.add(documents=[chunk], embeddings=[embedding], ids=[str(i)]) #Insere o chunk no banco.

    return colecao, modelo

#Recebe a pergunta do usuário e a converte em vetor para realizar a busca.
def buscar_trechos(pergunta, colecao, modelo, n_resultados=22):
    embedding_pergunta = modelo.encode(pergunta).tolist() #Converte a pergunta em vetor.
    resultados = colecao.query(query_embeddings=[embedding_pergunta], n_results=n_resultados)

    return "\n\n".join(resultados["documents"][0])

#Interpreta a pergunta do usuário e o fornece uma resposta baseado na interpretação do livro.
def perguntar(pergunta, colecao, modelo_embedding):
    contexto = buscar_trechos(pergunta, colecao, modelo_embedding)

    client = Groq(api_key="") # Insira sua API KEY do Groq.
    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        max_tokens=1024, 
        messages=[{
            "role": "user", 
            "content": f"""Você é um assistente que interpreta livros.

Trechos relevantes do livro:
{contexto}

Pergunta: {pergunta}

Responda com base apenas nos trechos fornecidos."""
            }])

    return resposta.choices[0].message.content

#Bloco principal do código, no qual realiza a execução do mesmo.
caminho = "livro.pdf"
print("Extraindo texto...")
chunks = extrair_chunks(caminho)

print(f"{len(chunks)} chunks criados. Indexando vetores...")
colecao, modelo_embedding = criar_banco(chunks)

print("Pronto! Você já pode realizar as suas perguntas.\n")

while True:
    pergunta = input("Realize sua pergunta ou digite 'sair' para encerrar o programa: ")
    if pergunta.lower() == "sair":
        break
    resposta = perguntar(pergunta, colecao, modelo_embedding)
    print(f"\n {resposta}\n")