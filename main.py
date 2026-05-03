import fitz #Usado para abrir e ler arquivos PDF, extraindo o texto de cada página.
import chromadb #Banco de dados vetorial. Armazena os chunks do livro convertidos em vetores numéricos.
import anthropic #SDK oficial da Anthropic. Comunica com a API do Claude e envia perguntas.
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

def criar_banco(chunks):
    modelo = SentenceTransformer("all-MiniLM-L6-v2") #Carrega um modelo de embedding leve e eficiente.
    client = chromadb.Client()
    colecao = client.create_collection("livro")

    for i, chunk in enumerate(chunks):
        embedding = modelo.encode(chunk).tolist()
        colecao.add(documents=[chunk], embeddings=[embedding], ids=[str(i)]) #Insere o chunk no banco.

    return colecao, modelo
