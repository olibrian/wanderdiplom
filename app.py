"""
Wanderdiplom PDF Generator Web App

This Flask application allows users to generate personalized PDF diplomas
by filling out a form and selecting a diploma type. The app uses PyMuPDF (fitz)
to manipulate PDF templates and insert user-provided names.
"""
import os
from flask import Flask, request, render_template, send_file
import fitz  # PyMuPDF

app = Flask(__name__)

# Folder structure for templates and outputs
TEMPLATE_DIR = "templates"
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to insert text into a PDF template
def insert_text_into_pdf(template_path, output_path, name):
    """
    Inserts a name at a specific position into a PDF template.
    :param template_path: Path to the PDF template
    :param output_path: Path to the output PDF
    :param name: The name to be inserted
    """
    # A4 page dimensions and text area
    a4_width = 595  # Width of an A4 PDF in points
    left_margin = 50
    right_margin = 50

    doc = fitz.open(template_path)
    page = doc[0]  # Work on the first page

    # Define a rectangle where the text will be centered
    rect = fitz.Rect(left_margin, 170, a4_width - right_margin, 200)

    # Insert text
    page.insert_textbox(
        rect,
        name,
        fontsize=20,
        fontname="helv",
        color=(0, 0, 0),
        align=1     # Center alignment
    )

    # Save the PDF
    doc.save(output_path)
    doc.close()

@app.route('/')
def home():
    """
    Render the home page with the input form.
    """
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """
    Handle PDF generation request, validate input, and return the generated PDF or an error message.
    """
    name = request.form.get("name")
    diploma_type = request.form.get("diploma_type")  # Selection of the diploma type

    if not name or not diploma_type:
        return "Bitte geben Sie einen Namen und wählen Sie ein Wanderdiplom aus!", 400

    # Template paths for the different diplomas
    template_map = {
        "1": os.path.join(TEMPLATE_DIR, "wanderdiplom1.pdf"),
        "2": os.path.join(TEMPLATE_DIR, "wanderdiplom2.pdf"),
        "3": os.path.join(TEMPLATE_DIR, "wanderdiplom3.pdf")
    }

    # Select the correct template based on the selection
    template_path = template_map.get(diploma_type)
    if not template_path or not os.path.exists(template_path):
        return "Die ausgewählte Vorlage wurde nicht gefunden.", 400

    # Generate output path and personalize the PDF
    output_path = os.path.join(OUTPUT_FOLDER, f"diploma_{diploma_type}_{name}.pdf")
    insert_text_into_pdf(template_path, output_path, name)

    # Provide the personalized PDF to the user
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
