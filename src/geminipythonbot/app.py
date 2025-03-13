import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
import time  

# ✅ صفحے کی سیٹنگز
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.markdown("Hello! I'm your AI Assistant. Ask me anything.")

# ✅ API Key حاصل کریں
api_key = st.secrets["google"]["api_key"]

# ✅ چیٹ ہسٹری محفوظ رکھیں
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ ماڈل سیٹ اپ کریں
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# ✅ چیٹ ہسٹری دکھائیں
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# ✅ یوزر ان پٹ لے کر پراسیس کریں
user_input = st.chat_input("Ask me anything...")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = model.invoke(user_input).content
        
        # ✅ ٹائپنگ ایفیکٹ
        full_response = ""
        for letter in response:
            full_response += letter
            message_placeholder.markdown(full_response + "▌")  
            time.sleep(0.02)
        message_placeholder.markdown(full_response)
        
        st.session_state.chat_history.append(AIMessage(content=full_response))

# ✅ چیٹ صاف کرنے کا بٹن
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()



