import argparse
import sys
from Docker.post_install import run_docker_compose
from src import start_qdrant as sq
from src.ETL import Etl

def main():
    """Função principal que gerencia a execução do framework."""
    parser = argparse.ArgumentParser(
        description="Framework para extração e armazenamento de dados em Qdrant"
    )
    parser.add_argument(
        "--docker", action="store_true", help="Executa o processo do Docker para criar o storage"
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
        execute_docker()
        execute_etl()
        upload_to_qdrant()
    elif args.docker:
        execute_docker()
    elif args.etl:
        execute_etl()
    elif args.upload:
        upload_to_qdrant()
    else:
        print("Nenhuma ação especificada. Use --docker, --etl, --upload ou --all.")
        sys.exit(1)

def execute_docker():
    """Executa o processo do Docker para iniciar o Qdrant."""
    try:
        run_docker_compose()
        print("Docker iniciado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o processo do Docker: {e}")

def execute_etl():
    """Executa o processo de ETL para extrair e salvar dados."""
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
