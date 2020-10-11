import requests
import os
import sys
from bs4 import BeautifulSoup as bs

class Pixiv():
    def __init__(self):
        self.s = requests.Session()
        self.base_url = 'https://accounts.pixiv.net/login'
        self.main_url = 'https://www.pixiv.net'
        self.setting_url = 'https://www.pixiv.net/setting_profile.php'
        self.artworks_url = 'https://www.pixiv.net/artworks/'
        self.ranking_url = 'https://www.pixiv.net/ranking.php?'
        
        self.headers = {
            'referer': 'https://accounts.pixiv.net',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'connection': 'keep-alive'
        }
        
        self.params = {
            'mode': 'daily',
            'content': 'illust'
        }
        
        self.login_info = {}
        self.pixiv_id = 'pixiv_id'
        self.password = 'pixiv_pw'
        self.post_key = []
        self.return_to = 'http://www.pixiv.net'
        self.cookies = []
        self.current_path = './Pixiv/'
        
    def login(self):
        self.get_info()
        post_key_html = self.s.get(self.base_url, data = self.login_info, headers = self.headers).text
        post_key_soup = bs(post_key_html, 'html.parser')
        self.post_key = post_key_soup.find('input', {'name': 'post_key'})
        self.login_info = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'post_key': self.post_key['value'],
            'return_to': self.return_to
        }
        login_req = self.s.post(self.base_url, data = self.login_info, headers = self.headers)
        self.cookies = self.s.cookies.get_dict()
        self.headers = {**self.headers, **self.cookies}
        print(login_req.status_code)
        
    def get_info(self):
        while True:
            try:
                self.pixiv_id = sys.argv[1]
                self.password = sys.argv[2]
                break;
            except:
                print('Enter your pixiv ID and password')
                sys.exit(0)
    
    def get_artwork_url(self):
        ranking_html = self.s.get(self.ranking_url, data = self.login_info, headers = self.headers, params = self.params).text
        ranking_data = bs(ranking_html, 'html.parser').find('div', {'class': 'ranking-items-container'}).find_all('section')
        today_data = bs(ranking_html, 'html.parser').find_all('a', {'class': 'current'})
        
        for html in today_data:
            if html['href'].find('date', 4) != -1:
                today = html['href'].split('=')[-1]
        self.concat_path(today)
        self.mkdir()
        
        for itr in ranking_data:
            print('{rank}: {title} by {name}[{id}]'.format(rank = itr['data-rank'], title  = itr['data-title'], name = itr['data-user-name'], id = itr['data-id']))
            self.get_img_url(itr['data-rank'], itr['data-title'], itr['data-user-name'], itr['data-id'])
            print()
            
    def get_img_url(self, data_rank, data_title, user_name, data_id):
        target_html = self.s.get(self.artworks_url + data_id, headers = self.headers).text
        target_soup = bs(target_html, 'html.parser').find_all('meta')
        target_content = target_soup[-1]['content']
        target_content = target_content.split(',')
                
        target_url = ''
        for html in target_content:
            if html.find('"original"') != -1:
                target_url = max(target_url, html, key = len)
        target_url = max(target_url.split('"'), key = len)
        
        index = 0
        img_url = target_url
        while (True):
            img_url = target_url.split('.')
            img_format = img_url[-1]
            if index != 0:
                img_page = img_url[-2].split('_')
                img_page[-1] = img_page[-1].replace('0', '{index}'.format(index = index))
                img_url[-2] = '_'.join(img_page)
            img_url = '.'.join(img_url)
                
            img_data = self.s.get(img_url, headers = self.headers)
            if img_data.status_code != 200:
                break;
            
            if index == 0:
                file_name = '#{rank} - {title} by {name}.{format}'.format(rank = data_rank, title = data_title, name = user_name, format = img_format)
            else:
                file_name = '#{rank} - {title}[{index}] by {name}.{format}'.format(rank = data_rank, title = data_title, index = index, name = user_name, format = img_format)
            self.download_img(img_data, file_name)
            print(file_name)
                
            index += 1
        
    def download_img(self, img_data, file_name):
        try:
            with open(os.path.join(self.current_path, file_name), 'wb') as handle:
                handle.writelines(img_data)
                handle.close()
        except FileNotFoundError:
            print('File name [{file_name}] is too long!'.format(file_name = file_name))
            print('Download failed')
        
    def mkdir(self):
        has_path = os.path.exists(self.current_path)
        
        if has_path:
            print('The folder already exists')
        else:
           os.makedirs(self.current_path)
           
    def concat_path(self, today):
        list = []
        for itr in self.current_path:
            list.append(itr)
        list.append('/')
        for itr in today:
            list.append(itr)
        for itr in self.params:
            list.append('/')
            list.append(self.params[itr])
        list.append('/')
        self.current_path = ''.join(list)
        
if __name__ == '__main__':
    pixiv = Pixiv()
    pixiv.login()
    pixiv.get_artwork_url()
