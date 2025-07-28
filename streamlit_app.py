import streamlit as st
import requests
import os
from dotenv import load_dotenv


load_dotenv()


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Assistente de Planilhas IA", layout="wide")
st.title("📊 Assistente de Planilhas com IA")

st.header("📁 Upload do Arquivo")

uploaded_file = st.file_uploader("Envie um arquivo CSV ou Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    with st.spinner("Enviando arquivo..."):
        response = requests.post(f"{API_BASE_URL}/api/upload", files=files)

    if response.status_code == 200:
        upload_data = response.json()
        st.success("Arquivo enviado com sucesso!")
        st.session_state["file_name"] = os.path.basename(upload_data["file_path"])
        st.session_state["file_delimiter"] = ";" if uploaded_file.name.endswith(".csv") else ","
        st.write(f"📝 Nome do arquivo: `{st.session_state['file_name']}`")
    else:
        st.error("Erro ao enviar o arquivo.")

if "file_name" in st.session_state:
    st.header("🔍 Consultar Dados com IA")

    query = st.text_input("Digite sua pergunta (ex: média de vendas por região)")

    if st.button("Enviar Consulta") and query:
        payload = {
            "query": query,
            "file_name": st.session_state["file_name"],
            "file_delimiter": st.session_state["file_delimiter"]
        }

        with st.spinner("Consultando IA..."):
            response = requests.post(f"{API_BASE_URL}/api/search", json=payload)

        if response.status_code == 200:
            result = response.json()

            if result["error_msg"]:
                st.error(f"❌ Erro: {result['error_msg']}")
            else:
                st.markdown("### 💬 Resposta do Assistente")
                st.markdown(result["llm_output"])

                st.markdown("### 🐼 Comandos Pandas usados")
                for cmd in result["pandas_commands"]:
                    st.code(cmd, language="python")

                st.markdown("### 📤 Resultado")
                if result["image_path"]:
                    image_url = f"{API_BASE_URL}/{result['image_path']}"
                    st.image(image_url, use_container_width=True)
                elif result["pandas_output"] is not None:
                    st.write("Resultado:")
                    st.write(result["pandas_output"])

                st.markdown("### 📊 Uso de tokens")
                usage = result.get("usage", {})
                st.json(usage)

        else:
            st.error("Erro ao consultar a IA.")