# Atlas IPEA - Framework de Extração e Banco Vetorial

Este projeto visa estruturar e armazenar publicações do **Atlas da Violência** em um banco de vetores utilizando **Qdrant**.

## Sumário
1. [Objetivo](#objetivo)
2. [Instalações](#instalações)
3. [Componentes do Projeto](#componentes-do-projeto)
4. [Banco de Vetores](#banco-de-vetores)
5. [LLM](#llm)
6. [Autor](#autor)

## Objetivo
O projeto automatiza a extração, tratamento e armazenamento de informações contidas em documentos PDF da publicação *Atlas da Violência* em uma estrutura vetorial que pode ser usada para consultas avançadas.
[link do atlas](https://www.ipea.gov.br/atlasviolencia/publicacoes)
___
## Projeto:
1. **Instalações**: 
    - para as instalações minimas

```bash
pip install qdrant-client sentence-transformers tqdm pandas BeautifulSoup4 pdfplumber
```
--- 
## Componentes do Projeto
### SCRIPT_QDRANT
Este script cria e configura o banco de dados com a coleção AtlasIpea. Ele inclui funções para:

Instanciar o banco
Gerar chunks de dados
Converter arquivos CSV para documentos
Realizar upload dos dados para o banco

### DOC
estrutura baseica do documento 
```
class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata
```
está localizado na pasta util

### ETL
o objetivo de extrair os textos é deixar na estrutura de 
```py
chunk= [
   {
       'pagina': 1,
       'origem': 'example.pdf',
       'paragrafo': 1,
       'capitulo': 'Introdução',
       'texto': 'Este é um texto de exemplo.'
   }
]
```
Os dados processados são salvos na pasta ./LAKE.

### Diretório LAKE
A pasta LAKE armazena os arquivos extraídos dos PDFs para processamento.

## Banco Vetorial
O banco de dados Qdrant é utilizado para armazenar as informações em um Docker. Para iniciar o banco, execute:

bash

```
cd ./Docker
docker-compose up
```
## LLM
Este projeto usa o Llama 3.1 como modelo de linguagem.

## Autor
Jefferson Silva dos Anjos, [GitHub - 0rakul0](http://github.com/0rakul0)
