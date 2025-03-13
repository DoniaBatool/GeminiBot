import streamlit as st 
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage

st.set_page_config(page_title="AI Text Assistant", page_icon="👽")
st.title("AI Chatbot")

st.markdown("Hello! I'm your AI Assistant. I can help answer you any technology and education related question")

# API key from secrets
api_key = st.secrets["google"]["api_key"]

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a helpful AI Assistant. Please respond to the user in English"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

msgs = StreamlitChatMessageHistory(key="langchain_messages")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

chain_with_history = RunnableWithMessageHistory(
    prompt | model,  # Prompt aur model ko connect karein
    lambda session_id: msgs,
    input_messages_key="question",
    history_message_key="chat_history",
)

user_input = st.text_input("Enter your question in English", "")

if user_input:
    st.chat_message("human").write(user_input)

    # Chat history update karein
    msgs.add_message(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        config = {"configurable": {"session_id": "any"}}

        response = chain_with_history.invoke({"question": user_input, "chat_history": []}, config)

        full_response = response.content if hasattr(response, "content") else response
        message_placeholder.markdown(full_response)

        # Chat history mein assistant ka response add karein
        msgs.add_message(AIMessage(content=full_response))

else:
    st.warning("Please enter your question.")