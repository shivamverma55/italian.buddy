import streamlit as st
from langchain_groq import ChatGroq
import os

st.set_page_config(page_title="Italy Study Advisor", page_icon="🇮🇹", layout="wide")

st.title("🇮🇹 Italy Study Advisor AI")
st.markdown("**Bachelor's & Master's in Italy**")

# API Keys
os.environ["GROQ_API_KEY"] = st.secrets.get

@st.cache_resource
def load_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

llm = load_llm()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 👋 Kaise help karu aapko Italy study ke liye?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Universities, visa, scholarship ke baare mein pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            response = llm.invoke(f"""You are expert Italy education consultant. 
            Answer in friendly way: {prompt}""")
            answer = response.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
