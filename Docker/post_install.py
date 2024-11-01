import os
import subprocess
import sys


def check_docker_installed():
    """Verifica se o Docker e o Docker Compose estão instalados."""
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Docker ou Docker Compose não está instalado. Por favor, instale-os e tente novamente.")
        sys.exit(1)


def create_data_directory():
    """Cria o diretório para armazenar os dados do Qdrant se ele não existir."""
    if not os.path.exists('./qdrant_data'):
        os.makedirs('./qdrant_data', exist_ok=True)
        print("Diretório './qdrant_data' criado.")
    else:
        print("O diretório './qdrant_data' já existe. Os dados existentes não serão apagados.")


def is_qdrant_running():
    """Verifica se o contêiner do Qdrant já está em execução."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=qdrant", "--format", "{{.Names}}"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Se o output não for vazio, o contêiner está rodando
        return bool(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar se o contêiner do Qdrant está em execução: {e}")
        sys.exit(1)


def run_docker_compose():
    """Executa o Docker Compose para iniciar o Qdrant."""
    check_docker_installed()
    create_data_directory()

    if is_qdrant_running():
        print("O contêiner do Qdrant já está em execução.")
        print("Você pode acessá-lo em: http://localhost:6333/dashboard")
    else:
        try:
            # Executa o comando docker-compose
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("Qdrant iniciado com sucesso.")
            print("Você pode acessá-lo em: http://localhost:6333/dashboard")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar Docker Compose: {e}")
            sys.exit(1)


if __name__ == "__main__":
    run_docker_compose()
