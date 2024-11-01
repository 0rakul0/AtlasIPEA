import argparse
import sys
from src import start_qdrant as sq
from src.ETL import Etl

def main():
    # Configura os argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Framework para extração e armazenamento de dados em Qdrant"
    )
    parser.add_argument(
        "--etl", action="store_true", help="Executa o processo de ETL para extrair e salvar dados"
    )
    parser.add_argument(
        "--upload", action="store_true", help="Faz upload dos dados para o banco Qdrant"
    )
    parser.add_argument(
        "--all", action="store_true", help="Executa o processo completo de ETL e upload"
    )

    args = parser.parse_args()

    # Verifica qual ação executar
    if args.all:
        execute_etl()
        upload_to_qdrant()
    elif args.etl:
        execute_etl()
    elif args.upload:
        upload_to_qdrant()
    else:
        print("Nenhuma ação especificada. Use --etl, --upload ou --all.")
        sys.exit(1)

def execute_etl():
    """Executa o processo de ETL."""
    try:
        etl = Etl()
        etl.run()
        print("Processo de ETL concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o processo de ETL: {e}")

def upload_to_qdrant():
    """Faz upload dos dados para o banco Qdrant."""
    try:
        sq.up_banco()
        print("Upload para o banco Qdrant concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante o upload para o banco Qdrant: {e}")

if __name__ == "__main__":
    main()
