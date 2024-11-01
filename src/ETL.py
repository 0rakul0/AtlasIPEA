"""
esse script é dedicado para fazer a raspagem do atlas IPEA e salvar na pasta LAKE os txt dos PDFs
"""
import requests
from bs4 import BeautifulSoup as bs
import os
import pdfplumber
import pandas as pd


class Etl():
    def __init__(self):
        self.link = 'https://www.ipea.gov.br/atlasviolencia/publicacoes'
        self.destino = './LAKE'
        os.makedirs(self.destino, exist_ok=True)

    def run(self):
        self.extrator()
        dados = self.tratamento()
        self.salvar(dados)

    def extrator(self):
        # extrai o pdf do site
        response = requests.get(self.link)
        soup = bs(response.content, 'html.parser')

        pdf_links = soup.findAll('div', {'id': 'iniciodoconteudo'})

        print(pdf_links)

        for i, pdf_link in enumerate(pdf_links):
            pdf_response = requests.get(pdf_link)
            pdf_path = os.path.join(self.destino, f"document_{i}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            print(f"PDF {i + 1} baixado e salvo em {pdf_path}")

    def tratamento(self):
        # abre o pdf salvo e gera os dados de 'page','origem','paragrafo','capitulo','texto'
        dados = []
        for pdf_file in os.listdir(self.destino):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(self.destino, pdf_file)
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages, start=1):
                        text = page.extract_text()
                        if text:
                            # Divide o texto em parágrafos
                            for paragrafo_num, paragrafo_text in enumerate(text.split('\n\n'), start=1):
                                dados.append({
                                    'pagina': page_num,
                                    'origem': pdf_file,
                                    'paragrafo': paragrafo_num,
                                    'capitulo': 'Capítulo desconhecido',  # Placeholder para o capítulo
                                    'texto': paragrafo_text.strip()
                                })
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
