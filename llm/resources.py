import streamlit as st
from training.vectorstore import init_vectordb
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
# from langchain.memory import ConversationTokenBufferMemory

qa = None
embedding = None

def get_embedding():
    global embedding

    if embedding == None:
        embedding = AzureOpenAIEmbeddings(
            model = st.secrets.embedding.model,
            openai_api_key = st.secrets.embedding.openai_api_key,
            openai_api_base = st.secrets.embedding.openai_api_base,
            openai_api_type = st.secrets.embedding.openai_api_type,
            chunk_size = st.secrets.embedding.chunk_size
            )
    return embedding

def get_qa():
    global qa
    llm = AzureChatOpenAI(
        openai_api_base = st.secrets.llm.openai_api_base,
        openai_api_key = st.secrets.llm.openai_api_key,
        openai_api_type = st.secrets.llm.openai_api_type,
        openai_api_version = st.secrets.llm.openai_api_version,
        temperature = float(st.secrets.llm.temperature)
        )
    # memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=500)
    vectordb = init_vectordb("Chromadb", get_embedding())
    retriever = vectordb.as_retriever(search_type='similarity', search_kwargs={'k': 3})

    system_template_with_reference = r""" 
    Given a specific context, please give a short answer to the question, covering the required advices in general and then provide the names all of relevant(even if it relates a bit) products.
    After the answer, please mention the reference document name and page number in next para. 
    ----
    {context}
    ----
    """
    general_user_template = "Question:```{question}```"
    qa_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template_with_reference),
        HumanMessagePromptTemplate.from_template(general_user_template)
    ])

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=retriever,
        # memory=memory,
        combine_docs_chain_kwargs={'prompt': qa_prompt},
        verbose=False
    )
    return qa
