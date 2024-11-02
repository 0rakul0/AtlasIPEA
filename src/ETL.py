"""
esse script é dedicado para fazer a raspagem do atlas IPEA e salvar na pasta LAKE os txt dos PDFs

https://www.ipea.gov.br/atlasviolencia/publicacoes
"""
import os
import pdfplumber
import pandas as pd
import re


class Etl():
    def __init__(self):
        self.destino = r'../LAKE/RAW/'
        os.makedirs(self.destino, exist_ok=True)

    def run(self):
        dados = self.extrator()
        df = self.tratamento(dados)
        self.salvar(df)

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

                    # Adiciona a entrada ao dicionário de sumário
                    sumario[capitulo] = {'titulo': titulo, 'pagina': pagina}
                break
        return sumario

    def extrator(self):
        dados = []
        arqs = os.listdir(self.destino)

        for pdf_file in arqs:
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(self.destino, pdf_file)

                with pdfplumber.open(pdf_path) as pdf:
                    sumario = self.extrair_sumario(pdf)

                    for page_num, page in enumerate(pdf.pages, start=1):
                        text = page.extract_text()

                        if text:
                            capitulo_atual = 'Capítulo desconhecido'
                            for cap, info in sumario.items():
                                if page_num >= info['pagina']:
                                    capitulo_atual = f"{cap}. {info['titulo']}"

                            for paragrafo_num, paragrafo_text in enumerate(text.split('.\n'), start=1):
                                paragrafo_text = paragrafo_text.replace('\n', ',')
                                if paragrafo_text not in 'Sumário':
                                    paragrafo = paragrafo_text.strip()
                                    paragrafo = re.sub(r'\.', '', paragrafo)
                                    dados.append({
                                        'pagina': page_num,
                                        'origem': pdf_file,
                                        'paragrafo': paragrafo_num,
                                        'capitulo': capitulo_atual,
                                        'texto': paragrafo
                                    })
        return dados

    def tratamento(self, dados):
        df = pd.DataFrame(dados)
        return df

    def salvar(self, df):
        # salvar na pasta LAKE
        output_path = os.path.join(self.destino, "dados_extracao.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"CSV criado com sucesso em {output_path}")


if __name__ == "__main__":
    etl = Etl()
    etl.run()
