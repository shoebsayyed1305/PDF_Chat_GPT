import streamlit as st
import time
from retrieval.qa import get_answer

def show():
    st.title("Vehicle Q & A")

    for chat_message in st.session_state.get('chat_history', []):
        with st.chat_message(chat_message["role"]):
            st.markdown(chat_message["content"])
    st.empty()
    # TODO: Move 120 to config
    user_input = st.chat_input("Hi there! I'm GenAI based chat-bot. Happy to answer vehicle queries.", max_chars=120)
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            assistant_response = get_answer(user_input, st.session_state.chat_history_for_summary)

            message_placeholder = st.empty()
            full_response = ""
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.08)
                message_placeholder.markdown(full_response + "✍")
            message_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.session_state.chat_history_for_summary.append((user_input, full_response))
            # TODO: Move 50 to config
            # Only have limited history
            if len(st.session_state.chat_history_for_summary) > 50:
                st.session_state.chat_history_for_summary.pop(0)
    def clear_chat():
        st.session_state.chat_history_for_summary = []
        st.session_state.chat_history = []
        st.empty()
    # TODO - move to appropriate place
    st.button("Clear Chat", key="train-youtube", on_click=clear_chat)

