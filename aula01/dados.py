"""Leitura dos arquivos CSV do projeto.
"""
import csv
from pathlib import Path

# Pasta onde este arquivo .py está. Assim o programa encontra o CSV
# mesmo quando é executado a partir de outra pasta (como no Streamlit Cloud).
PASTA = Path(__file__).parent
CAMINHO_LIVROS = PASTA / "livros.csv"

def ler_livros():
    livros = []
    with open(CAMINHO_LIVROS, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            livros.append(linha)
    return livros


if __name__ == "__main__":
    livros = ler_livros()
    print(f"Total de livros: {len(livros)}")
    print("Primeiro livro:", livros[0])

