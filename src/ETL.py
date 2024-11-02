"""
esse script é dedicado para fazer a raspagem do atlas IPEA e salvar na pasta LAKE os txt dos PDFs

https://www.ipea.gov.br/atlasviolencia/publicacoes
"""
import os
from collections import Counter
import pdfplumber
import pandas as pd
import re
from tqdm import tqdm


class Etl():
    def __init__(self):
        self.origem = r'../LAKE/RAW/'
        self.destino = r'../LAKE/TRAT/'
        os.makedirs(self.origem, exist_ok=True)
        os.makedirs(self.destino, exist_ok=True)

    def run(self):
        dados, nome = self.extrator()
        df = self.tratamento(dados)
        self.salvar(df, nome)

    def extrair_sumario(self, pdf):
        sumario = {}
        sumario_regex = r'(?P<capitulo>\d+(\.\d+)?)\.?\s+(?P<titulo>[A-Za-zÀ-Ýà-ý\s\,\-\+]+)\s+\.*\s*(?P<pagina>\d+)'

        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if "SUMÁRIO" in text:
                text = "".join(text)
                linhas = re.findall(sumario_regex, text)

                for linha in linhas:
                    capitulo, _, titulo, pagina = linha
                    titulo = str(titulo).replace('\n', '').strip()
                    pagina = int(pagina)
                    sumario[capitulo] = {'titulo': titulo, 'pagina': pagina}
                break
        return sumario

    def criar_chunks(self, text, chunk_size, overlap):
        """Divide o texto em chunks com overlap baseado em palavras."""
        text = re.sub(r'\n+', ' ', text)
        palavras = text.split()
        chunks = []
        start = 0
        while start < len(palavras):
            end = min(start + chunk_size, len(palavras))
            chunk = ' '.join(palavras[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap

            if start >= len(palavras):
                break
        return chunks

    def extrator(self):
        dados = []
        arqs = os.listdir(self.origem)
        nome_arq = None
        for pdf_file in arqs:
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(self.origem, pdf_file)
                nome_arq = pdf_file.split('.')[0]
                with pdfplumber.open(pdf_path) as pdf:
                    sumario = self.extrair_sumario(pdf)
                    for page_num, page in tqdm(enumerate(pdf.pages, start=1)):
                        text = page.extract_text()
                        if text:
                            capitulo_atual = 'Capítulo desconhecido'
                            for cap, info in sumario.items():
                                if page_num >= info['pagina']:
                                    capitulo_atual = f"{cap}. {info['titulo']}"
                            pagina_texto = " ".join([
                                paragrafo.strip()
                                for paragrafo in text.split('\n\n') if paragrafo.strip()
                            ])
                            chunks = self.criar_chunks(pagina_texto, chunk_size=100, overlap=10)
                            for i, chunk in enumerate(chunks, start=1):
                                dados.append({
                                    'pagina': page_num,
                                    'origem': pdf_file,
                                    'capitulo': capitulo_atual,
                                    'texto': chunk
                                })
        return dados, nome_arq

    def contar_palavras(self, texto):
        palavras = re.findall(r'\b\w{6,}\b', texto.lower())
        return Counter(palavras)

    def tratamento(self, dados):
        df = pd.DataFrame(dados)
        df['texto'] = df['texto'].str.replace(r'\.+', '', regex=True)
        df['texto'] = df['texto'].str.replace(r'Sumário', '', regex=True)
        df = df[df['texto'].str.len() >= 40]
        df['key'] = df['texto'].apply(
            lambda texto: [palavra[0] for palavra in self.contar_palavras(texto).most_common(10)]
            )
        return df

    def salvar(self, df, nome):
        # salvar na pasta LAKE
        output_path = os.path.join(self.destino, f"{nome}.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"CSV criado com sucesso em {output_path}")

if __name__ == "__main__":
    etl = Etl()
    etl.run()
