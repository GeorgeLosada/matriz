import streamlit as st
import numpy as np

def cifrado_cesar(texto, desplazamiento, modo='cifrar'):
    resultado = ''
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            if modo == 'cifrar':
                nuevo = (ord(c) - base + desplazamiento) % 26 + base
            else:
                nuevo = (ord(c) - base - desplazamiento) % 26 + base
            resultado += chr(nuevo)
        else:
            resultado += c
    return resultado

def app_cesar():
    st.subheader("Cifrado César")
    texto = st.text_input("Texto")
    desplazamiento = st.slider("Desplazamiento", 1, 25, 3)
    modo = st.radio("Modo", ["Cifrar", "Descifrar"])
    if st.button("Ejecutar"):
        resultado = cifrado_cesar(texto, desplazamiento, modo.lower())
        st.text_area("Resultado", resultado, height=150)

def metodo_euler(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]
    for _ in range(n):
        y0 += h * f(x0, y0)
        x0 += h
        xs.append(x0)
        ys.append(y0)
    return xs, ys

def app_euler():
    st.subheader("Método de Euler para EDOs")
    fx = st.text_input("Función f(x, y)", value="x + y")
    x0 = st.number_input("x0", value=0.0)
    y0 = st.number_input("y0", value=1.0)
    h = st.number_input("Paso h", value=0.1)
    n = st.number_input("Número de pasos", value=10, step=1)

    if st.button("Calcular"):
        f = lambda x, y: eval(fx)
        xs, ys = metodo_euler(f, x0, y0, h, int(n))
        st.write("Resultados:")
        for i in range(len(xs)):
            st.write(f"x = {xs[i]:.4f}, y = {ys[i]:.4f}")

def gauss_reduction(A):
    A = A.astype(float)
    n, m = A.shape
    for i in range(min(n, m)):
        if A[i, i] == 0:
            for j in range(i + 1, n):
                if A[j, i] != 0:
                    A[[i, j]] = A[[j, i]]
                    break
        if A[i, i] != 0:
            A[i] = A[i] / A[i, i]
            for j in range(i + 1, n):
                A[j] = A[j] - A[j, i] * A[i]
    return A

def app_gauss():
    st.subheader("Reducción Gaussiana")
    filas = st.number_input("Número de filas", 1, 10, 3)
    columnas = st.number_input("Número de columnas", 1, 10, 4)
    datos = st.text_area("Matriz (fila por fila, separados por espacios)", "1 2 3 4\n5 6 7 8\n9 10 11 12")
    if st.button("Reducir"):
        try:
            matriz = [list(map(float, fila.split())) for fila in datos.strip().split('\n')]
            A = np.array(matriz)
            A_reducida = gauss_reduction(A)
            st.write("Matriz escalonada:")
            st.write(A_reducida)
        except Exception as e:
            st.error(f"Error: {e}")

def app_corr_cov():
    st.subheader("Correlación y Covarianza")
    x_input = st.text_input("Valores de X (separados por comas)", "1, 2, 3, 4, 5")
    y_input = st.text_input("Valores de Y (separados por comas)", "2, 4, 6, 8, 10")

    if st.button("Calcular"):
        try:
            x = np.array(list(map(float, x_input.split(','))))
            y = np.array(list(map(float, y_input.split(','))))
            cov = np.cov(x, y)[0][1]
            corr = np.corrcoef(x, y)[0][1]
            st.write(f"Covarianza: {cov:.4f}")
            st.write(f"Correlación: {corr:.4f}")
        except:
            st.error("Error al procesar los datos.")

def app_matrices():
    st.subheader("Operaciones con Matrices")
    mat1 = st.text_area("Matriz A", "1 2\n3 4")
    mat2 = st.text_area("Matriz B", "5 6\n7 8")
    operacion = st.selectbox("Operación", ["Suma", "Resta", "Multiplicación"])

    if st.button("Ejecutar operación"):
        try:
            A = np.array([list(map(float, fila.split())) for fila in mat1.strip().split('\n')])
            B = np.array([list(map(float, fila.split())) for fila in mat2.strip().split('\n')])
            if operacion == "Suma":
                resultado = A + B
            elif operacion == "Resta":
                resultado = A - B
            else:
                resultado = A @ B
            st.write("Resultado:")
            st.write(resultado)
        except:
            st.error("Error: asegúrate de que las matrices tengan dimensiones compatibles.")

st.title("Calculadoras Matemáticas Interactivas")

opcion = st.sidebar.selectbox("Selecciona una herramienta", [
    "Cifrado César",
    "Método de Euler (EDOs)",
    "Reducción Gaussiana",
    "Correlación y Covarianza",
    "Operaciones con Matrices"
])

if opcion == "Cifrado César":
    app_cesar()
elif opcion == "Método de Euler (EDOs)":
    app_euler()
elif opcion == "Reducción Gaussiana":
    app_gauss()
elif opcion == "Correlación y Covarianza":
    app_corr_cov()
elif opcion == "Operaciones con Matrices":
    app_matrices()
