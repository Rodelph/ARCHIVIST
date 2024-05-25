import os
import sys
import pdfkit
import base64
import qrcode
import fitz  # PyMuPDF
import webbrowser
from jsonio import update_data, create_data
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QMessageBox, QFileDialog)

if sys.platform == "win32":
    PATH_TO_WKHTMLTOPDF = r'./wkhtmltopdf/bin/wkhtmltopdf.exe'
elif sys.platform in ["linux", "linux2"]:
    PATH_TO_WKHTMLTOPDF = r'./wkhtmltopdf/wkhtmltopdf'
elif sys.platform in ["darwin", "os2", "os2emx"]:
    PATH_TO_WKHTMLTOPDF = r'./wkhtmltopdf/wkhtmltopdf-mcos'

CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_TO_WKHTMLTOPDF)
OPT = {
    'margin-top': '2in',
    'margin-bottom': '1in',
    'margin-left': '1in',
    'margin-right': '1in',
    'page-size': 'Letter'
}
TEMP_PDF_PATH = "./PDF/temp.pdf"
FINAL_PDF_PATH = "./PDF/output.pdf"
BIN_ID = create_data()
QR_FOLDER_PATH = "./QR"
UID_FOLDER_PATH = os.path.join(QR_FOLDER_PATH, BIN_ID)
OUTPUT_FOLDER_PATH = "./PDF"
AR_MARKER_PATH = './_ARMarker/Markers/MarkerIcons03.png'

# Ensure directories exist
os.makedirs(UID_FOLDER_PATH, exist_ok=True)
os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

def count_pdf_pages(temp_pdf_path):
    with open(temp_pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        return len(pdf_reader.pages)

def generate_qr_codes(num_pages):
    for p_no in range(num_pages):
        text = f'{{"id": "{BIN_ID}", "page": {p_no}}}'
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(os.path.join(UID_FOLDER_PATH, f"{p_no}.png"))

def add_qr_codes_to_pdf(num_pages, temp_pdf_path, final_pdf_path):
    pdf_reader = PdfReader(temp_pdf_path)
    pdf_writer = PdfWriter()

    a, b = 200, 660
    wid, hei = 120, 120

    with open(AR_MARKER_PATH, 'rb') as marker_file:
        marker_data = marker_file.read()
        marker_base64 = base64.b64encode(marker_data).decode('utf-8')

    for i in range(num_pages):
        page = pdf_reader.pages[i]
        qr_path = os.path.join(UID_FOLDER_PATH, f"{i}.png")
        
        with open(qr_path, 'rb') as qr_file:
            qr_data = qr_file.read()
            qr_base64 = base64.b64encode(qr_data).decode('utf-8')

        image_pdf_path = 'image_page.pdf'
        c = canvas.Canvas(image_pdf_path, pagesize=letter)
        c.drawImage(f"data:image/png;base64,{marker_base64}", a, b, width=wid, height=hei)
        c.drawImage(f"data:image/png;base64,{qr_base64}", a + wid + 5, b, width=wid, height=hei)
        c.save()

        with open(image_pdf_path, 'rb') as image_pdf_file:
            image_pdf_reader = PdfReader(image_pdf_file)
            image_page = image_pdf_reader.pages[0]
            page.merge_page(image_page)
            pdf_writer.add_page(page)

        os.remove(image_pdf_path)
        
    with open(final_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def process_pdf_metadata(pdf_path, url):
    doc = fitz.open(pdf_path)
    a, b = 200, 660
    wid, hei = 120, 120
    json_data = {
        'URL': url,
        'ar_marker_coordinates': [a, (792 - (b + hei)), (a + wid), (792 - b)],
        'pages': []
    }
    
    total_pages = doc.page_count
    item_count = 0
    
    hyperlink_id = BIN_ID
    for page_idx in range(total_pages):
        cur_page = doc.load_page(page_idx)
        links = cur_page.get_links()
        hyperlinks = []

        for item in links:
            x0, y0, x1, y1 = item['from']
            coordinates = [round(coord, 5) for coord in [x0, y0, x1, y1]]
            uri = item.get('uri', '')
            hyperlink = {'id': f"{hyperlink_id}-{item_count}", 'uri': uri, 'coordinates': coordinates}
            hyperlinks.append(hyperlink)
            item_count += 1

        json_data['pages'].append({"hyperlinks": hyperlinks})

    update_data(bin_id=BIN_ID, json_data=json_data)
    doc.close()

def making_pdf_qr(path):
    pdfkit.from_url(path, output_path=TEMP_PDF_PATH, configuration=CONFIG, options=OPT, verbose=False)
    num_pages = count_pdf_pages(TEMP_PDF_PATH)
    generate_qr_codes(num_pages)
    add_qr_codes_to_pdf(num_pages, TEMP_PDF_PATH, FINAL_PDF_PATH)
    os.remove(TEMP_PDF_PATH)
    process_pdf_metadata(FINAL_PDF_PATH, path)
    webbrowser.open(FINAL_PDF_PATH)  # Open the final PDF file

def process_pdf_file(file_path):
    num_pages = count_pdf_pages(file_path)
    generate_qr_codes(num_pages)
    add_qr_codes_to_pdf(num_pages, file_path, FINAL_PDF_PATH)
    process_pdf_metadata(FINAL_PDF_PATH, file_path)
    webbrowser.open(FINAL_PDF_PATH)  # Open the final PDF file

class PDFGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Generator with QR Codes')
        self.layout = QVBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter URL')
        self.layout.addWidget(self.url_input)
        self.browse_button = QPushButton('Browse PDF', self)
        self.browse_button.clicked.connect(self.browse_pdf)
        self.layout.addWidget(self.browse_button)
        self.generate_button = QPushButton('Generate PDF from URL', self)
        self.generate_button.clicked.connect(self.generate_pdf_from_url)
        self.layout.addWidget(self.generate_button)
        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

    def browse_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_path:
            self.status_label.setText('Processing File...')
            try:
                process_pdf_file(file_path)
                self.status_label.setText('File processed successfully!')
                QMessageBox.information(self, 'Success', 'File processed successfully!', QMessageBox.Ok)
            except Exception as e:
                self.status_label.setText('Error processing the file.')
                QMessageBox.critical(self, 'Error', f'Error processing the file: {e}', QMessageBox.Ok)

    def generate_pdf_from_url(self):
        url = self.url_input.text()
        if url:
            self.status_label.setText('Generating PDF...')
            try:
                making_pdf_qr(url)
                self.status_label.setText('PDF generated successfully!')
                QMessageBox.information(self, 'Success', 'PDF generated successfully!', QMessageBox.Ok)
            except Exception as e:
                self.status_label.setText('Error generating PDF.')
                QMessageBox.critical(self, 'Error', f'Error generating PDF: {e}', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid URL.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFGeneratorApp()
    ex.show()
    sys.exit(app.exec_())
