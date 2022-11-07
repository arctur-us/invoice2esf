from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sys
from invoice import Income
from xml.dom import minidom
import os

def readInvoice(pdf):
    output_string = StringIO()
    with open(pdf, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    content = output_string.getvalue()
    return content

def getRate(date):
    link = "https://www.nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut/report?rates%5B%5D=5&beginDate=" + date + "&endDate=" + date
    soup = BeautifulSoup(requests.get(link).text, "lxml")
    rate = soup.find("table").find_all("td")[-1].get_text()
    return float(rate)

def calcSO(opv, so):
    return 14700 # change formula

def calcVOSMS():
    MZP = 60000
    return int(round(MZP*1.4*0.05,0))

def main():
    if len(sys.argv) < 4:
        print("Example:")
        print("python3 main.py invoice.pdf ОЗП_ОПВ ОЗП_СО")
        print()
        return -1
    root = minidom.Document()
    xml = root.createElement('root')
    root.appendChild(xml)
    productChild = root.createElement('product')
    productChild.setAttribute('name', 'Geeks for Geeks')
    xml.appendChild(productChild)
    xml_str = root.toprettyxml(indent = "\t")
    save_path_file = "test.xml"
    with open(save_path_file, "w") as out_file:
        out_file.write(xml_str)
    file = sys.argv[1]
    data = readInvoice(file)
    i = Income(data)
    i.skim(data)
    rate = getRate( datetime.strftime( i.invoice_date, '%d.%m.%Y' ) )
    print("Invoice:", i.invoice_number, "from", i.invoice_date.strftime('%d.%m.%y'))
    print("Act:", i.contract, "for work completed on", datetime.strftime( i.delivery_date, '%d.%m.%y' ))
    print("Income", i.gross, "USD")
    print("Rate:", rate, "on", datetime.strftime( i.invoice_date, '%d.%m.%y' ))
    i.price = round(rate*i.gross,2)
    IPN = int(round(i.price*0.015,0))
    OZP_OPV = int(sys.argv[2]) # revisit
    OZP_SO = int(sys.argv[3])  # revisit
    SO = int(calcSO(OZP_OPV, OZP_SO))
    SN = int(round(i.price*0.015-SO,0))
    OPV = int(round(OZP_OPV*0.1,0))
    VOSMS = calcVOSMS()
    print("KZT", i.price)
    print("ИПН", IPN)
    print("CH", SN)
    print("ОПВ", OPV)
    print("CO", SO)
    print("ВОСМС", VOSMS)

if __name__ == "__main__":
    main()