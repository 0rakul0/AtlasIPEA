from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
embedd = SentenceTransformer('all-MiniLM-L6-v2', device=device)

client = QdrantClient(url="http://localhost:6333")



def consultar_banco(query_text, limit=5):
    # Gerando o vetor de consulta
    query_vector = embedd.encode(query_text).tolist()

    # Realizando a consulta com base no vetor de consulta
    response = client.search(
        collection_name="AtlasIpea",
        query_vector=query_vector,
        limit=limit
    )

    return response


if __name__ == "__main__":
    # Texto que você deseja buscar
    termo_busca = "mulher"
    resultados = consultar_banco(termo_busca)

    # Exibindo os resultados
    for resultado in resultados:
        print(f"ID: {resultado.id}\n Page Content: {resultado.payload['conteudo_da_pagina']}\n Score: {resultado.score}\n\n")
        # print(
        #     f"ID: {resultado.id}, Metadata: {resultado.payload['metadata']}, Page Content: {resultado.payload['conteudo_da_pagina']}")
