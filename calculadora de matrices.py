import streamlit as st
import numpy as np

TAM = 20

def inicializar_matriz():
    return np.random.randint(100, 201, size=(TAM, TAM))

def producto_por_escalar(matriz, escalar):
    return matriz * escalar

def suma_matrices(m1, m2):
    return m1 + m2

def resta_matrices(m1, m2):
    return m1 - m2

def multiplicacion_elemento(m1, m2):
    return m1 * m2

def suma_diagonal(matriz):
    return np.trace(matriz)

def menor_valor(matriz):
    return matriz.min()

def mayor_valor(matriz):
    return matriz.max()

def suma_total(matriz):
    return matriz.sum()

def promedio_matriz(matriz):
    return int(matriz.mean())

def multiplicacion_matricial(m1, m2):
    return np.dot(m1, m2)

st.set_page_config(layout="wide")
st.title("🔢 Calculadora de Matrices - George Losada")

if 'A' not in st.session_state:
    st.session_state['A'] = inicializar_matriz()
if 'B' not in st.session_state:
    st.session_state['B'] = inicializar_matriz()

A = st.session_state['A']
B = st.session_state['B']

# --- Selector principal en pantalla (no en sidebar) ---
st.header("Operaciones Disponibles")
opcion = st.selectbox("Seleccione una operación:", [
    "Ver matrices A y B",
    "Producto por escalar",
    "Suma de matrices",
    "Resta de matrices",
    "Multiplicación elemento a elemento",
    "Suma diagonal de A",
    "Menor valor de A",
    "Mayor valor de A",
    "Suma total de A",
    "Promedio de A",
    "Multiplicación matricial",
    "Reiniciar matrices"
], key="main_selector")

# --- Contenedor para resultados ---
result_container = st.container()

# Operaciones con controles en pantalla principal
if opcion == "Ver matrices A y B":
    with result_container:
        st.header("Matriz A")
        st.dataframe(A)
        st.header("Matriz B")
        st.dataframe(B)

elif opcion == "Producto por escalar":
    escalar = st.number_input("Ingrese escalar distinto de 0", 
                            value=2, 
                            key="escalar_input")
    if escalar == 0:
        st.error("El escalar no puede ser 0.")
    else:
        with result_container:
            st.header(f"Matriz A × {escalar}")
            resultado = producto_por_escalar(A, escalar)
            st.dataframe(resultado)

elif opcion == "Suma de matrices":
    with result_container:
        st.header("Suma: A + B")
        resultado = suma_matrices(A, B)
        st.dataframe(resultado)

elif opcion == "Resta de matrices":
    with result_container:
        st.header("Resta: A - B")
        resultado = resta_matrices(A, B)
        st.dataframe(resultado)

elif opcion == "Multiplicación elemento a elemento":
    with result_container:
        st.header("Multiplicación elemento a elemento (A * B)")
        resultado = multiplicacion_elemento(A, B)
        st.dataframe(resultado)

elif opcion == "Suma diagonal de A":
    with result_container:
        st.header("Suma de la diagonal principal")
        st.success(f"Resultado: {suma_diagonal(A)}")

elif opcion == "Menor valor de A":
    with result_container:
        st.header("Valor mínimo en A")
        st.success(f"Resultado: {menor_valor(A)}")

elif opcion == "Mayor valor de A":
    with result_container:
        st.header("Valor máximo en A")
        st.success(f"Resultado: {mayor_valor(A)}")

elif opcion == "Suma total de A":
    with result_container:
        st.header("Suma de todos los elementos de A")
        st.success(f"Resultado: {suma_total(A)}")

elif opcion == "Promedio de A":
    with result_container:
        st.header("Promedio de los elementos de A")
        st.success(f"Resultado: {promedio_matriz(A)}")

elif opcion == "Multiplicación matricial":
    with result_container:
        st.header("Multiplicación matricial (A × B)")
        resultado = multiplicacion_matricial(A, B)
        st.dataframe(resultado)

elif opcion == "Reiniciar matrices":
    st.session_state['A'] = inicializar_matriz()
    st.session_state['B'] = inicializar_matriz()
    with result_container:
        st.success("Matrices reinicializadas con nuevos valores aleatorios")
        st.balloons()
