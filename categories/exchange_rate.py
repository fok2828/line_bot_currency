import os, json, re, threading
from categories.bank_crawl import BankCrawl
from collections import deque
from multiprocessing import Pool 

class ExchangeRate():
    def __init__(self, country):
        self.msg = ''
        self.bank_deque = {}
        self.country = country
        self.currency_list = {}
        self.bank_info = self.get_bank_info()
        self.multi_exec(self.bank_info, 5)
        self.compare_currency(country)
        
    def get_bank_info(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        bank_info = []
        with open(os.path.join(current_path, 'bank.json'), 'r') as r:
            info = json.load(r)
            for i in info:
                yield [i['bank_name'], i['bank_link']]
            
    def get_currency(self):
        while len(self.bank_deque) > 0:
            each_bank, each_link = self.bank_deque.popleft()
            bc = BankCrawl(each_bank, each_link, self.country)
            if bc.rs_currency is not None: 
                if each_bank not in self.currency_list:
                    self.currency_list[each_bank] = {}
                
                self.currency_list[each_bank]['sell'] = bc.rs_currency[self.country]['sell']
                self.currency_list[each_bank]['buy'] = bc.rs_currency[self.country]['buy']
            
            
            #msg = self.get_message()
            #self.msg = msg.format(each_bank, country, self.currency_list[each_bank]['sell'], self.currency_list[each_bank]['buy'])
        
    def compare_currency(self, country):
        compare_list, empty_list = {}, []
        sell_price, buy_price = float(99999), float(0)
        bank_list = [i for i in self.currency_list]
        for each_bank in self.currency_list:
            try:
                float(self.currency_list[each_bank]['sell'])
            except:
                empty_list.append(each_bank)
                continue
            
            if float(self.currency_list[each_bank]['sell']) <= sell_price:
                compare_list['bank_sell'] = each_bank
                sell_price = float(self.currency_list[each_bank]['sell'])
            if float(self.currency_list[each_bank]['buy']) >= buy_price:
                compare_list['bank_buy'] = each_bank
                buy_price = float(self.currency_list[each_bank]['buy'])
        
        if compare_list:        
            self.msg = self.get_message().format(
                country = country,
                bank_sell = compare_list['bank_sell'],
                bank_buy = compare_list['bank_buy'],
                sell_price = sell_price,
                buy_price = buy_price,
                bank_list = ','.join(bank_list)
            )
        else:
            self.msg = '無數據可以比較'
    
    def get_message(self):
        msg = '''各銀行 {country} 最低價
{bank_sell}現金匯率最低賣出：{sell_price}
{bank_buy}現金匯率最高買入：{buy_price}

參考銀行：{bank_list}
        '''
        return msg
        
    def multi_exec(self, bank_info, thread_num):
        self.bank_deque = deque(bank_info)
        threads = []

        while thread_num != 0:
            p = threading.Thread(target=self.get_currency,
                                 name='Thread - ' + str(thread_num))
            p.start()
            threads.append(p)
            thread_num = thread_num - 1
        
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    er = ExchangeRate('JPY')
    print(er.msg)
