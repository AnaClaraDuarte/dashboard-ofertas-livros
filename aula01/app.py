"""Dashboard de Livros: app Streamlit.
"""

import streamlit as st

from dados import ler_livros


def converter_preco(texto):
    return float(texto.replace("£", ""))


def calcular_preco_medio(livros):
    soma = 0
    for livro in livros:
        soma = soma + converter_preco(livro["preco"])
    return soma / len(livros)


def contar_cinco_estrelas(livros):
    contador = 0
    for livro in livros:
        if livro["nota"] == "Five":
            contador = contador + 1
    return contador


def encontrar_mais_caro(livros):
    mais_caro = livros[0]  
    for livro in livros:
        if converter_preco(livro["preco"]) > converter_preco(mais_caro["preco"]):
            mais_caro = livro  
    return mais_caro


livros = ler_livros()
mais_caro = encontrar_mais_caro(livros)

st.title("📚 Dashboard de Livros")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de livros", len(livros))
col2.metric("Preço médio", f"£{calcular_preco_medio(livros):.2f}")
col3.metric("Livros com 5 estrelas", contar_cinco_estrelas(livros))
col4.metric("Livro mais caro", mais_caro["preco"])
col4.caption(mais_caro["titulo"])

st.dataframe(livros)