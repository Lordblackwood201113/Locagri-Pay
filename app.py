import streamlit as st
from appli import *
import time
from connexion import *
import streamlit_authenticator as stauth
from streamlit_modal import Modal
import streamlit.components.v1 as components
import pandas as pd
from deta import Deta
import datetime
import uuid
import os
from dotenv import load_dotenv
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from agstyler import PINLEFT, draw_grid, highlight
from connexion import database


st.set_page_config(layout="wide", page_title = "Locagri Pay", page_icon= ":evergreen_tree:")

authentication_status = False

if authentication_status == False :
    
    placeholder = st.empty()

    image_path = 'logo-locagri1.png'


    config = database()

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    placeholder.image(image_path)
    name, authentication_status, username = authenticator.login('Interface de connexion', 'main')
    
    if authentication_status == False:
        st.error("Nom d'utilisateur ou Mot de passe incorrecte")

    if authentication_status ==  None:
        st.warning("S'il vous plaît entrez votre Nom d'utilisateur et votre Mot de passe")


    if authentication_status :
        
        contact = config['credentials']['usernames'][str(username)]['contact']
        compte = config['credentials']['usernames'][str(username)]['compte']
        st.sidebar.title("Locagri Pay")
        st.sidebar.image(image_path, use_column_width=True)
        st.write(f'Bienvenue *{name}*')
        authenticator.logout('Déconnexion', 'sidebar')
        placeholder.empty()
        app(name, contact, compte)
    
