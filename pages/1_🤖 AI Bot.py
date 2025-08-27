import streamlit as sl
import polars as pl
from streamlit_lottie import st_lottie
import requests
from huggingface_hub import InferenceClient
df1 = pl.read_csv("aqi_clean_state.csv")
hf_token = sl.secrets["HUGGINGFACEHUB_API_TOKEN"]
client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=hf_token)
#  streamlit theme
sl.set_page_config(page_title="Aeris", page_icon=r"C:\Users\tempe\OneDrive\Documents\Air quality project\Aeris.png")
url = "https://lottie.host/16969d1e-85b4-4c9c-a549-f79d40d622cc/kxb2JFGleJ.json"
response = requests.get(url)
animation_json = response.json()
st_lottie(animation_json, height=200, key="lottie2")
sl.title(":red[Talk with AER!]")

if "messages" not in sl.session_state:
    sl.session_state.messages = [
        {"role": "system", "content": "You are AER, an AI assistant that provides state-specific solutions for combating air pollution in India. Be short, concise and if someone asks you who build you, or anything related your creator, respond Daksh Gupta. If someone ask some other questions from you on different topics like philosphy, code generation, etc.,  anything other than Pollution, respond with I'm sorry. I can only provide information regarding pollution"}
    ]

# Display previous messages
for msg in sl.session_state.messages[1:]:  # skip system msg
    with sl.chat_message(msg["role"]):
        sl.markdown(msg["content"])

# user input
if user_input := sl.chat_input("Ask AER about air pollution solutions..."):
    # Store user message
    sl.session_state.messages.append({"role": "user", "content": user_input})
    with sl.chat_message("user"):
        sl.markdown(user_input)

    # Get AI response
    with sl.chat_message("assistant"):
        with sl.spinner("Thinking..."):
            response = client.chat_completion(
                model="meta-llama/Meta-Llama-3-8B-Instruct",  # free Llama-3
                messages=sl.session_state.messages,
                max_tokens=300,
            )
            bot_reply = response.choices[0].message["content"]
            sl.markdown(bot_reply)

    # Store AI reply
    sl.session_state.messages.append({"role": "assistant", "content": bot_reply})
