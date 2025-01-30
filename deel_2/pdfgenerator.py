import json
import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Mappen instellen
ORDER_DIR = "JSON_ORDER"
INVOICE_DIR = "JSON_INVOICE"
PROCESSED_DIR = "JSON_PROCESSED"

os.makedirs(ORDER_DIR, exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

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
    
    # Factuurdetails
    y_position = height - 70
    c.drawString(50, y_position, f"Factuurnummer: {json_data['factuur']['factuurnummer']}")
    c.drawString(50, y_position - 15, f"Datum: {json_data['factuur']['factuurdatum']}")
    y_position -= 30
    
    # Klantgegevens
    klant = json_data['factuur']['klant']
    c.drawString(50, y_position, f"Klant: {klant['naam']}")
    c.drawString(50, y_position - 15, f"Adres: {klant['adres']}, {klant['postcode']} {klant['stad']}")
    y_position -= 30
    
    # Producten
    c.drawString(50, y_position, "Omschrijving")
    c.drawString(250, y_position, "Aantal")
    c.drawString(350, y_position, "Prijs per stuk")
    c.drawString(500, y_position, "Totaal")
    y_position -= 15
    c.line(50, y_position, 550, y_position)
    
    subtotal = 0
    for item in json_data['factuur']['producten']:
        totaal_prijs = item['aantal'] * item['prijs_per_stuk_excl_btw']
        c.drawString(50, y_position - 15, item['productnaam'])
        c.drawString(250, y_position - 15, str(item['aantal']))
        c.drawString(350, y_position - 15, f"€ {item['prijs_per_stuk_excl_btw']:.2f}")
        c.drawString(500, y_position - 15, f"€ {totaal_prijs:.2f}")
        subtotal += totaal_prijs
        y_position -= 15
    
    btw = round(subtotal * 0.21, 2)
    totaal = round(subtotal + btw, 2)
    
    c.drawString(350, y_position - 15, f"Subtotaal: € {subtotal:.2f}")
    c.drawString(350, y_position - 30, f"BTW (21%): € {btw:.2f}")
    c.drawString(350, y_position - 45, f"Totaal: € {totaal:.2f}")
    
    c.save()
    print(f"Factuur opgeslagen: {output_path}")

# Verwerken van alle JSON-bestanden
for filename in os.listdir(ORDER_DIR):
    if filename.endswith(".json"):
        json_path = os.path.join(ORDER_DIR, filename)
        invoice_path = os.path.join(INVOICE_DIR, filename.replace(".json", ".pdf"))
        
        data = load_json(json_path)
        if data:
            create_invoice(data, invoice_path)
            shutil.move(json_path, os.path.join(PROCESSED_DIR, filename))
            print(f"Verwerkt en verplaatst: {filename}")
