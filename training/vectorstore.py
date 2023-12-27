import os
import shutil
import pickle
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma

vectordb_wrapper = None

class FaissVectorDbWrapper:
    def __init__(self, embedding):
        self.vectordb = None
        self.store_folder_path = os.path.join(os.getcwd(), 'store')
        self.vectordb_file_name = "vectordb.pkl"
        self.embedding = embedding
        self.init_vectordb()

    def init_vectordb(self):
        if os.path.exists(os.path.join(self.store_folder_path, self.vectordb_file_name)):
            with open(os.path.join(self.store_folder_path, self.vectordb_file_name), "rb") as f:
                self.vectordb = pickle.load(f)
        else:
            self.vectordb = FAISS.from_texts(['a'], self.embedding)
            with open(os.path.join(self.store_folder_path, self.vectordb_file_name), "wb") as f:
                pickle.dump(self.vectordb, f)

    def cleanup_store_folder(self):
        if os.path.exists(self.store_folder_path):
            shutil.rmtree(self.store_folder_path, ignore_errors=True)
        self.init_vectordb()

    def store_chunks(self, chunks):
        new_chunks_vectordb = FAISS.from_documents(chunks, self.embedding)
        self.vectordb.merge_from(new_chunks_vectordb)
        with open(os.path.join(self.store_folder_path, self.vectordb_file_name), "wb") as f:
            pickle.dump(self.vectordb, f)

    def get_vectordb(self):
        return self.vectordb
    
class ChromaVectorDbWrapper:
    COLLECTION_NAME = "qna-langchain"
    def __init__(self, embedding):
        self.vectordb = None
        self.persist_directory = os.path.join(os.getcwd(), 'store', 'chroma')
        self.embedding = embedding
        self.init_vectordb()

    def init_vectordb(self):
        self.vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=self.embedding)

    def cleanup_store_folder(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory, ignore_errors=True)
        self.init_vectordb()

    def store_chunks(self, chunks):
        self.vectordb.add_documents(documents=chunks)
        self.vectordb.persist()

    def get_vectordb(self):
        return self.vectordb

def init_vectordb(type, embedding):
    global vectordb_wrapper
    if (vectordb_wrapper == None):
        if type == "FAISS":
            vectordb_wrapper = FaissVectorDbWrapper(embedding)
        else:
            vectordb_wrapper = ChromaVectorDbWrapper(embedding)
    return vectordb_wrapper.get_vectordb()

def cleanup_store_folder():
    global vectordb_wrapper
    vectordb_wrapper.cleanup_store_folder()

def store_chunks(chunks):
    global vectordb_wrapper
    vectordb_wrapper.store_chunks(chunks)

def get_vectordb():
    global vectordb_wrapper
    return vectordb_wrapper.get_vectordb()
