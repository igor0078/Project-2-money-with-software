import tkinter as tk
from tkinter import filedialog
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Functie om JSON-bestand in te lezen
def load_json(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Functie om de factuurgegevens uit JSON te halen en PDF te genereren
def create_invoice_from_json(json_data, output_folder="PDF_INVOICE", filename="factuur_gevuld.pdf"):
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Factuur")
    
    c.setFont("Helvetica", 12)
    
    y_position = height - 90

    # Bedrijfsgegevens
    bedrijfsgegevens = [
        ("Bedrijfsnaam:", json_data["order"]["klant"]["naam"]),
        ("Adres:", json_data["order"]["klant"]["adres"]),
        ("Postcode:", json_data["order"]["klant"]["postcode"]),
        ("Plaats:", json_data["order"]["klant"]["stad"]),
        ("KVK-nummer:", json_data["order"]["klant"]["KVK-nummer"]),
    ]
    for label, value in bedrijfsgegevens:
        c.drawString(50, y_position, label)
        c.drawString(200, y_position, value)
        y_position -= 20

    # Factuurgegevens
    c.drawString(300, height - 90, "Factuurgegevens")
    factuurgegevens = [
        ("Factuurnummer:", json_data["order"]["ordernummer"]),
        ("Orderdatum:", json_data["order"]["orderdatum"]),
        ("Betaaltermijn:", json_data["order"]["betaaltermijn"]),
    ]
    y_position = height - 130
    for label, value in factuurgegevens:
        c.drawString(300, y_position, label)
        c.drawString(450, y_position, value)
        y_position -= 20

    # Klantgegevens
    c.drawString(50, height - 250, "Klantgegevens")
    klantgegevens = [
        ("Naam:", json_data["order"]["klant"]["naam"]),
        ("Adres:", json_data["order"]["klant"]["adres"]),
        ("Postcode:", json_data["order"]["klant"]["postcode"]),
        ("Plaats:", json_data["order"]["klant"]["stad"]),
    ]
    y_position = height - 270
    for label, value in klantgegevens:
        c.drawString(50, y_position, label)
        c.drawString(200, y_position, value)
        y_position -= 20
    
    # Factuurregels
    c.drawString(50, y_position, "Omschrijving")
    c.drawString(250, y_position, "Aantal")
    c.drawString(350, y_position, "Prijs per stuk (excl. BTW)")
    c.drawString(500, y_position, "Totaal (excl. BTW)")
    y_position -= 20
    c.line(50, y_position, 550, y_position)
    
    # Producten
    subtotal = 0
    for item in json_data["order"]["producten"]:
        c.drawString(50, y_position - 20, item["productnaam"])
        c.drawString(250, y_position - 20, str(item["aantal"]))
        c.drawString(350, y_position - 20, f"€ {item['prijs_per_stuk_excl_btw']:.2f}")
        totaal_per_product = item["aantal"] * item["prijs_per_stuk_excl_btw"]
        c.drawString(500, y_position - 20, f"€ {totaal_per_product:.2f}")
        subtotal += totaal_per_product
        y_position -= 20
        if y_position < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
    
    # BTW en Totaalbedrag
    btw = round(subtotal * 0.21, 2)
    totaal = round(subtotal + btw, 2)
    c.drawString(350, y_position - 20, f"Subtotaal (excl. BTW): € {subtotal:.2f}")
    c.drawString(350, y_position - 40, f"BTW (21%): € {btw:.2f}")
    c.drawString(350, y_position - 60, f"Totaalbedrag (incl. BTW): € {totaal:.2f}")
    
    # Betalingsinstructies
    y_position -= 100
    c.drawString(50, y_position, "Betalingsinstructies:")
    c.drawString(50, y_position - 20, "Graag betalen binnen 14 dagen op rekeningnummer:")
    c.drawString(50, y_position - 40, "Ten name van: Software Solutions B.V.")
    c.drawString(50, y_position - 60, "Rekeningnummer: NL91ABNA0417164300")

    c.save()
    print(f"Factuur opgeslagen als: {filepath}")


# Functie om bestandspad te selecteren via bestandsdialoog
def select_file():
    root = tk.Tk()
    root.withdraw()  # Verberg het hoofdvenster
    file_path = filedialog.askopenfilename(
        title="Kies een JSON-bestand",
        filetypes=(("JSON bestanden", "*.json"), ("Alle bestanden", "*.*")),
        initialdir=r"C:\School\code\Project-2-money-with-software\deel_2\data"
    )
    return file_path

# Gebruik
json_file = select_file()  # Open de bestandsdialoog
if json_file:  # Als er een bestand geselecteerd is
    json_data = load_json(json_file)
    if json_data:
        create_invoice_from_json(json_data)
else:
    print("Er is geen bestand geselecteerd.")
