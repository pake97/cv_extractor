import streamlit as st
import hmac
import os
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)





review_template_str = """Sei un HR chatbot, il tuo compito è di chattare con uno studente, ponendogli delle domande per capire meglio il suo profilo e le sue competenze. Capisci qual'è il suo settire e in seguito chiedigli delle sue competenze relative a quel settore, soft skills, conoscenze linguistiche, esperienze lavorative e formative. 
L'obiettivo finale è quello di comporre il currivulum vitae dello studente. Non essere rigido, cerca di creare un ambiente rilassato e amichevole. Approfondisci le risposte dello studente, chiedigli di fornire esempi concreti delle sue esperienze.
"""

cv_template_str = """Partendo dalla seguente conversazione avuta tra un HR manager e uno studente, componi il curriculum vitae strutturato dello studente.
Conversazione : 
{chat}
"""

db_template_str = """Partendo dalla seguente conversazione avuta tra un HR manager e uno studente, componi il curriculum vitae strutturato dello studente in formato json, da inserire in un NoSQL database.
Conversazione : 
{chat}
"""

messages = []



chat_model =ChatOpenAI(
    #model="gpt-4o",
    model ="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None)


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is 
st.logo('logo.png', icon_image='logo.png')
def resetChat():
    st.session_state.messagessalesiani = [{"role": "assistant", "content": "Ciao, raccontami brevemente di te."}]
    st.session_state.aimessagessalesiani = [SystemMessage(content=review_template_str), AIMessage(content="Ciao, raccontami brevemente di te.")]
    
st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.title("Talentiverso")
if "messagessalesiani" not in st.session_state:
    st.session_state.messagessalesiani = [{"role": "assistant", "content": "Ciao, raccontami brevemente di te."}]
    
if "aimessagessalesiani" not in st.session_state:
    st.session_state.aimessagessalesiani = [SystemMessage(content=review_template_str), AIMessage(content="Ciao, raccontami brevemente di te.")]

st.button("Reset", on_click=resetChat)
if st.button("Crea CV"):
    # Validate inputs
    try:
        with st.spinner('Attendi...'):
            chat = ""
            
            for msg in st.session_state.messagessalesiani:
                if(msg["role"] == "user"):
                    chat += "Studente : "+ msg["content"] + "\n"
                if(msg["role"] == "assistant"):
                    chat += "HR : "+ msg["content"] + "\n"
            summary = chat_model.stream(cv_template_str.format(chat=chat))
            st.write_stream(summary) 
    except Exception as e:
        st.exception(f"An error occurred: {e}")

if st.button("Crea CV per database"):
    # Validate inputs
    try:
        with st.spinner('Attendi...'):
            chat = ""
            for msg in st.session_state.messagessalesiani:
                if(msg["role"] == "user"):
                    chat += "Studente : "+ msg["content"] + "\n"
                if(msg["role"] == "assistant"):
                    chat += "HR : "+ msg["content"] + "\n"
            summary = chat_model.stream(db_template_str.format(chat=chat))
            st.write_stream(summary) 
    except Exception as e:
        st.exception(f"An error occurred: {e}")






for message in st.session_state.messagessalesiani:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Invia messagio al Chatbot Salesiani:"):
    st.session_state.messagessalesiani.append({"role": "user", "content": prompt})
    with st.chat_message("user"):    
        st.session_state.aimessagessalesiani.append(HumanMessage(content=prompt))
        print(messages)
    with st.chat_message("assistant"):        
        stream =chat_model.stream(st.session_state.aimessagessalesiani)
        response = st.write_stream(stream)
        st.session_state.aimessagessalesiani.append(AIMessage(content=response))
    st.session_state.messagessalesiani.append({"role": "assistant", "content": response})



