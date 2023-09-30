import streamlit as st
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
from connexion import *
from test import *
import streamlit_authenticator as stauth
import base64
from io import BytesIO
from pdf import show_pdf
import pygwalker as pyg
from requete import requete


def app(name, contact, compte) :

    image_path = 'logo-locagri1.png'
    st.sidebar.title("Contacts")
    st.sidebar.info(
        """
        [LinkedIn](https://www.linkedin.com/in/sarl-locagri-nature-based-solutions-climate-foods-security-b69b221b1/) | 
        [Email](contact@locagri-ci.com) | 

        | [Téléphone](27 22 59 56 68) | 
        """
    )

    #load_dotenv(".env")
    #DETA_KEY_APP = os.getenv("DETA_KEY")
    DETA_KEY_APP ="a0hye2esenw_Vtsyv7h3ggTWqyMJQNZEQCNWfszrBm8K"

    deta = Deta(DETA_KEY_APP)

    db = deta.Base("example-db")
    
    produit = {
        "C26" : "6482761c1cbee308d1f23ed5",
        "CY2" : "648314bf1cbee308d1f23edb",
        "AIR BURKINA" : "64898b7cb8096f1c60731872",
        "JT11" : "6492ce64b8096f1c60731899",
    }
    
    if compte == 'utilisateur' :
        col1 = st.columns(1)

        date_actuelle = datetime.datetime.now().date()
        heure_actuelle = datetime.datetime.now().time()

        with st.form( key = "LOCAGRI PAY", clear_on_submit= True):
            st.image(image_path, use_column_width=True)
            with st.expander("Information Générale"):
                date = st.date_input("Date d'aujourd'hui", value=date_actuelle, format="DD/MM/YYYY", disabled=True)
                time = st.time_input("Heure actuelle", value = heure_actuelle, disabled=True)
                localite = st.text_input("Localité ", help="Le nom du village o u de la ville")
                nom_technicien = st.text_input("Nom et prénoms du technicien ", value= name, disabled=True)
                numero_technicien = st.text_input("Contact du technicien ", value= contact, disabled=True)
            with st.expander("Détail de la Transaction"):
                variete = st.selectbox("Variété de riz", options=["C26", "CY2", "AIR BURKINA", "JT11", "WITTA9"], help="Variété de riz acheté")
                prix_achat = st.number_input("Prix d'achat (FCFA)", value = 150, max_value= 250, help = "Prix d'achat de 1 kilogramme en FCFA")
                qt_achat = st.number_input("Quantité total acheté (kg)", help = "La quantité total de riz acheté en kg", min_value=0)
                total = prix_achat * qt_achat
            with st.expander("Information Producteur"):
                nom_producteur = st.text_input("Nom et prénoms du producteur", help="Noms et prénoms du producteur")
                numero_producteur = st.text_input("Conatct du producteur", value = "+225", help= "Contact Mobile money")
                moy_paie = st.selectbox("Méthode de paiement", options=["Orange money", "MTN money", "Moov money", "Wave"], help="Méthode de paiment mobile money")
            open_modal = st.form_submit_button("ACHETER")
            
            
        modal = Modal(title="Locagri Pay", key="2289")

        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                global uuid_str
                attention = "<span style='font-size:18px;'>ATTENTION, VOUS ALLEZ ENVOYER UN ORDRE D'ACHAT</span>"
                st.markdown(attention, unsafe_allow_html=True)
                message = "<span style='font-size:18px; background-color : green'>Total : {} FCFA</span>".format(total)
                components.html(message, height=50)
                close = st.button("Confirmez")
                uuid_al = uuid.uuid4()
                uuid_str = str(uuid_al)
                if close :
                    # Générer un UUID version 4 (aléatoire)
                    a = 1 
                    pdf_buffer = BytesIO()
                    receipt (uuid_str, date, time, prix_achat, qt_achat, total, name, nom_producteur, numero_producteur, moy_paie, contact, localite, variete)
                    if (a == 1) :
                        variete = produit[variete] 
                        #requete(total, qt_achat, prix_achat, variete)
                        a = 0
                    pdf_buffer.seek(0)
                    b64_pdf = base64.b64encode(pdf_buffer.read()).decode("utf-8")

                    db.put({"key" : uuid_str,
                            "date" : str(date),
                            "time" : str(time),
                            "localite" : localite,
                            "variete " : variete,
                            "nom_technicien" : nom_technicien,
                            "numero_technicien" : numero_technicien,
                            "nom_producteur": nom_producteur,
                            "numero_producteur": numero_producteur,
                            "moy_paie" : moy_paie, 
                            "prix_achat": prix_achat,
                            "qt_achat" : qt_achat,
                            "total" : total,
                            "stat" : 'En cours'})
                    sucess = True 
                    modal.close()

        if st.sidebar.button("Télécharger") :
            
            try: uuid_str
            except NameError: uuid_str = None
            
            if uuid_str is None :
                st.warning('Aucun reçu disponible', icon="⚠️")
            else :
                rec = "reçu {}.pdf".format(uuid_str)
                data_dive = detadrive()
                data_dive.put(rec, path= rec)
                show_pdf(rec)
                st.success("PDF charger avec succès", icon="⏰")
                

    if compte == 'administrateur' :

        db_content = db.fetch().items
        df = pd.DataFrame(db_content)

        status = ['En cours' , 'Refusé' , 'Validé'] 
        formatter = { 
            'stat' : ('Status',{
                'editable' : True,
                'cellEditor' : 'agSelectCellEditor',
                'cellEditorParams' : {
                    'values' : [ '' ] + status,
                }, 'width' : 150,
            }), 
            'key' : ( 'ID' , { 'width' : 150 }), 
            'date' : ( 'Date' , { 'width' : 150 }), 
            'time' : ( 'Heure' , { 'width' : 150 }),
            'localite' : ( 'Localité' , { 'width' : 150 }),
            "variete" : ( 'Variété' , { 'width' : 150 }),
            'nom_technicien' : ( 'Nom du technicien' , { 'width' : 150 }), 
            'numero_technicien' : ( 'Numéro du technicien' , { 'width' :150 }), 
            'nom_producteur' : ( 'Nom du producteur' , { 'width' : 150 }), 
            'numero_producteur' : ( 'Numéro du producteur' , { 'width' :150 }),
            'moy_paie' : ( 'Méthode de paiement' , { 'width' : 150 }),
            'variete' : ( 'Variété' , { 'width' : 150 }),
            'prix_achat' : ( "Prix d'achat (FCFA)" , { 'width' : 150 }),
            'qt_achat' : ( "Quantité acheté (kg)" , { 'width' : 150 }),
            'total' : ( "Coût total (FCFA)" , { 'width' : 150 }), 
        }

        data = dynamic (formatter, df)
        
        df = data['selected_rows']
        df = pd.DataFrame(df)
               
        if st.sidebar.button('Télécharger'):
            df = df.iloc[:, 1:15]
            df.to_excel("output.xlsx")
        #with st.expander("⏰ VISUALISATION & GRAPHIQUE "):
            #pyg_html = pyg.walk(df, return_html=True)
            #components.html(pyg_html, height=1000, scrolling=True)

        if st.button("Sauvegarder") :
            sauvegarder(data, db)


    
    

