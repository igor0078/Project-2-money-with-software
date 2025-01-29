from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def create_invoice_template(output_folder="PDF_INVOICE", filename="factuur_template.pdf"):
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Factuur")
    
    c.setFont("Helvetica", 12)
    
    # Bedrijfsgegevens
    bedrijfsgegevens = [
        ("Bedrijfsnaam:", 50, height - 90),
        ("Adres:", 50, height - 110),
        ("Postcode:", 50, height - 130),
        ("Plaats:", 50, height - 150),
        ("KVK-nummer:", 50, height - 170),
        ("BTW-nummer:", 50, height - 190),
        ("Telefoon:", 50, height - 210),
        ("E-mail:", 50, height - 230),
        ("Website:", 50, height - 250),
    ]
    for text, x, y in bedrijfsgegevens:
        c.drawString(x, y, text)
    
    # Factuurgegevens
    c.drawString(300, height - 90, "Factuurgegevens")
    factuurgegevens = [
        ("Factuurnummer:", 300, height - 110),
        ("Factuurdatum:", 300, height - 130),
        ("Vervaldatum:", 300, height - 150),
    ]
    for text, x, y in factuurgegevens:
        c.drawString(x, y, text)
    
    # Klantgegevens
    c.drawString(50, height - 280, "Klantgegevens")
    klantgegevens = [
        ("Naam:", 50, height - 300),
        ("Adres:", 50, height - 320),
        ("Postcode:", 50, height - 340),
        ("Plaats:", 50, height - 360),
    ]
    for text, x, y in klantgegevens:
        c.drawString(x, y, text)
    
    # Factuurregels
    c.drawString(50, height - 400, "Omschrijving")
    c.drawString(250, height - 400, "Aantal")
    c.drawString(350, height - 400, "Prijs per stuk (excl. BTW)")
    c.drawString(500, height - 400, "Totaal (excl. BTW)")
    
    # Lijn onder de koptekst
    c.line(50, height - 405, 550, height - 405)
    
    # Totaalbedrag sectie
    c.drawString(350, height - 500, "Subtotaal (excl. BTW):")
    c.drawString(350, height - 520, "BTW (21%):")
    c.drawString(350, height - 540, "Totaalbedrag (incl. BTW):")
    
    # Betalingsinstructies
    c.drawString(50, height - 600, "Betalingsinstructies")
    c.drawString(50, height - 620, "Graag betalen binnen 14 dagen op rekeningnummer:")
    c.drawString(50, height - 640, "Ten name van:")
    
    c.save()
    print(f"Template opgeslagen als: {filepath}")

create_invoice_template()
