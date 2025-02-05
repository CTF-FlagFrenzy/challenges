import base64
import hashlib
import logging
import os

import fitz
from flask import Flask, send_from_directory
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def caesar_cipher(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result


def create_invoice_pdf(output_filename, flag):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Invoice title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, "Invoice")

    # Invoice details
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 100, "Invoice Number: 12345")
    c.drawString(30, height - 120, "Date: 2023-10-01")
    c.drawString(30, height - 140, "Bill To: John Doe")
    c.drawString(30, height - 160, "Address: 1234 Main St, Anytown, USA")

    # Table header
    c.setFillColor(colors.white)
    c.drawString(30, height - 200, "It's not that easy!")
    c.setFillColor(colors.black)
    c.rect(30, height - 205, 100, 15, fill=1)  # Black out the word "Description"
    c.setFillColor(colors.black)
    c.drawString(300, height - 200, "Quantity")
    c.drawString(400, height - 200, "Unit Price")
    c.drawString(500, height - 200, "Total")

    # Table content
    items = [("Widget A", 2, 50.00), ("Widget B", 1, 75.00), ("Widget C", 3, 20.00)]

    y = height - 220
    for item in items:
        description, quantity, unit_price = item
        total = quantity * unit_price
        # Black out the description
        c.setFillColor(colors.black)
        c.drawString(30, y, description)
        c.setFillColor(colors.black)
        c.drawString(300, y, str(quantity))
        c.drawString(400, y, f"${unit_price:.2f}")
        c.drawString(500, y, f"${total:.2f}")
        y -= 20

    # Total amount
    total_amount = sum(quantity * unit_price for _, quantity, unit_price in items)
    c.drawString(400, y - 20, "Total Amount:")
    c.drawString(500, y - 20, f"${total_amount:.2f}")

    # Hidden flag
    c.setFillColor(colors.white)
    c.drawString(100, 50, flag)

    c.save()
    logger.info(f"Basic PDF with first flag created successfully.")


def embed_file_in_pdf(pdf_path, textfile_path, output_pdf_path):
    # Open the existing PDF
    pdf_document = fitz.open(pdf_path)

    # Read the content of the text file
    with open(textfile_path, "rb") as file:
        file_content = file.read()

    # Embed the text file in the PDF
    pdf_document.embfile_add(textfile_path, file_content, filename=textfile_path)

    # Save the modified PDF to a new file
    pdf_document.save(output_pdf_path)
    logger.info(f"Embedded text file into PDF file successfully")


def create_pdf_full():

    challenge_flag = "#oLq3j&ZcF"
    challenge_flag_two = "M9LQXpX^Us"
    team_flag = os.getenv("TEAMKEY")

    combined_flag = challenge_flag + team_flag
    combined_flag_two = challenge_flag_two + team_flag

    hashed_flag = "FF{" + hashlib.sha256(combined_flag.encode()).hexdigest() + "}"
    logger.info(f"Flag in PDF successfully created and hashed {hashed_flag}")

    hashed_flag_two = (
        "FF{" + hashlib.sha256(combined_flag_two.encode()).hexdigest() + "}"
    )
    logger.info(f"Flag in text file successfully created and hashed {hashed_flag_two}")

    invoice_pdf = "flask_app/download/first.pdf"
    create_invoice_pdf(invoice_pdf, hashed_flag)

    # Encode the flag with Caesar Cipher (shift 5) and Base64
    caesar_encoded_flag = caesar_cipher(hashed_flag_two, 5)
    base64_encoded_flag = base64.b64encode(caesar_encoded_flag.encode()).decode()

    # Write the encoded flag to the text file
    text_file = "flask_app/download/flag.txt"
    with open(text_file, "w") as f:
        f.write(base64_encoded_flag)

    # Embed the text file with the encoded flag
    output_pdf = "flask_app/download/stealth_invoice.pdf"
    embed_file_in_pdf(invoice_pdf, text_file, output_pdf)


app = Flask(__name__)


@app.route("/")
def download_pdf():
    return send_from_directory(
        os.path.join(app.root_path, "download"), "stealth_invoice.pdf"
    )


if __name__ == "__main__":
    create_pdf_full()
    app.run(host="0.0.0.0", port=80)
