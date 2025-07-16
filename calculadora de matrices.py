import streamlit as st
import numpy as np

def inicializar_matriz(filas, columnas, aleatoria=True):
    if aleatoria:
        return np.random.randint(100, 201, size=(filas, columnas))
    else:
        return np.zeros((filas, columnas), dtype=int)

def mostrar_editor_matriz(key, matriz):
    with st.expander(f"Editar Matriz {key}", expanded=True):
        filas, columnas = matriz.shape
        nueva_filas = st.number_input(f"Filas {key}", min_value=1, value=filas, key=f"filas_{key}")
        nueva_columnas = st.number_input(f"Columnas {key}", min_value=1, value=columnas, key=f"columnas_{key}")
        
        if nueva_filas != filas or nueva_columnas != columnas:
            matriz = np.zeros((nueva_filas, nueva_columnas), dtype=int)
            st.session_state[key] = matriz
            st.experimental_rerun()
        
        # Editor de matriz
        st.write(f"Ingrese valores para Matriz {key}:")
        nueva_matriz = []
        for i in range(matriz.shape[0]):
            cols = st.columns(matriz.shape[1])
            fila = []
            for j in range(matriz.shape[1]):
                with cols[j]:
                    fila.append(st.number_input(
                        f"{key}[{i},{j}]", 
                        value=int(matriz[i,j]), 
                        key=f"{key}_{i}_{j}"))
            nueva_matriz.append(fila)
        
        if st.button(f"Guardar Matriz {key}"):
            st.session_state[key] = np.array(nueva_matriz, dtype=int)
            st.success(f"Matriz {key} actualizada!")
            st.experimental_rerun()
        
        if st.button(f"Generar aleatoria {key}"):
            st.session_state[key] = inicializar_matriz(matriz.shape[0], matriz.shape[1])
            st.experimental_rerun()

def verificar_compatibilidad(m1, m2, operacion):
    if operacion in ["Suma de matrices", "Resta de matrices", "Multiplicación elemento a elemento"]:
        return m1.shape == m2.shape
    elif operacion == "Multiplicación matricial":
        return m1.shape[1] == m2.shape[0]
    return True

# Configuración inicial
st.set_page_config(layout="wide")
st.title("🔢 Calculadora de Matrices Interactiva")

# Inicialización de matrices
if 'A' not in st.session_state:
    st.session_state['A'] = inicializar_matriz(3, 3)
if 'B' not in st.session_state:
    st.session_state['B'] = inicializar_matriz(3, 3)

A = st.session_state['A']
B = st.session_state['B']

# Sidebar para configuración general
with st.sidebar:
    st.header("Configuración General")
    default_size = st.number_input("Tamaño predeterminado (n×n)", min_value=1, value=3)
    if st.button("Reiniciar todas las matrices"):
        st.session_state['A'] = inicializar_matriz(default_size, default_size)
        st.session_state['B'] = inicializar_matriz(default_size, default_size)
        st.experimental_rerun()

# Editor de matrices en pestañas
tab1, tab2 = st.tabs(["Matriz A", "Matriz B"])
with tab1:
    mostrar_editor_matriz('A', A)
with tab2:
    mostrar_editor_matriz('B', B)

# Operaciones
st.header("Operaciones Matriciales")
opcion = st.selectbox("Seleccione operación:", [
    "Ver matrices",
    "Producto por escalar",
    "Suma de matrices",
    "Resta de matrices",
    "Multiplicación elemento a elemento",
    "Suma diagonal",
    "Menor valor",
    "Mayor valor",
    "Suma total",
    "Promedio",
    "Multiplicación matricial",
    "Transpuesta"
])

result_container = st.container()

with result_container:
    if opcion == "Ver matrices":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Matriz A")
            st.dataframe(A)
        with col2:
            st.subheader("Matriz B")
            st.dataframe(B)
    
    elif opcion == "Producto por escalar":
        matriz_op = st.radio("Seleccione matriz:", ('A', 'B'))
        escalar = st.number_input("Ingrese escalar:", value=2)
        matriz = A if matriz_op == 'A' else B
        resultado = matriz * escalar
        st.subheader(f"Resultado: {matriz_op} × {escalar}")
        st.dataframe(resultado)
    
    elif opcion in ["Suma de matrices", "Resta de matrices", "Multiplicación elemento a elemento", "Multiplicación matricial"]:
        if not verificar_compatibilidad(A, B, opcion):
            st.error("Las matrices no tienen dimensiones compatibles para esta operación")
        else:
            if opcion == "Suma de matrices":
                resultado = A + B
                st.subheader("A + B")
            elif opcion == "Resta de matrices":
                resultado = A - B
                st.subheader("A - B")
            elif opcion == "Multiplicación elemento a elemento":
                resultado = A * B
                st.subheader("A * B (element-wise)")
            elif opcion == "Multiplicación matricial":
                resultado = np.dot(A, B)
                st.subheader("A × B (matricial)")
            st.dataframe(resultado)
    
    elif opcion in ["Suma diagonal", "Menor valor", "Mayor valor", "Suma total", "Promedio"]:
        matriz_op = st.radio("Seleccione matriz:", ('A', 'B'))
        matriz = A if matriz_op == 'A' else B
        
        if opcion == "Suma diagonal":
            if matriz.shape[0] != matriz.shape[1]:
                st.error("La matriz debe ser cuadrada para calcular la diagonal")
            else:
                st.success(f"Suma diagonal: {np.trace(matriz)}")
        elif opcion == "Menor valor":
            st.success(f"Menor valor: {matriz.min()}")
        elif opcion == "Mayor valor":
            st.success(f"Mayor valor: {matriz.max()}")
        elif opcion == "Suma total":
            st.success(f"Suma total: {matriz.sum()}")
        elif opcion == "Promedio":
            st.success(f"Promedio: {matriz.mean():.2f}")
    
    elif opcion == "Transpuesta":
        matriz_op = st.radio("Seleccione matriz:", ('A', 'B'))
        matriz = A if matriz_op == 'A' else B
        st.subheader(f"Transpuesta de {matriz_op}")
        st.dataframe(matriz.T)
