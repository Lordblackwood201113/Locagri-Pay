from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
import qrcode


def receipt (key, date, time, prix_achat, qt_achat, total, name, nom_producteur, numero_producteur, moy_paie, contact, localite) :
    
    data = str({"key" : key,
            "date" : str(date),
            "time" : str(time),
            "localite" : localite,
            "nom_technicien" : name,
            "numero_technicien" : contact,
            "nom_producteur": nom_producteur,
            "numero_producteur": numero_producteur,
            "moy_paie" : moy_paie, 
            "prix_achat": prix_achat,
            "qt_achat" : qt_achat,
            "total" : total,
            "stat" : 'En cours'})
    
    #img = qrcode.make(data)
    
    
    qr = qrcode.QRCode(
        version=2,
        box_size=1)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qrcode.jpg')
    x = 20
    y = 650
    title = "reçu {}.pdf".format(key)
    c = canvas.Canvas(title, pagesize=(169.3*mm, 275.9*mm))
    c.setFont("Helvetica-Bold", 33.5) 
    c.drawString(x, y, "Reçu de Transaction")

    dat = "Date d'édition : {} à {}".format(date.strftime("%d/%m/%Y"), time)
    y -= 50
    c.setFont("Helvetica", 20.5)
    c.drawString(x, y, dat)

    Lieu = "Lieu : {}".format(localite)
    y -= 30
    c.setFont("Helvetica", 20.5)
    c.drawString(x, y, Lieu)

    y -= 30
    c.setLineWidth(2)
    c.line(x,y,460,y)
    #-------------- Détail de la transaction ---------------------
    y -= 40
    c.setFont("Helvetica-Bold", 22.5) 
    c.drawString(x, y, "Détail de la transaction")

    ID = "ID : {}".format(key)
    y -= 30
    c.setFont("Helvetica", 18.5) 
    c.drawString(x, y, ID)

    prix_unit = "Prix unitaire : {} FCFA/kg".format(prix_achat)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, prix_unit)
    
    
    qt_tot = "Quantité total : {} kg".format(qt_achat)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, qt_tot)

    prix_tot = "Prix total : {} FCFA".format(total)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, prix_tot)

    y -= 30
    c.setLineWidth(2)
    c.line(x,y,460,y)

    #-------------- Information Technicien ---------------------

    y -= 40
    c.setFont("Helvetica-Bold", 22.5) 
    c.drawString(x, y, "Information Technicien")

    nom_tech = "Nom et prénoms : {}".format(name)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, nom_tech )

    contact_tech = "Contact : {}".format(contact)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, contact_tech)

    y -= 30
    c.setLineWidth(2)
    c.line(x,y,460,y)

    #-------------- Information Producteur ---------------------
    y -= 40
    c.setFont("Helvetica-Bold", 22.5) 
    c.drawString(x, y, "Information Producteur")
    
    nom_pro = "Nom et prénoms : {}".format(nom_producteur)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, nom_pro)

    cont_pro = "Contact : {}".format(numero_producteur)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, cont_pro)

    Meth_pai = "Méthode de paiement : {}".format(moy_paie)
    y -= 30
    c.setFont("Helvetica", 18.5)
    c.drawString(x, y, Meth_pai)

    y -= 30
    c.setLineWidth(2)
    c.line(x,y,460,y)

    c.drawImage("logo-locagri2.jpg", x-5,700, width=5.68*cm,height=2*cm)
    c.drawImage('qrcode.jpg', 350,700)
    c.showPage()
    c.save()