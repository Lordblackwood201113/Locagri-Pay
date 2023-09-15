import requests
from num2words import num2words

def requete (total, qt_achat, prix_achat) : 

    data = {
        'IdPlanteur' : '648882f7b8096f1c60731862' ,
        'IdDemandeur' : '648882f7b8096f1c60731862',
        'IdUtilisateur' : '64f0ad3b0b7a0b102e418003',
        'Source' : 'LOCAGRI 2.0',
        'CoutTotal' : str(total),
        'Quantite' : str(qt_achat),
        'Status' : 'en_attente',
        'Manu' : 'non',
        'CoutTotalenLettre' : num2words(total, lang='fr')
    }

    r = requests.post('https://api.locagri.digi-pme.com/users/apiv1/creatReception', data= data)

    print(r.text)

    data_mvt = {
        'IdPlanteur' : '648882f7b8096f1c60731862' ,
        'Originemv' : r.text,
        'Sensmvt' : 'Entree',
        'manu' : 'non',
        'IdVariete' : '64898b7cb8096f1c60731872',
        'Quantite' : str(qt_achat),
        'Coutunitaire' : str(prix_achat),
        'Entrepot' : ' ',
        'Ilot' : ' '
    }
    
    r = requests.post('https://api.locagri.digi-pme.com/users/apiv1/creatMouvements', data= data_mvt)

    print(r.text)
