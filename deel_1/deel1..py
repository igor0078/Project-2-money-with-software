import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf(text):
    # Maak de map 'PDF_INVOICE' aan als deze nog niet bestaat
    if not os.path.exists("PDF_INVOICE"):
        os.makedirs("PDF_INVOICE")

    # Pad naar de PDF
    pdf_path = os.path.join("PDF_INVOICE", "output.pdf")

    # Maak een PDF-document aan
    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Stel de tekst in
    c.setFont("Helvetica", 12)
    c.drawString(72, 750, text)  # (x, y, text)

    # Sla de PDF op
    c.save()

    print(f"PDF is opgeslagen in: {pdf_path}")

if __name__ == "__main__":
    # Vraag de gebruiker om tekst in te voeren
    user_text = input("Voer een stukje tekst in: ")

    # Genereer de PDF
    create_pdf(user_text)