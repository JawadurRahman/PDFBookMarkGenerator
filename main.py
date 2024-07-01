# app.py
from flask import Flask, send_file, send_from_directory, render_template, request
from PyPDF2 import PdfReader, PdfWriter
import os
import io


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit


@app.route('/')
def index():
    return render_template('index.html')

"""
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
"""
"""

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Handle file upload
    pdfFile = request.files['pdfFile']
    if pdfFile and pdfFile.filename.endswith('.pdf'):
        pdfFilePath = os.path.join(app.config['UPLOAD_FOLDER'], pdfFile.filename)
        pdfFile.save(pdfFilePath)
    else:
        return 'Error: Please upload a valid PDF file.'

    # Process bookmark data
    outlines = []
    index = 1  # Start with 1 for naming consistency with HTML field names
    while f'bookmarkName{index}' in request.form:
        bookmarkName = request.form[f'bookmarkName{index}']
        pageNumber = int(request.form[f'pageNumber{index}']) - 1
        outlines.append((bookmarkName, pageNumber))
        index += 1

    # Generate new PDF with outlines
    pdf = PdfReader(open(pdfFilePath, 'rb'))
    pdf_writer = PdfWriter()

    for page in range(len(pdf.pages)):
        pdf_writer.add_page(pdf.pages[page])

    for bookmarkName, pageNumber in outlines:
        pdf_writer.add_outline_item(bookmarkName, pageNumber)

    newPdfFilePath = os.path.join(app.config['UPLOAD_FOLDER'], 'new_pdf.pdf')
    with open(newPdfFilePath, 'wb') as f:
        pdf_writer.write(f)

    return f'PDF generated successfully! <a href="/{newPdfFilePath}">Download</a>'
"""

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Handle file upload
    pdfFile = request.files['pdfFile']
    if pdfFile and pdfFile.filename.endswith('.pdf'):
        pdfBytes = pdfFile.read()  # Read PDF file content

        # Process bookmark data and generate new PDF with outlines
        outlines = []
        index = 1
        while f'bookmarkName{index}' in request.form:
            bookmarkName = request.form[f'bookmarkName{index}']
            pageNumber = int(request.form[f'pageNumber{index}']) - 1
            outlines.append((bookmarkName, pageNumber))
            index += 1

        # Generate new PDF with outlines in memory
        pdf_writer = PdfWriter()
        pdf_stream = io.BytesIO(pdfBytes)
        pdf_reader = PdfReader(pdf_stream)

        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

        for bookmarkName, pageNumber in outlines:
            pdf_writer.add_outline_item(bookmarkName, pageNumber)

        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        output_stream.seek(0)

        # Send generated PDF file to client for download
        return send_file(output_stream, download_name="new_pdf.pdf", as_attachment=True)
    else:
        return 'Error: Please upload a valid PDF file.'



if __name__ == '__main__':
    app.run(debug=True)
