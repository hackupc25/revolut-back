import streamlit as st
import streamlit.components.v1 as components
from gemini import main

st.set_page_config(page_title="BLACKOUT", layout="wide", initial_sidebar_state="collapsed")

# Fase de introducción (efecto linterna)
if "show_controls" not in st.session_state:
    st.session_state.show_controls = False

if not st.session_state.show_controls:
    components.html(
        """
        <html>
        <head>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                background: black;
                color: #FFD700;
                overflow: hidden;
                cursor: none;
            }

            .spotlight {
                position: fixed;
                top: 0;
                left: 0;
                height: 100%;
                width: 100%;
                pointer-events: none;
                background: radial-gradient(
                    circle 10vmax at var(--cursorX, 50vw) var(--cursorY, 50vh),
                    rgba(0, 0, 0, 0) 0%,
                    rgba(0, 0, 0, 0.5) 80%,
                    rgba(0, 0, 0, 0.95) 100%
                );
                z-index: 9999;
            }

            .content {
                position: relative;
                z-index: 1;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-family: sans-serif;
            }

            h1 {
                font-size: 4em;
            }
        </style>
        </head>
        <body>
            <div class="content">
                <h1>BLACKOUT</h1>
            </div>
            <div class="spotlight"></div>

            <script>
            document.addEventListener('mousemove', function(e) {
                document.documentElement.style.setProperty('--cursorX', e.clientX + 'px');
                document.documentElement.style.setProperty('--cursorY', e.clientY + 'px');
            });
            </script>
        </body>
        </html>
        """,
        height=600,
    )

    if st.button("Entrar"):
        st.session_state.show_controls = True
        st.rerun()
else:
    st.title("Simulador de Recomendación de Efectivo")

    user_choice = st.selectbox("Selecciona usuario", [1, 2, 3, 4, 5])
    days = st.slider("Días de simulación", 1, 7, 3)

    if st.button("Generar recomendación de efectivo"):
        response = main(user_choice, duration_days=days)
        st.markdown(f"### {response}", unsafe_allow_html=True)
