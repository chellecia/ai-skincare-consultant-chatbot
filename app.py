import os
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


# Load .env
load_dotenv()

GOOGLE_API_KEY = os.getenv("api_key")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY tidak ditemukan di file .env")

# Inisiasi client LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key = GOOGLE_API_KEY,
    temperature=0.6,
    top_p = 0.95,
    top_k=40
    )

# --- Streamlit UI ---
st.title("💄 Chatbot Skincare")
st.caption("Tanyakan apa saja tentang skincare ✨")


# Inisiasi chat history dengan hanya system message
if "messages" not in st.session_state:
    st.session_state.messages =[
        SystemMessage(
            "You are a professional skincare expert."
            "Always respond in less than 3 sentences in a chat style."
            "Use a friendly chat style. "
            "Reply in bahasa indonesia."
            "If the question is not related to skincare, politely say you can only answer skincare-related questions."
        
    )
]

# --- Display chat messages ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif msg.type == "ai":
        st.chat_message("assistant").write(msg.content)
        
# --- Chat input ---
user_input = st.chat_input("Tanya tentang skincare...")

if user_input:
    # 1. Tampilkan pesan user
    st.chat_message("user").write(user_input)

    # 2. Masukkan ke history
    st.session_state.messages.append(HumanMessage(user_input))

    # 3. Invoke model
    response = llm.invoke(st.session_state.messages)

    # 4. Tampilkan dan simpan jawaban
    st.session_state.messages.append(response)
    st.chat_message("assistant").write(response.content)