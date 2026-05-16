import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
import os

st.set_page_config(page_title="Italy Study Advisor", page_icon="🇮🇹", layout="centered")

st.title("🇮🇹 Italy Study Advisor AI")
st.markdown("**Your AI helper for Bachelor's & Master's in Italy**")

# ===================== API KEYS =====================
os.environ["GROQ_API_KEY"] = st.secrets.get("GROQ_API_KEY", "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")
os.environ["TAVILY_API_KEY"] = st.secrets.get("TAVILY_API_KEY", "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")

# ===================== LOAD LLM & TOOL =====================
@st.cache_resource
def load_components():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=1024
    )
    tool = TavilySearchResults(max_results=3)
    return llm, tool

llm, search_tool = load_components()

# ===================== CHAT HISTORY =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 👋 How can I help you with your study plans in Italy?\n\nYou can ask about universities, application process, visa, scholarships, etc."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================== USER INPUT =====================
if prompt := st.chat_input("Ask me anything about studying in Italy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... ⚡"):
            # Use tool only when needed
            context = ""
            if any(word in prompt.lower() for word in ["deadline", "2026", "visa", "scholarship", "latest", "current", "requirement"]):
                tool_output = search_tool.invoke(prompt)
                context = f"\n\n**Latest Information:**\n{tool_output}"

            full_prompt = f"""You are a friendly and expert consultant for studying in Italy.
            Help students with universities, applications, documents, visa, scholarships, and student life.
            {context}

            Student Question: {prompt}
            Answer clearly and helpfully."""

            response = llm.invoke(full_prompt)
            answer = response.content

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("Useful Links")
    st.markdown("[Universitaly](https://www.universitaly.it)")
    st.markdown("[Study in Italy](https://studyinitaly.esteri.it)")
    st.markdown("[Student Visa](https://vistoperitalia.esteri.it)")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Groq + Tavily")
