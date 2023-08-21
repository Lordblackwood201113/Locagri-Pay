import streamlit_authenticator as stauth
from deta import Deta

hashed_passwords = stauth.Hasher(['Franck201113', 'administrateur', 'technicien']).generate()

data = {
    'credentials': {
        'usernames': {
            'daniel': {
                'email': 'gle.yao@inphb.ci',
                'name': 'YAO GLE YAO FRANCK DANIEL',
                'contact' : '+225 07 59 78 85 97',
                'compte' : 'administrateur',
                'password': hashed_passwords[0] 
            },
            'Administrateur': {
                'email': 'administrateur@gmail.com',
                'name': 'ADMINISTRATEUR',
                'contact' : '+225 07 00 00 00 00',
                'compte' : 'administrateur',
                'password': hashed_passwords[1] 
            },
            'technicien': {
                'email': 'technicien@gmail.com',
                'name': 'TECHNICIEN',
                'contact' : '+225 07 00 00 00 00',
                'compte' : 'utilisateur',
                'password': hashed_passwords[2] 
            },
        }
    },
    'cookie': {
        'expiry_days': 1,
        'key': 'some_signature_key',
        'name': 'some_cookie_name'
    },
    'preauthorized': {
        'emails': [
            ''
        ]
    }
}

#with open('config.yaml', 'w') as config_file:
    #yaml.dump(data, config_file)


DETA_KEY = "a0hye2esenw_Vtsyv7h3ggTWqyMJQNZEQCNWfszrBm8K"

deta = Deta(DETA_KEY)

db = deta.Base("example")

db.update(key = "1m0za4838jry", updates = data)


