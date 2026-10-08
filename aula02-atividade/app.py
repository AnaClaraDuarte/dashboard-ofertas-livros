"""Dashboard de Livros: app Streamlit.
"""

import streamlit as st

import dados

def montar_tabela(livros):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis."""
    tabela = []
    for livro in livros:
        linha = {
            "Título": livro["titulo"],
            "Categoria": livro["categoria"],
            "Nota": livro["nota"] * "⭐",
            "Preço": f"£ {livro['preco']:.2f}",
            "Faixa": classificar_preco(livro["preco"])
        }
        tabela.append(linha)
    return tabela

def classificar_preco(preco):
    """Classifica um preço em libras em uma faixa de texto."""
    if preco < 20:
        return "Barato"
    elif preco <= 40:
        return "Médio"
    else:
        return "Caro"

def contar_por_faixa(livros):
    """Conta quantos livros existem em cada faixa de preço: {"Caro": 403, ...}"""
    contagem = {}
    for livro in livros:
        faixa = classificar_preco(livro["preco"])
        if faixa in contagem:
            contagem[faixa] = contagem[faixa] + 1
        else:
            contagem[faixa] = 1

    return contagem

def buscar_por_titulo(livros, busca):
    """Devolve uma lista só com os livros cujo título contém o texto buscado.
    A comparação ignora maiúsculas/minúsculas: "harry" também acha "Harry Potter".
    Com a busca vazia, todos os livros aparecem.
    """
    encontrados = []
    for livro in livros:
        if busca.lower() in livro["titulo"].lower():
            encontrados.append(livro)
    return encontrados

def listar_categorias(livros):
    """Devolve uma lista com todas as categorias únicas dos livros."""
    categorias = []
    for livro in livros:
        if livro["categoria"] not in categorias:
            categorias.append(livro["categoria"])
    categorias.sort()
    return list(categorias)

def filtrar_por_categoria(livros, categoria):
    """Devolve uma lista só com os livros que pertencem à categoria especificada.
    Com a categoria vazia, todos os livros aparecem.
    """
    if categoria == "Todas":
        return livros
    
    resultado = []
    for livro in livros:
        if livro["categoria"] == categoria:
            resultado.append(livro)
    return resultado

def main():
    st.set_page_config(page_title="Dashboard de Livros", page_icon="📚", layout="wide")
    st.title("📚 Dashboard de Livros")    
    livros = dados.carregar_livros()

    tabela = montar_tabela(livros)

    col1, col2, col3, col4 = st.columns(4)
    qtd_livros = len(livros)
    col1.metric("Total de Livros", qtd_livros)

    preco_medio = dados.calcular_preco_medio(livros)
    col2.metric("Preço médio", f"£{preco_medio:.2f}")

    cinco_estrelas = dados.contar_cinco_estrelas(livros)
    col3.metric("Qtd. livros 5 Estrelas", cinco_estrelas)

    mais_caro = dados.encontrar_mais_caro(livros)
    col4.metric("Livro mais caro", f"£{mais_caro['preco']}")
    col4.caption(mais_caro["titulo"])

    col_busca, col_categoria = st.columns(2)

    busca = st.text_input("🔎 Buscar pelo título")
    categoria = st.selectbox("Filtrar por categoria", ["Todas"] + listar_categorias(livros))

    encontrados = filtrar_por_categoria(livros, categoria)
    encontrados = buscar_por_titulo(encontrados, busca)
 
    qtd_livros = len(encontrados)

    # Só a tabela usa os livros encontrados
    if len(encontrados) == 0:
        st.warning("Nenhum livro encontrado.")
    else:
        st.caption(f"{len(encontrados)} livros encontrados")
        st.dataframe(montar_tabela(encontrados))

if __name__ == "__main__":
     main()

    