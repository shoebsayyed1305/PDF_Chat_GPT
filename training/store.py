import os
import datetime
import streamlit as st
import pickle as pkl
from training.vectorstore import cleanup_store_folder
from training.vectorstore import store_chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
from training.loaders import load_text_file
from training.loaders import load_pdf_file
from training.loaders import load_html_file
from training.loaders import load_image_file


DUMP_FOLDER_PATH = os.path.join(os.getcwd(), 'store')
DUMP_FILE_PATH = os.path.join(DUMP_FOLDER_PATH, 'stored_docs.pkl')

def get_stored_doc_list():
    global DUMP_FILE_PATH
    if os.path.exists(DUMP_FILE_PATH):
        with open(DUMP_FILE_PATH, "rb") as f:
            stored_docs = pkl.load(f)
            return stored_docs
    else:
        stored_docs = []
        save_stored_doc_list(stored_docs)
        return stored_docs

def save_stored_doc_list(stored_doc_list):
    global stored_docs
    if os.path.exists(DUMP_FOLDER_PATH) == False:
        try:
            os.makedirs(DUMP_FOLDER_PATH)
        except FileExistsError:
            pass
    stored_docs = stored_doc_list
    with open(DUMP_FILE_PATH, "wb") as f:
        pkl.dump(stored_docs, f) 

def split_content(content, fileType):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = int(st.secrets.splitter.chunk_size),
        chunk_overlap = int(st.secrets.splitter.chunk_overlap),
        length_function = len)
    if (fileType == 'text'):
        txtChunks = text_splitter.split_text(content)
        chunks = text_splitter.create_documents(txtChunks)
    else:   
        chunks = text_splitter.split_documents(content)

    print(f"Number of chunks : {len(chunks)}.")   
    return chunks

def store_file(uploaded_file):
    content = None
    fileType = None
    if uploaded_file is not None:
        if 'text/plain' == uploaded_file.type:
            content = load_text_file(uploaded_file)
            fileType = 'text'
        elif 'application/pdf' == uploaded_file.type:
            content = load_pdf_file(uploaded_file)
            fileType = 'pdf'
        elif 'text/html' == uploaded_file.type:
            content = load_html_file(uploaded_file)
            fileType = 'html'
    if (content != None):
        chunks = split_content(content,fileType)
        if (len(chunks) == 0):
            content = load_image_file(uploaded_file)
            chunks = split_content(content,'pdf')
        
        store_chunks(chunks)
        now_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        stored_doc_list = get_stored_doc_list()
        stored_doc_list.append({'name': uploaded_file.name, 'type': uploaded_file.type, 'time': now_time})
        save_stored_doc_list(stored_doc_list)
    else:
        pass

def clear_store():
    cleanup_store_folder()
    save_stored_doc_list([])

