import streamlit as st
from streamlit_option_menu import option_menu
import sections.about as about
import sections.training as training
import sections.queries as queries
from llm.resources import get_qa

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'chat_history_for_summary' not in st.session_state:
        st.session_state['chat_history_for_summary'] = []
    if 'already_training' not in st.session_state:
        st.session_state['already_training'] = False
    if 'data_file_path' not in st.session_state:
        st.session_state['data_file_path'] = None
    if 'youtube_link' not in st.session_state:
        st.session_state['youtube_link'] = None

def display_sidebar_options():
    with st.sidebar:
        st.image("https://www.persistent.com/wp-content/uploads/2021/04/Logo-variants-Primary-vertical.jpg")
        st.title("Vehicle Query System")
        st.write("")
        st.write("")
        
        selected_page = option_menu(
            menu_title=None,
            options=['Q & A', 'Document Ingestion', 'About Team D'],
            icons=['chat', 'wrench', 'info-circle'],
            default_index=0,
            )
    if selected_page == 'Q & A':
        queries.show()
    elif selected_page == 'Document Ingestion':
        training.show()
    elif selected_page == 'About Team D':
        about.show()
    else:
        queries.show()

if __name__=='__main__':

    initialize_session_state()
    get_qa()
    st.set_page_config(page_title="Team D: Vehicle Query Handler")
    st.markdown(
    r"""
    <style>
    .stDeployButton {
        visibility: hidden;
    }
    [data-testid=stSidebar] [data-testid=stImage]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    [data-testid=stSidebar] [data-testid=stMarkdownContainer]{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
    #MainMenu {
        visibility: hidden;
    }
    [data-testid="stStatusWidget"] {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True
    )
    display_sidebar_options()
