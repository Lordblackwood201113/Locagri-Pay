from deta import Deta
import os
from dotenv import load_dotenv
import streamlit as st
from agstyler import PINLEFT, draw_grid, highlight

import pandas as pd


def database() :
    #load_dotenv(".env")
    #DETA_KEY = os.getenv("DETA_KEY")
    DETA_KEY = "a0hye2esenw_Vtsyv7h3ggTWqyMJQNZEQCNWfszrBm8K"

    deta = Deta(DETA_KEY)

    db = deta.Base("example")

    db = deta.Base("example")

    config = db.fetch().items

    config = config[0]
    
    return config


def data_base() :
    
    #load_dotenv(".env")
    #DETA_KEY_APP = os.getenv("DETA_KEY")
    DETA_KEY_APP = "a0hye2esenw_Vtsyv7h3ggTWqyMJQNZEQCNWfszrBm8K"

    deta = Deta(DETA_KEY_APP)

    db = deta.Base("example-db")
    
    return db


def sauvegarder(data, db) :
        df = pd.DataFrame(data["data"])
        updated_data = df.to_dict(orient='records')

        for record in updated_data:
            db.put(record)


def dynamic (formatter, df) :
    go = { 'getRowStyle' : highlight("#fcccbb", "params.data.stat == 'Refusé' ")} 
    with st.expander("⏰ ENREGISTREMENT"):
        showData=st.multiselect('Filtrer: ',options= ['stat', 'key', 'date', 'time', "localite", "nom_technicien", "numero_technicien",'nom_producteur', 'numero_producteur', 'moy_paie', 'prix_achat', 'qt_achat', 'total'] , default=['stat', 'key', 'date', 'time', 'nom_producteur', 'numero_producteur', 'moy_paie', 'prix_achat', 'qt_achat', 'total'])
        selected_columns = {
            key: value
            for key, value in formatter.items()
            if key in showData
        }
        if showData != [] : 
            data = draw_grid(
                df,
                formatter=selected_columns,
                fit_columns=False,
                selection='multiple',
                use_checkbox='True', 
                grid_options=go
            )
    return data


    
    


    



