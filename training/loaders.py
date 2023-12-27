import os
import tempfile
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import UnstructuredImageLoader
from pdf2image import convert_from_path
from langchain.document_loaders import PyPDFLoader



def load_text_file(uploaded_file):
    text_content = None
    file_path = os.path.join(tempfile.gettempdir(), 'training-files', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with open(file_path) as f:
        text_content = f.read()
    os.remove(file_path)
    return text_content

def load_html_file(uploaded_file):
    if False == os.path.exists(os.path.join(tempfile.gettempdir(), 'training-files')):
        os.makedirs(os.path.join(tempfile.gettempdir(), 'training-files'))
    file_path = os.path.join(tempfile.gettempdir(), 'training-files', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    html_loader = UnstructuredHTMLLoader(file_path)
    html_content = html_loader.load()
    os.remove(file_path)
    return html_content

def load_pdf_file(uploaded_file):
    if False == os.path.exists(os.path.join(tempfile.gettempdir(), 'training-files')):
        os.makedirs(os.path.join(tempfile.gettempdir(), 'training-files'))
    file_path = os.path.join(tempfile.gettempdir(), 'training-files', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    pdf_loader = PyPDFLoader(file_path)
    pdf_content = pdf_loader.load()
    os.remove(file_path)
    return pdf_content

def load_image_file(uploaded_file):
    if False == os.path.exists(os.path.join(tempfile.gettempdir(), 'training-files')):
        os.makedirs(os.path.join(tempfile.gettempdir(), 'training-files'))
    file_path = os.path.join(tempfile.gettempdir(), 'training-files', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    print ("pdf loading as images - start")
    pdf_images = convert_from_path(file_path, 500,
                                   poppler_path=str(st.secrets.pdfimage.popler_path))

    pdf_image_content = []
    
    for image in pdf_images:
       pageImage = 'pdf_page_'+ str(pdf_images.index(image))+'.jpg' 
       image.save(pageImage, 'JPEG')
       imageLoader = UnstructuredImageLoader(pageImage)
       pdf_image_content.extend(imageLoader.load())
       os.remove(pageImage)

    print(len(pdf_image_content))
    os.remove(file_path)
    return pdf_image_content   
