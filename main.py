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
  app.run(host='0.0.0.0', port=5000)

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=80)
#https://ask.replit.com/t/flask-app-not-loading-except-when-deployed/58186/13