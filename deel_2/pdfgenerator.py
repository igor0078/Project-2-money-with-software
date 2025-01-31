import json
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Mappen instellen
ORDER_DIR = "JSON_ORDER"
INVOICE_DIR = "JSON_INVOICE"
PROCESSED_DIR = "JSON_PROCESSED"
ERROR_DIR = "JSON_ORDER_ERROR"

os.makedirs(ORDER_DIR, exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ERROR_DIR, exist_ok=True)

# Functie om JSON-bestand in te lezen
def load_json(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Fout bij het lezen van {filepath}: {e}")
        return None

# Functie om factuur aan te maken
def create_invoice(json_data, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica", 8)  # Kleinere lettergrootte
    c.drawString(50, height - 50, "Factuur")
    
    # Controleren of de 'order' sleutel aanwezig is
    if 'order' not in json_data:
        raise KeyError("'order' niet gevonden in de JSON-structuur.")
    
    # Factuurdetails
    y_position = height - 90
    order = json_data['order']
    c.drawString(50, y_position, f"Ordernummer: {order.get('ordernummer', 'N/A')}")
    c.drawString(50, y_position - 20, f"Datum: {order.get('orderdatum', 'N/A')}")
    c.drawString(50, y_position - 40, f"Betaaltermijn: {order.get('betaaltermijn', 'N/A')}")
    y_position -= 60
    
    # Klantgegevens
    klant = order.get('klant', {})
    c.drawString(50, y_position, f"Klant: {klant.get('naam', 'N/A')}")
    c.drawString(50, y_position - 20, f"Adres: {klant.get('adres', 'N/A')}, {klant.get('postcode', 'N/A')} {klant.get('stad', 'N/A')}")
    y_position -= 40
    
    # Producten
    c.drawString(50, y_position, "Omschrijving")
    c.drawString(250, y_position, "Aantal")
    c.drawString(350, y_position, "Prijs per stuk")
    c.drawString(500, y_position, "Totaal")
    y_position -= 20
    c.line(50, y_position, 550, y_position)
    
    subtotal = 0
    producten = order.get('producten', [])
    if not producten:
        raise KeyError("'producten' niet gevonden in de JSON-structuur.")
    
    for item in producten:
        totaal_prijs = item.get('aantal', 0) * item.get('prijs_per_stuk_excl_btw', 0)
        c.drawString(50, y_position - 20, item.get('productnaam', 'N/A'))
        c.drawString(250, y_position - 20, str(item.get('aantal', 'N/A')))
        c.drawString(350, y_position - 20, f"€ {item.get('prijs_per_stuk_excl_btw', 0):.2f}")
        c.drawString(500, y_position - 20, f"€ {totaal_prijs:.2f}")
        subtotal += totaal_prijs
        y_position -= 20
    
    btw = round(subtotal * 0.21, 2)
    totaal = round(subtotal + btw, 2)
    
    c.drawString(350, y_position - 20, f"Subtotaal: € {subtotal:.2f}")
    c.drawString(350, y_position - 40, f"BTW (21%): € {btw:.2f}")
    c.drawString(350, y_position - 60, f"Totaal: € {totaal:.2f}")
    
    c.save()
    print(f"Factuur opgeslagen: {output_path}")

# Verwerken van alle JSON-bestanden
for filename in os.listdir(ORDER_DIR):
    if filename.endswith(".json"):
        json_path = os.path.join(ORDER_DIR, filename)
        invoice_path = os.path.join(INVOICE_DIR, filename.replace(".json", ".pdf"))
        
        data = load_json(json_path)
        if data:
            try:
                create_invoice(data, invoice_path)
                shutil.move(json_path, os.path.join(PROCESSED_DIR, filename))
                print(f"Verwerkt en verplaatst: {filename}")
            except KeyError as e:
                print(f"Fout bij het verwerken van {filename}: {e}")
                shutil.move(json_path, os.path.join(ERROR_DIR, filename))  # Fout bestand verplaatsen
                print(f"Bestand met fout verplaatst naar {ERROR_DIR}: {filename}")
            except Exception as e:
                print(f"Onverwachte fout bij {filename}: {e}")
                shutil.move(json_path, os.path.join(ERROR_DIR, filename))  # Fout bestand verplaatsen
                print(f"Bestand met fout verplaatst naar {ERROR_DIR}: {filename}")
        else:
            shutil.move(json_path, os.path.join(ERROR_DIR, filename))  # Fout bestand verplaatsen
            print(f"Bestand zonder geldige data verplaatst naar {ERROR_DIR}: {filename}")
