import re
from datetime import datetime

class Income(object):
    def __init__(self, data):
        pass
    
    invoice_date = "" # done
    reference = ""
    my_name = ""
    turnover_date = ""
    employer_address = ""
    employer_country = ""
    employer_name = ""
    my_address = ""
    my_business = ""
    my_tin = ""
    delivery_date = "" # done
    invoice_number = "" # done
    contract_date = ""
    contract = "" # done
    term = 'безналичный расчет' # done
    yes = "true" # done
    transport_code = 99 # done
    currency = "KZT" # done
    catalogue = 1 # done
    product_description = "Разработка программного обеспечения" # done
    price = ""
    origin_code = 6 # done
    nomenclature = 5114 # done
    zero = 0 # done
    bank = ''
    bik = ""
    iik = ""
    no = "false" # done
    kbe = ""
    employer_status = "EXPORTER" # done
    gross = 0 # done

    def getInvoice(self, data):
        reg = 'Number:\ [\r\n]+([^\r\n]+)'
        matches = re.findall(reg, data)
        invoice = matches[-1].replace(" ","")
        return invoice

    def getIncome(self, data):
        reg = '(?s)составляет (.*) USD'
        matches = re.findall(reg, data)
        usd = float(matches[-1].replace(" ","").replace(",","."))
        return usd

    def getiDate(self, data):
        reg = '(.+)\n(Agreement #)'
        matches = re.findall(reg, data)
        date = matches[-1]
        mydate =  date[0].replace(" ","")
        return datetime.strptime(mydate, '%d-%b-%y')
    
    def getAct(self, data):
        reg = '(?s)Agreement #(.*) \nfrom'
        matches = re.findall(reg, data)
        agreement = matches[-1]
        return agreement
        
    def getaDate(self, data):
        reg = '\(services\)  (.*) '
        matches = re.findall(reg, data)
        date = matches[-1]
        return datetime.strptime(date, '%m/%d/%Y')
    
    def getTIN(self, data):
        reg = '(?<=номер )(.[0-9]+)'
        matches = re.findall(reg, data)
        reg = matches[-1].replace(" ","")
        return reg

    def skim(self, data):
        self.invoice_number = self.getInvoice(data)
        self.gross = self.getIncome(data)
        self.invoice_date = self.getiDate(data)
        self.contract = self.getAct(data)
        self.delivery_date = self.getaDate(data)
        self.reference = ""
        self.my_name = ""
        self.turnover_date = ""
        self.employer_address = ""
        self.employer_country = ""
        self.employer_name = ""
        self.my_address = ""
        self.my_business = ""
        self.my_tin = self.getTIN(data)
        self.price = ""
        self.bank = ''
        self.bik = ""
        self.iik = ""
        self.kbe = ""