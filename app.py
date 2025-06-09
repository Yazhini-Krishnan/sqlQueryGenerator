import streamlit as st
import pandas as pd
from llama_cpp import Llama

# Path to your local Phi-3 model
MODEL_PATH = "/Users/yazhini.krishnan/.cache/huggingface/hub/models--microsoft--Phi-3-mini-4k-instruct-gguf/snapshots/999f761fe19e26cf1a339a5ec5f9f201301cbb83/Phi-3-mini-4k-instruct-q4.gguf"

@st.cache_resource
def load_model():
    return Llama(model_path=MODEL_PATH)

llm = load_model()

st.title("SQL Generator: Natural Language to SQL")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your table (CSV or Excel file)", 
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # Read file as dataframe
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Table Preview")
    st.dataframe(df.head())

    # Build table schema as a string
    schema = []
    for col in df.columns:
        dtype = str(df[col].dtype).upper()
        # Simplify common dtypes
        if "INT" in dtype or "int" in dtype:
            dtype = "INT"
        elif "FLOAT" in dtype or "double" in dtype:
            dtype = "FLOAT"
        elif "OBJECT" in dtype or "str" in dtype:
            dtype = "VARCHAR"
        elif "BOOL" in dtype:
            dtype = "BOOLEAN"
        else:
            dtype = dtype
        schema.append(f"{col} {dtype}")
    schema_str = ", ".join(schema)

    st.markdown(f"**Detected table schema:** `{schema_str}`")

    # Question input loop
    st.subheader("Ask a question about your table")
    question = st.text_input("Enter your question (e.g., Show top 5 users by revenue)")

    if question:
        # Compose prompt for LLM
        prompt = (
            "You are a helpful assistant that writes SQL queries.\n"
            f"Table schema: {schema_str}\n"
            f"User request: {question}\n"
            "SQL:"
        )
        with st.spinner("Generating SQL..."):
            output = llm(prompt, max_tokens=256)
            sql = output['choices'][0]['text']
        st.code(sql, language="sql")

        # Allow the user to ask another question (just leave input box open)

else:
    st.info("Upload a CSV or Excel file to get started.")