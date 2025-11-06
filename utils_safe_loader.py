import streamlit as st
import traceback

def safe_run(func):
    """Ejecuta una función mostrando una pantalla amigable si ocurre un error."""
    try:
        func()
    except Exception as e:
        st.error("🚧 **La aplicación está en mantenimiento temporal.**")
        st.warning("Por favor, vuelve a intentarlo en unos minutos.")
        st.markdown("---")
        with st.expander("🔍 Detalles técnicos (solo para el desarrollador)"):
            st.text(traceback.format_exc())
