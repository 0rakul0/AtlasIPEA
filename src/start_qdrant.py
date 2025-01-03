# %% importações
import ast
import os
import re
from collections import Counter
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import warnings
from util.doc import Documento
import logging
from tqdm import tqdm
import pandas as pd
import torch
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

device = "cuda" if torch.cuda.is_available() else "cpu"
embedd = SentenceTransformer('all-MiniLM-L6-v2', device=device)

client = QdrantClient(url="http://localhost:6333")


# %% criação da coleção
if "AtlasIpea" not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name="AtlasIpea",
        vectors_config=models.VectorParams(
            size=embedd.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
        ),
    )

# %% chuncks dos textos extraidos
def gerador_chunks(nome_arq):
    """Retorna os chunks de dados a serem processados, seja a partir de um CSV ou de exemplo."""
    chunks = pd.read_csv(fr'../LAKE/TRAT/{nome_arq}', low_memory=False)
    return chunks

# %% gerando
def csv_para_documento(chuncks):
    documents = []
    for _, linha in chuncks.iterrows():
        linha = linha.to_dict()
        linha['key'] = ast.literal_eval(linha['key'])
        metadata = {
            'pagina': linha['pagina'],  # pagina da informção
            'key': linha['key'],  # tags do chunk
            'origem': linha['origem'],  # pdf da informação
            'capitulo': linha['capitulo']  # capitulo da informação
        }
        document = Documento(conteudo_da_pagina=linha['texto'], metadata=metadata)
        documents.append(document)
    return documents

#%% gera o banco com os dados
def up_banco():
    arq = os.listdir('../LAKE/TRAT/')
    for arquivo in arq:
        try:
            chuncks = gerador_chunks(arquivo)
            docs = csv_para_documento(chuncks)
            points = [
                models.PointStruct(
                    id=idx,
                    vector=embedd.encode(doc.conteudo_da_pagina).tolist(),
                    payload={'metadata': doc.metadata, 'conteudo_da_pagina': doc.conteudo_da_pagina}
                ) for idx, doc in tqdm(enumerate(docs))
            ]
            client.upload_points(
                collection_name="AtlasIpea",
                points=points
            )
            logging.info("Dados enviados com sucesso para o Qdrant.")
        except Exception as e:
            logging.error(f"Erro ao processar dados: {e}")

if __name__ == "__main__":
    up_banco()