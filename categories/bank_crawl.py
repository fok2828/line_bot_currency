from webconnector import webconnector 
# pip3 install BeautifulSoup4
from bs4 import BeautifulSoup

class BankCrawl():
    def __init__(self, bank_name, bank_link, country):
        self.bank_name, self.bank_link, self.country = bank_name, bank_link, country
        driver = webconnector.WebConnector()
        driver.driver.get(bank_link)
        page_source = (driver.driver.page_source).encode('utf-8')
        rs = BeautifulSoup(page_source, "html.parser")
        self.rs_currency = self.get_currency_price(rs)
        driver.driver.close()
    
    def get_currency_price(self, rs):
        currency_info = {}
        if self.bank_name == '台灣銀行':
            currency_info = self.get_bot_currency(rs)
            
        elif self.bank_name == '台新銀行':
            currency_info = self.get_tsb_currency(rs)

        elif self.bank_name == '玉山銀行':
            currency_info = self.get_esun_currency(rs)

        elif self.bank_name == '中國信託':
            currency_info = self.get_ctbc_currency(rs)
            
        elif self.bank_name == '國泰世華':
            currency_info = self.get_cathay_currency(rs)
            
        return currency_info

    def get_bot_currency(self, rs):
        currency_info = {}
        currency_tb_list = rs.find('table', class_="table table-striped table-bordered table-condensed table-hover").find_all('tr')
        for each_tr in currency_tb_list:
            country = each_tr.find('div', {"class":"visible-phone print_hide"})
            if country:
                country = country.text.strip()
                if self.country in country:
                    currency_info[self.country]={}
                    currency_info[self.country]['sell'] = each_tr.find('td', {"data-table":"本行現金賣出"}).text.strip()
                    currency_info[self.country]['buy'] = each_tr.find('td', {"data-table":"本行現金買入"}).text.strip()
                    break
                    
        return currency_info
        
    def get_tsb_currency(self, rs):
        currency_info = {}
        country = ''
        currency_tb_list = rs.find('table', class_="table01").find_all('tr')
        for each_tr in currency_tb_list:
            count = 0
            if currency_info:
                break
            
            for each_td in each_tr.find_all('td'):
                if count == 0 and self.country in each_td.text.strip():
                    country = each_td.text.strip()
                    currency_info[self.country]={}
                if self.country in currency_info:
                    if count == 3:
                        currency_info[self.country]['buy'] = each_td.text.strip()
                    if count == 4:
                        currency_info[self.country]['sell'] = each_td.text.strip()
                count += 1
                
        return currency_info
        
    def get_esun_currency(self, rs):
        currency_info = {}
        currency_tb_list = rs.find('table', {'id' : 'CashBoardRate'}).find_all('tr')
        for each_tr in currency_tb_list:
            if currency_info:
                break
            
            count = 0
            for each_td in each_tr.find_all('td'):
                if count == 1:
                    currency_info[self.country]['buy'] = each_td.text
                    count += 1
                if count == 2:
                    currency_info[self.country]['sell'] = each_td.text
                    
                if each_td.find('a'):
                    if self.country not in each_td.find('a').text:
                        break
                    else:
                        currency_info[self.country] = {}
                        count += 1
       
        return currency_info
        
    def get_ctbc_currency(self, rs):
        currency_info = {}
        currency_tb_list = rs.find('table', {'id' : 'mainTable'}).find_all('tr')
        for each_tr in currency_tb_list:
            if currency_info:
                break
            
            for i, each_td in enumerate(each_tr.find_all('td')):
                if i == 0:
                    if self.country not in each_td.text.rstrip():
                        break
                    else:
                        currency_info[self.country] = {}
                        continue
                if i == 1:
                    currency_info[self.country]['buy'] = each_td.text
                if i == 2:
                    currency_info[self.country]['sell'] = each_td.text

        return currency_info
                         
    def get_cathay_currency(self, rs):
        currency_info = {}
        currency_tb_list = rs.find('table', {'class' : 'table-rate text-left'}).find_all('tr')
        for each_tr in currency_tb_list:
            if currency_info:
                break
            
            for i, each_td in enumerate(each_tr.find_all('td')):
                if i == 0:
                    if self.country not in each_td.text.rstrip() or 'Cash' not in each_td.text.rstrip():
                        break
                    else:
                        currency_info[self.country] = {}
                        continue
                if i == 1:
                    currency_info[self.country]['buy'] = each_td.text
                if i == 2:
                    currency_info[self.country]['sell'] = each_td.text

        return currency_info
        
        
        