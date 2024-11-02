# AtlasIPEA

Framework para extração e armazenamento de dados em Qdrant.

## Descrição:
Este projeto é dedicado a extrair dados de PDFs, estruturá-los em um formato adequado e armazená-los em um banco de dados vetorial utilizando o Qdrant, possibilitando consultas eficientes e organizadas.

---

## Sumário
1. [Objetivo](#objetivo)
2. [Instalações](#instalacoes)
3. [Scripts Principais](#scripts-principais)
4. [Uso do Framework](#uso-do-framework)
5. [Estrutura dos Dados](#estrutura-dos-dados)
6. [Banco Vetorial](#banco-vetorial)
7. [LLM](#llm)
8. [Autor](#autor)

---

## Objetivo:
Desenvolver um processo de ETL para extrair dados de publicações disponíveis em PDF e armazená-los no Qdrant em uma estrutura vetorial para consultas rápidas.

---

## Instalações:
Para instalar as dependências necessárias:

```bash
pip install qdrant-client sentence-transformers tqdm pandas beautifulsoup4 pdfplumber
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## Scripts Principais

### `script_qdrant.py`
Este script gera o banco de dados no Qdrant, com as principais funções:
- Instanciar o banco de dados e configurar a coleção.
- Gerar chunks (blocos de texto) para armazenamento.
- Converter dados de CSV para documentos.
- Fazer upload para o banco de dados.

### `ETL.py`
Script de Extração, Transformação e Carregamento (ETL) para extrair textos de PDFs, estruturá-los e salvá-los na pasta `./LAKE`.
---

## Uso do Framework

Agora você pode executar o framework utilizando argumentos de linha de comando:

- **Executar somente o processo de ETL**:
  
  ```bash
  python main.py --etl
  ```

- **Fazer somente o upload para o banco Qdrant**:

  ```bash
  python main.py --upload
  ```

- **Executar o processo completo (ETL e upload)**:

  ```bash
  python main.py --all
  ```

Essas opções permitem uma execução mais flexível e controlada do fluxo do framework.

---

## Estrutura dos Dados
O objetivo do ETL é extrair os textos e organizá-los no formato JSON com a seguinte estrutura:

```json
{
    "chunk": [
        {
            "pagina": 1,
            "origem": "example.pdf",
            "paragrafo": 1,
            "capitulo": "Introdução",
            "texto": "Este é um texto de exemplo."
        }
    ]
}
```

Cada arquivo processado é salvo na pasta `./LAKE`.

---

## Banco Vetorial:
O banco de dados vetorial utilizado é o Qdrant, configurado via Docker. Para iniciar o banco, execute o comando:

```bash
cd ./Docker
docker-compose up
```

Nome do banco: `AtlasIpea`

---

## LLM:
A versão do LLM utilizada é o **Llama 3.1**.

---

## Autor:
Jefferson Silva dos Anjos  
GitHub: [0rakul0](https://github.com/0rakul0)
