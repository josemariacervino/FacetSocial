import requests
from lxml import html
from bs4 import BeautifulSoup
from pymsgbox import prompt as msgPrompt
from pymsgbox import password as msgPassword

class ScrappyDoo():
    def __init__(self,url):
        self.url = url
        self.session = requests.Session()

    def login_GUI(self,login_url,username=None,password=None,username_element="email",password_element="password",enable_csrf=False):
        if username is None:
            username = msgPrompt(text='Enter Username', title='Username')
        if password is None:
            password = msgPassword(text='Enter Password', title='Password',mask='*')
        self.login_page(login_url,username,password,username_element,password_element,enable_csrf)

    def login_page(self,login_url,username,password,username_element="email",password_element="password",enable_csrf=False):
        site = self.session.get(login_url)
        bs_content = BeautifulSoup(site.content, "html.parser")
        if enable_csrf:
            csrf_wrapper = bs_content.find("input", {"name":"csrf_token"})
            token = csrf_wrapper["value"]
            login_data = {username_element:username,password_element:password, "csrf_token":token}
        else:
            login_data = {username_element:username,password_element:password}
        res = self.session.post(login_url,data=login_data)
        #print(res.text)
        self.load_page()
    
    def load_page(self):
        page = self.session.get(self.url)
        #print(page.text)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def find_tables(self,match_headers=None,table_id=None):
        if (table_id is not None):
            results = self.soup.find_all("table",id=table_id)
        else:
            results = self.soup.find_all("table")
        tables = []
        for result in results:
            if (match_headers is not None):
                headers = self.find_table_headers(result)
                headers_matched = True
                if len(headers) == len(match_headers):
                    for h,m_h in zip(match_headers,headers):
                        if h != m_h:
                            headers_matched = False
                            break
                else:
                    headers_matched = False
                if (headers_matched):
                    print("Headers matched in table")
                    tables.append(result)
            else:
                tables.append(result) #if headers are not specified then return all tables from the page
        return tables

    def find_table_headers(self,table):
        table_headers = []
        for tx in table.find_all('th'):
            tx_t = tx.get_text()
            if tx_t != "":
                table_headers.append(tx_t)
        return table_headers