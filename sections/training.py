import streamlit as st
import pandas as pd
import time
from training.store import store_file
from training.store import clear_store
from training.store import get_stored_doc_list

already_training = False

def show():
    global already_training
    st.title("Document Ingestion")

    def train_data_file(data_file_path):
        global already_training

        if data_file_path is not None:
            already_training = True
            with st.spinner('Training in progress...'):
                store_file(data_file_path)
            already_training = False
            print(data_file_path.name)

    def train_cleanup():
        clear_store()

    file_upload_container = st.container()
    file_upload_container.subheader("Upload Files")

    with st.form("my-form", clear_on_submit=True, border=False):
        if data_file_path := st.file_uploader("Please upload data files (pdf / txt)...", type=["pdf", "txt"], disabled=already_training):
            st.session_state.data_file_path = data_file_path
        st.form_submit_button("Train", on_click=train_data_file(data_file_path))


    training_data_list_container = st.container()
    training_data_list_container.subheader("Saved Data List")
    stored_doc_list = get_stored_doc_list()
    data_list = []
    index_list = []
    for stored_info in stored_doc_list:
        data_list.append([stored_info['name'], stored_info['type']])
        index_list.append(stored_info['time'])
    df = df1 = pd.DataFrame(data_list, columns=['Name', 'Content Type'], index=index_list)
    training_data_list_container.table(df)
    training_data_list_container.write("")
    training_data_list_container.error("Do you really, really, wanna do this?")
    training_data_list_container.button("Cleanup Training Data", key="train-cleanup", on_click=train_cleanup, disabled=st.session_state.already_training)
