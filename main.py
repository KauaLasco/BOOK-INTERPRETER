import fitz #Usado para abrir e ler arquivos PDF, extraindo o texto de cada página.
import chromadb #Banco de dados vetorial. Armazena os chunks do livro convertidos em vetores numéricos.
import anthropic #SDK oficial da Anthropic. Comunica com a API do Claude e envia perguntas.
from sentence_transformers import SentenceTransformer #Classe importada da biblioteca "sentence_transformers".
#Carrega um modelo de linguagens capaz de converter textos em vetores numéricos (embeddings), representando
#o significa semântico  de cada trecho.

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
