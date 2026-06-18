import streamlit as st
from google import genai
from google.genai import types

# mais tarde vamos colar codigo aqui
def converter_para_gemini(historico):
    mensagens_gemini = []
    teperature=0.4


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INTRODUCAO_SISITEMA,
            temperature=0.4,
        )
    )


    return resposta.text




MODELO = "gemini-2.5-flash"
persona = open("pokemon_persona.txt","r", encoding="utf-8")
INTRODUCAO_SISITEMA = persona.read()
persona.close()

st.set_page_config("chatbot com Gemini","👍")

st.title("chatbot pokemon")

st.image("https://thf.bing.com/th/id/OIP.PGSG3JPYjoMAEWIFR8Sg-gHaHa?w=186&h=186&c=7&r=0&o=7&cb=thfc1falcon2&pid=1.7&rm=3")

chave_api = st.sidebar.text_input("Digite sua cha de API",type="password")

if not chave_api:
    st.warning("É preciso inserir uma chave de API ")
    st.stop()

cliente = genai.Client(api_key= chave_api)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


entrada_usuario = st.chat_input("digete sua pergunta:")


if entrada_usuario:
    st.session_state.historico.append({
    "role":"user",
    "content":entrada_usuario
    })

    with st.chat_message("user"):
        st.markdown(entrada_usuario)

    with st.chat_message("assistant"):
        resposta_ia = gerar_resposta()
        st.markdown(resposta_ia)
        


    st.session_state.historico.append({
        "role" : "assistant",
        "content":resposta_ia
    })