from tkinter import Tk, Canvas, Button, Label, Entry, CENTER, SOLID
from tkinter import ttk
from PIL import Image, ImageTk
import requests

# Couleurs
color1 = "#FFFFFF"  # Blanc
color2 = "#00BFFF"  # Bleu ciel éclatant
color3 = "#FF6F61"  # Corail
color4 = "#000000"  # Noir
color5 = "#005f85"  # Violet

# Liste des symboles de devises
currency_symbols = {
    "USD": "$", "BRL": "R$", "EUR": "€", "INR": "₹",
    "CAD": "$", "JPY": "¥", "CHF": "CHF", "GBP": "£",
    "XAF": "FCFA", "CNY": "¥", "COP": "$", "CLP": "$",
    "KMF": "CF", "ZAR": "R", "ZWD": "Z$", "RUB": "₽",
    "KES": "KSh", "NGN": "₦"
}

# Page d'accueil
def show_home_page():
    home_window = Tk()
    home_window.geometry("550x550")
    home_window.title("Page d'Accueil")
    home_window.resizable(height=False, width=False)

    # Charger l'image de fond
    image_path = "https://i.ibb.co/stNx1CJ/image.png"  # Remplacer par ton image
    response = requests.get(image_path, stream=True)
    if response.status_code == 200:
        with open("home_background.jpg", "wb") as f:
            f.write(response.content)

    bg_image = Image.open("home_background.jpg").resize((550, 550), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Ajouter l'image au Canvas
    canvas = Canvas(home_window, width=550, height=550)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Titre d'accueil
    label = Label(home_window, text="BIENVENUE DANS LE CONVERTISSEUR DE MONAIE ! ", font=("Ivy 21 bold"), bg=color1, fg=color5)
    canvas.create_window(269, 205, window=label)  # Positionner le texte sur le canvas

    # Bouton "Entrer"
    enter_button = Button(home_window, text="Entrer", font=("Ivy 12 bold"), bg=color3, fg=color5, command=lambda: (home_window.destroy(), show_main_page()))
    canvas.create_window(275, 250, window=enter_button)  # Positionner le bouton "Entrer"

    # Bouton "Quitter"
    quit_button = Button(home_window, text="Quitter", font=("Ivy 12 bold"), bg=color3, fg=color5, command=home_window.quit)
    canvas.create_window(275, 300, window=quit_button)  # Positionner le bouton "Quitter"

    home_window.mainloop()

# Page principale du convertisseur
def show_main_page():
    window = Tk()
    window.geometry("550x550")
    window.title("Convertisseur de monnaie")
    window.resizable(height=False, width=False)

    # Charger l'image de fond
    image_path = "https://www.made-in-mosaic.fr/Files/16786/Img/16/enduit-teinte-brut-argilus-blanc-casse-web-zoom.jpg"
    response = requests.get(image_path, stream=True)
    if response.status_code == 200:
        with open("background.jpg", "wb") as f:
            f.write(response.content)

    bg_image = Image.open("background.jpg").resize((550, 550), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Ajouter l'image au Canvas
    canvas = Canvas(window, width=550, height=550)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # API de conversion
    def convert():
        url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"

        # Récupération des données utilisateur
        currency_1 = combo1.get()
        currency_2 = combo2.get()
        amount = value.get()

        # Validation des champs
        if not currency_1 or not currency_2:
            result["text"] = "Veuillez sélectionner les devises."
            return

        # Vérification que le montant est un nombre
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Montant non valide.")
        except ValueError:
            result["text"] = "Veuillez entrer un montant numérique valide."
            return

        querystring = {"from": currency_1, "to": currency_2, "amount": amount}
        headers = {
            "x-rapidapi-host": "currency-converter18.p.rapidapi.com",
            "x-rapidapi-key": "90c59d6c9fmsh4599f814e2ffc92p17fc6djsndeaa0265ac61",
        }

        # Requête à l'API et gestion des erreurs
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            response.raise_for_status()  # Vérifie les erreurs HTTP
            data = response.json()
            converted_amount = "{:,.3f}".format(data["result"]["convertedAmount"])
            symbol = currency_symbols.get(currency_2, "")
            result["text"] = f"{symbol}{converted_amount}"
        except requests.exceptions.RequestException as e:
            result["text"] = "Erreur de connexion à l'API."
            print("Erreur lors de la requête :", e)
        except KeyError:
            result["text"] = "Conversion impossible."
            print("Erreur : structure inattendue dans la réponse JSON.")

    # Charger l'image du logo dans Tkinter
    logo_image = Image.open("logo.png").resize((60, 60), Image.LANCZOS)  # Augmentation de la taille de l'icône
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Définir l'interface
    vcmd = window.register(lambda action, value: action == "0" or value.replace('.', '', 1).isdigit())

    # Position dynamique
    center_x = 550 // 2  # Centre horizontal
    start_y = 120        # Point de départ vertical pour laisser de l'espace en haut
    spacing_y = 70      # Espace entre les widgets

    # Fonction pour ajouter un placeholder
    def add_placeholder(entry, placeholder_text):
        entry.insert(0, placeholder_text)  # Ajout du texte placeholder
        entry.configure(fg="grey")  # Texte en gris par défaut
        
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                entry.configure(fg="black")  # Texte noir lorsque l'utilisateur commence à entrer du texte
        
        def on_focus_out(event):
            if not entry.get():  # Si l'utilisateur ne rentre rien, réafficher le placeholder
                entry.insert(0, placeholder_text)
                entry.configure(fg="grey")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Champ d'entrée pour le montant
    value = Entry(
        canvas,
        width=27,
        justify=CENTER,
        font=("Ivy 16 bold"),
        relief=SOLID,
        validate="key",
        validatecommand=(vcmd, "%d", "%P"),
    )
    add_placeholder(value, "Veuillez entrer le montant")  
    canvas.create_window(center_x, start_y, window=value)

    # Label pour afficher le résultat
    result = Label(
        canvas,
        text="",
        width=32,
        height=1,
        pady=7,
        relief="groove",
        anchor=CENTER,
        font=("Ivy 16 bold"),
        bg=color1,
        fg=color5,
    )
    canvas.create_window(center_x, start_y + 3 * spacing_y, window=result)

    # Labels et combobox pour la sélection des devises
    from_label = Label(
        canvas,
        text="From",
        font=("Ivy 16 bold"), fg=color5
    )
    canvas.create_window(center_x - 80, start_y - spacing_y, window=from_label)

    combo1 = ttk.Combobox(canvas, width=10, justify=CENTER, font=("Ivy 16 bold"), state="readonly", background=color4, foreground=color1)
    combo1["values"] = list(currency_symbols.keys())
    canvas.create_window(center_x + 20, start_y - spacing_y, window=combo1)

    to_label = Label(
        canvas,
        text="To",
        font=("Ivy 16 bold"),
        fg=color5   
    )
    canvas.create_window(center_x - 80, start_y + spacing_y, window=to_label)

    combo2 = ttk.Combobox(canvas, width=10, justify=CENTER, font=("Ivy 16 bold"), state="readonly", background=color4, foreground=color1)
    combo2["values"] = list(currency_symbols.keys())
    canvas.create_window(center_x + 20, start_y + spacing_y, window=combo2)

    # Le bouton "Convertir"
    logo_button = Button(
        canvas,
        text="Convertir",  # Utilise l'image téléchargée
       pady=7,
        relief="groove",
        anchor=CENTER,
        font=("Ivy 16 bold"),
        bg=color1,
        fg=color5,         # Épaisseur de la bordure
        command=convert,  # Lance la fonction de conversion
    )
    canvas.create_window(center_x, start_y + 4 * spacing_y, window=logo_button)

    # Lancer de la fenêtre principale
    window.mainloop()

# Lancer la page d'accueil
show_home_page() 