from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
embedd = SentenceTransformer('all-MiniLM-L6-v2', device=device)

client = QdrantClient(url="http://localhost:6333")


def buscar_semantico(query, top_k=10):
    query_vector = embedd.encode(query).tolist()

    # Realiza a busca no Qdrant
    resultados = client.search(
        collection_name="AtlasIpea",
        query_vector=query_vector,
        limit=top_k
    )

    documentos_encontrados = []
    for ponto in resultados:
        documento = {
            'id': ponto.id,
            'distancia': ponto.score,
            'metadata': ponto.payload['metadata'],
            'conteudo_da_pagina': ponto.payload['conteudo_da_pagina']
        }
        documentos_encontrados.append(documento)
    return documentos_encontrados

def listar_capitulos_da_busca(query, top_k=10):
    documentos = buscar_semantico(query, top_k)
    capitulos = [doc['metadata']['capitulo'] for doc in documentos if 'metadata' in doc and 'capitulo' in doc['metadata']]
    capitulos = set(capitulos)
    return capitulos

def listar_chaves_da_busca(query, top_k=10):
    documentos = buscar_semantico(query, top_k)
    capitulos = [doc['metadata']['key'] for doc in documentos]
    cap = set()

    for capitulo in capitulos:
        for c in capitulo:
            cap.add(c)

    return cap

if __name__ == "__main__":
    consulta = "mulher"
    resultados = buscar_semantico(consulta)

    # Exibir os resultados
    for doc in resultados:
        print(f"Metadata: {doc['metadata']}, Conteúdo: {doc['conteudo_da_pagina']}\n")

    capitulos_encontrados = listar_capitulos_da_busca("Mulheres")
    for capitulo in capitulos_encontrados:
        print(capitulo)

    print('\n')
    capitulos_chave_encontrados = listar_chaves_da_busca("mulher")
    for capitulo in capitulos_chave_encontrados:
        print(capitulo)