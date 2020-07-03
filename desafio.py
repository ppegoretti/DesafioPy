import datetime
import json
from fpdf import FPDF
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


with open('input.json') as f:
  input_Json = json.load(f)

def px_mm(value):
    return value * ( 25.4 / 96 )

#variables
pageFormat = (px_mm(375), px_mm(1127.55))
logo = "files/Logo.png"

class PDF(FPDF):
    def header(self):
        #self.image('Logo.png', 159, 36, 57, 52.25)
        self.image('Logo.png', px_mm(150), px_mm(34), px_mm(65), px_mm(59.60))
        self.ln(px_mm(103))
        self.set_font('arial', 'B', 14)
        self.cell(0, 0, 'Comprovante de Transferência', 0, 1, 'C', False)
        self.ln(px_mm(20))
        self.set_text_color(199, 199, 199)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 0, input_Json['timestamp'], 0, 1, 'C', False)
        pdf.set_left_margin(px_mm(16))
        self.ln(px_mm(40))
    def insert_title(self, label):
        self.ln(px_mm(10))
        self.set_text_color(43, 43, 43)
        self.set_font('Arial', "", 15)
        self.cell(px_mm(16), 0, label, 0, 1, 'L', False)
        self.ln(px_mm(10))
        self.line(px_mm(16), self.get_y(), px_mm(359), self.get_y())
        self.ln(px_mm(35))
    def insert_subtitle(self, label, value):
        self.set_text_color(189, 189, 189)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 0, label, 0, 1, 'L', False)
        self.ln(px_mm(20))
        self.set_text_color(43, 43, 43)
        self.set_font('Arial', "", 12)
        self.cell(0, 0, value, 0, 1, 'L', False)
        self.ln(px_mm(30))
    def footer(self):
        self.ln(px_mm(0))
        self.line(px_mm(16), self.get_y(), px_mm(359), self.get_y())
        self.ln(px_mm(20))
        self.set_text_color(43, 43, 43)
        self.set_font('arial', 'B', 10)
        self.cell(0, 0, 'Código de autenticação', 0, 1, 'C', False)
        self.ln(px_mm(20))
        self.set_text_color(196, 196, 196)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 0, input_Json['transactionId'], 0, 1, 'C', False)
        self.ln(px_mm(20))
        self.set_text_color(43, 43, 43)
        self.set_font('arial', 'B', 10)
        self.cell(0, 0, input_Json['from']['account']['name'], 0, 1, 'C', False)
        self.ln(px_mm(20))
        self.set_text_color(196, 196, 196)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 0, "CNPJ: 19.581.142/0001-18", 0, 1, 'C', False)


pdf = PDF('P', 'mm', pageFormat)
pdf.add_page()
pdf.insert_subtitle("VALOR TOTAL", "R$ " + input_Json['amount'])
pdf.insert_subtitle("TIPO DE TRANSFERÊNCIA",  input_Json['type'].upper())
pdf.ln(px_mm(14))
pdf.insert_title('Origem')
pdf.insert_subtitle("NOME", input_Json['from']['account']['name'])
pdf.insert_subtitle("BANCO", input_Json['from']['account']['institutionName'])
pdf.insert_subtitle("AGÊNCIA", input_Json['from']['account']['branch'])
pdf.insert_subtitle("CONTA", input_Json['from']['account']['number'])
pdf.insert_subtitle("EM NOME DE", input_Json['from']['entity']['fullName'])
pdf.insert_subtitle("CONTA ATAR PAY", input_Json['from']['entity']['atarId'])
pdf.insert_subtitle(input_Json['from']['entity']['documentType'], input_Json['from']['entity']['document'])
pdf.ln(px_mm(14))
pdf.insert_title('Destino')
pdf.insert_subtitle("NOME", input_Json['to']['entity']['fullName'])
pdf.insert_subtitle("BANCO", input_Json['to']['account']['institutionName'])
pdf.insert_subtitle("AGÊNCIA", input_Json['to']['account']['branch'])
pdf.insert_subtitle("CONTA", input_Json['to']['account']['number'])
pdf.ln(px_mm(14))
pdf.output("files\\" + input_Json['transactionId'] + '.pdf')


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file_path = "files/" + input_Json['transactionId'] + ".pdf"
file = drive.CreateFile()
file.SetContentFile(file_path)
file.Upload() # Upload the file.
print('title: %s, mimeType: %s' % (file['title'], file['mimeType']))