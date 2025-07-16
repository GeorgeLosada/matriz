import streamlit as st
import numpy as np
import pandas as pd

def inicializar_matriz(filas, columnas, aleatoria=True):
    if aleatoria:
        return np.random.randint(100, 201, size=(filas, columnas))
    else:
        return np.zeros((filas, columnas), dtype=int)

def mostrar_editor_matriz(key, matriz):
    with st.expander(f" Editar Matriz {key}", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            filas = st.number_input(f"Filas {key}", 
                                    min_value=1, 
                                    value=matriz.shape[0],
                                    key=f"filas_{key}")
        with col2:
            columnas = st.number_input(f"Columnas {key}", 
                                      min_value=1, 
                                      value=matriz.shape[1],
                                      key=f"columnas_{key}")
        
        # Verificar si hay cambio de tamaño
        if filas != matriz.shape[0] or columnas != matriz.shape[1]:
            matriz = np.zeros((filas, columnas), dtype=int)
            st.session_state[key] = matriz
            st.experimental_rerun()
        
        # Editor de matriz con data_editor
        st.write(f"Valores de la matriz {key}:")
        df = pd.DataFrame(matriz)
        edited_df = st.data_editor(df, use_container_width=True, 
                                  height=min(300, 50 + 35 * filas),
                                  key=f"editor_{key}")
        
        # Actualizar matriz si hay cambios
        if not edited_df.equals(df):
            st.session_state[key] = edited_df.to_numpy()
        
        # Botones de acción
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(f"Generar aleatoria {key}"):
                st.session_state[key] = inicializar_matriz(filas, columnas)
                st.experimental_rerun()
        with c2:
            if st.button(f"Limpiar {key}"):
                st.session_state[key] = np.zeros((filas, columnas), dtype=int)
                st.experimental_rerun()
        with c3:
            if st.button(f"Guardar cambios {key}"):
                st.success(f"Matriz {key} actualizada!")

def verificar_compatibilidad(m1, m2, operacion):
    if operacion in ["Suma", "Resta", "Multiplicación elemento a elemento"]:
        return m1.shape == m2.shape
    elif operacion == "Multiplicación matricial":
        return m1.shape[1] == m2.shape[0]
    return True

# Configuración de página
st.set_page_config(layout="centered")
st.title("Calculadora Avanzada de Matrices")
st.markdown("""
<style>
div[data-testid="stExpander"] div[role="button"] p {
    font-size: 1.2rem;
    font-weight: bold;
}
.st-b7 {
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

# Inicialización de matrices
if 'A' not in st.session_state:
    st.session_state['A'] = inicializar_matriz(3, 3)
if 'B' not in st.session_state:
    st.session_state['B'] = inicializar_matriz(3, 3)

A = st.session_state['A']
B = st.session_state['B']

# Sección de control de matrices
st.header("Configuración de Matrices")
col1, col2 = st.columns(2)

with col1:
    mostrar_editor_matriz('A', A)
    st.caption(f"Dimensión: {A.shape[0]}×{A.shape[1]}")

with col2:
    mostrar_editor_matriz('B', B)
    st.caption(f"Dimensión: {B.shape[0]}×{B.shape[1]}")

# Operaciones matemáticas
st.header("Operaciones Matriciales")
operacion = st.selectbox("Seleccione una operación:", [
    "Suma (A + B)",
    "Resta (A - B)",
    "Producto por escalar",
    "Multiplicación elemento a elemento (A * B)",
    "Multiplicación matricial (A × B)",
    "Transpuesta",
    "Suma diagonal",
    "Menor valor",
    "Mayor valor",
    "Suma total",
    "Promedio"
])

# Contenedor de resultados
result_container = st.container()
with result_container:
    st.header("Resultado")
    
    try:
        if operacion == "Suma (A + B)":
            if not verificar_compatibilidad(A, B, "Suma"):
                st.error("Las matrices deben tener la misma dimensión para sumar")
            else:
                resultado = A + B
                st.dataframe(resultado, use_container_width=True)
                st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
                
        elif operacion == "Resta (A - B)":
            if not verificar_compatibilidad(A, B, "Resta"):
                st.error("Las matrices deben tener la misma dimensión para restar")
            else:
                resultado = A - B
                st.dataframe(resultado, use_container_width=True)
                st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
                
        elif operacion == "Producto por escalar":
            col1, col2 = st.columns([1, 3])
            with col1:
                matriz = st.radio("Matriz:", ["A", "B"])
                escalar = st.number_input("Escalar:", value=2)
            matriz_seleccionada = A if matriz == "A" else B
            resultado = matriz_seleccionada * escalar
            st.dataframe(resultado, use_container_width=True)
            st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
            
        elif operacion == "Multiplicación elemento a elemento (A * B)":
            if not verificar_compatibilidad(A, B, "Multiplicación elemento a elemento"):
                st.error("Las matrices deben tener la misma dimensión")
            else:
                resultado = A * B
                st.dataframe(resultado, use_container_width=True)
                st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
                
        elif operacion == "Multiplicación matricial (A × B)":
            if not verificar_compatibilidad(A, B, "Multiplicación matricial"):
                st.error("El número de columnas de A debe igualar el número de filas de B")
            else:
                resultado = np.dot(A, B)
                st.dataframe(resultado, use_container_width=True)
                st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
                
        elif operacion == "Transpuesta":
            col1, col2 = st.columns([1, 3])
            with col1:
                matriz = st.radio("Matriz:", ["A", "B"])
            matriz_seleccionada = A if matriz == "A" else B
            resultado = matriz_seleccionada.T
            st.dataframe(resultado, use_container_width=True)
            st.success(f"Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
            
        elif operacion in ["Suma diagonal", "Menor valor", "Mayor valor", "Suma total", "Promedio"]:
            col1, col2 = st.columns([1, 3])
            with col1:
                matriz = st.radio("Matriz:", ["A", "B"])
            matriz_seleccionada = A if matriz == "A" else B
            
            if operacion == "Suma diagonal":
                if matriz_seleccionada.shape[0] != matriz_seleccionada.shape[1]:
                    st.error("La matriz debe ser cuadrada")
                else:
                    st.info(f"Suma diagonal = {np.trace(matriz_seleccionada)}")
                    
            elif operacion == "Menor valor":
                st.info(f"Valor mínimo = {matriz_seleccionada.min()}")
                
            elif operacion == "Mayor valor":
                st.info(f"Valor máximo = {matriz_seleccionada.max()}")
                
            elif operacion == "Suma total":
                st.info(f"Suma total = {matriz_seleccionada.sum()}")
                
            elif operacion == "Promedio":
                st.info(f"Promedio = {matriz_seleccionada.mean():.2f}")
                
    except Exception as e:
        st.error(f"Error en la operación: {str(e)}")

# Información adicional
st.divider()
st.info("Consejo: Puedes cambiar el tamaño de las matrices editando los valores de filas y columnas")
