"""
esse script é dedicado para fazer o ETL e salvar na pasta LAKE os txt dos PDFs
"""
import requests
from bs4 import BeautifulSoup as bs
import os
import pdfplumber
import pandas as pd


class Etl():
    def __init__(self):
        self.destino = './LAKE'
        os.makedirs(self.destino, exist_ok=True)

    def run(self):
        self.extrator()
        dados = self.tratamento()
        self.salvar(dados)

    def extrator(self):
       pass

    def tratamento(self):
        # abre o pdf salvo e gera os dados de 'page','origem','paragrafo','capitulo','texto'
        df = pd.DataFrame([
            {
                'page': 1,
                'origem': 'example.pdf',
                'paragrafo': 1,
                'capitulo': 'Introdução',
                'texto': 'Este é um texto de exemplo.'
            }
        ])
        return df

    def salvar(self, df):
        pass


if __name__ == "__main__":
    etl = Etl()
    etl.run()
