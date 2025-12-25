import streamlit as st
from advanced_chatbot import ask_bot   # your existing file
import time
import re
st.set_page_config(page_title="Web-Search Bot", layout="centered")

st.title("🤖 Ask-me-anything Bot")
st.caption("Answers come from live Google search")

# ------ chat history ------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------ display prior messages ------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------ input ------
if prompt := st.chat_input("Ask a question"):
    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # assistant answer with typing effect
    with st.chat_message("assistant"):
        full_response = ask_bot(prompt)

        message_placeholder = st.empty()
        streamed = ""
        for ch in full_response:   # <-- character loop keeps \n, spaces, back-ticks
            streamed += ch
            message_placeholder.write(streamed)
            time.sleep(0.015)      # slight delay for typing illusion
        # full_response = ask_bot(prompt)
        # junk = re.compile(r"^.*?(reasoning|thoughts:|```json|```)", re.I | re.S)
        # clean = junk.sub("", full_response).strip()            # first line only
        # if not clean:
        #     clean = "I couldn't formulate an answer."
        # message_placeholder = st.empty()
        # streamed = ""
        # for word in full_response.split():
        #     streamed += word + " "
        #     message_placeholder.write(streamed)
        #     time.sleep(0.08)   # slight delay → typing illusion
        st.session_state.messages.append({"role": "assistant", "content": full_response})