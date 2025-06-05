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

opcion = st.sidebar.selectbox("Seleccione una operación:", [
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
])

if opcion == "Ver matrices A y B":
    st.subheader("Matriz A")
    st.dataframe(A)
    st.subheader("Matriz B")
    st.dataframe(B)

elif opcion == "Producto por escalar":
    escalar = st.sidebar.number_input("Ingrese escalar distinto de 0", value=2)
    if escalar == 0:
        st.error("El escalar no puede ser 0.")
    else:
        resultado = producto_por_escalar(A, escalar)
        st.write(f"Matriz A multiplicada por {escalar}:")
        st.dataframe(resultado)

elif opcion == "Suma de matrices":
    resultado = suma_matrices(A, B)
    st.write("Suma de A + B:")
    st.dataframe(resultado)

elif opcion == "Resta de matrices":
    resultado = resta_matrices(A, B)
    st.write("Resta de A - B:")
    st.dataframe(resultado)

elif opcion == "Multiplicación elemento a elemento":
    resultado = multiplicacion_elemento(A, B)
    st.write("Multiplicación A * B (elemento a elemento):")
    st.dataframe(resultado)

elif opcion == "Suma diagonal de A":
    st.write(f"Suma de la diagonal principal de A: {suma_diagonal(A)}")

elif opcion == "Menor valor de A":
    st.write(f"Menor valor en A: {menor_valor(A)}")

elif opcion == "Mayor valor de A":
    st.write(f"Mayor valor en A: {mayor_valor(A)}")

elif opcion == "Suma total de A":
    st.write(f"Suma total de A: {suma_total(A)}")

elif opcion == "Promedio de A":
    st.write(f"Promedio de A: {promedio_matriz(A)}")

elif opcion == "Multiplicación matricial":
    resultado = multiplicacion_matricial(A, B)
    st.write("Multiplicación matricial A * B:")
    st.dataframe(resultado)

elif opcion == "Reiniciar matrices":
    st.session_state['A'] = inicializar_matriz()
    st.session_state['B'] = inicializar_matriz()
    st.success("Matrices reinicializadas.")