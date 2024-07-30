from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io
import os
from PIL import Image
from reportlab.lib.utils import ImageReader

def create_pdf(filename, duration, wave_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add audio file name
    c.drawString(100, height - 100, f"Audio File: {filename}")

    # Add duration
    c.drawString(100, height - 120, f"Duration: {duration:.2f} seconds")

    # Create and add audio wave plot
    plt.figure(figsize=(6, 2))
    plt.plot(wave_data)
    plt.axis('off')
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Convert BytesIO to ImageReader
    img_reader = ImageReader(img_buffer)
    
    # Draw the image
    c.drawImage(img_reader, 100, height - 350, width=400, height=200)

    c.save()
    buffer.seek(0)

    # Save to a temporary file
    media_folder = 'media'  # Make sure this folder exists
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    pdf_path = os.path.join(media_folder, "output.pdf")

    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(buffer.getvalue())

    return pdf_path