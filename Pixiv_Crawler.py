import requests
import imageio
import os
from bs4 import BeautifulSoup as bs

class Pixiv():
    def __init__(self):
        self.s = requests.Session()
        self.base_url = 'https://accounts.pixiv.net/login'
        self.main_url = 'https://www.pixiv.net'
        self.artworks_url = 'https://www.pixiv.net/artworks/'
        
        self.headers = {
            'referer': 'https://accounts.pixiv.net',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        
        self.login_info = {}
        self.params = {}
        self.cookies = []
        
        self.modes = ['daily', 'weekly', 'monthly', 'rookie', 'original', 'male', 'female', 'daily_r18', 'weekly_r18', 'male_r18', 'female_r18', 'r18g']
        self.contents = ['illust', 'ugoira', 'manga']
        
    def set_login_info(self, pixiv_id, password):
        self.login_info['pixiv_id'] = pixiv_id
        self.login_info['password'] = password
        
    def set_cookies(self):
        self.cookies = self.s.cookies.get_dict()
        
    def get_cur_headers(self):
        return self.s.headers
       
    def set_params(self, mode = None, content = None):
        try:
            self.params['mode'] = self.modes[self.modes.index(mode)]
        except:
            self.set_default('mode', self.modes)
            
        try:
            self.params['content'] = self.contents[self.contents.index(content)]
        except IndexError:
            pass
        except ValueError:
            self.set_default('content', self.contents)
            
        return self.params
        
    def set_default(self, condition, list):
        print('Your input is not valid or is empty')
        print('Set as default')
        self.params[condition] = list[0]
        
    def parse_url(self, url):
        return self.s.get(url, headers=self.headers, params=self.params)
        
    def get_today(self, req):
        return bs(req.text, 'html.parser').find_all('a', {'class': 'current'})[2].text
            
    def get_artwork_html(self, req):
        return bs(req.text, 'html.parser').find('div', {'class': 'ranking-items-container'}).find_all('section')
        
    def get_attribute(self, html):
        return html['data-attr']
        
    def get_date(self, html):
        return html['data-date']
        
    def get_artwork_id(self, html):
        return html['data-id']
            
    def get_rank(self, html, is_text=False):
        if is_text:
            return html['data-rank-text']
        return html['data-rank']
          
    def get_title(self, html):
        return html['data-title']
            
    def get_user_name(self, html):
        return html['data-user-name']
            
    def get_type(self, html):
        return html.find('img')['data-type']
                
    def get_page_count(self, html):
        try:
            return int(html.find('div', {'class': 'page-count'}).text)
        except:
            return 1
    
    def get_file_name(self, html, index, format):
        if index == 0:
            file_name = '#{rank} - {title} by {user_name}.{format}'.format(rank=self.get_rank(html), title=self.get_title(html), user_name=self.get_user_name(html), format=format)
        else:
            file_name = '#{} - {} by {}[{}].{}'.format(self.get_rank(html), self.get_title(html), self.get_user_name(html), index, format)
        return file_name.replace('/', '-')
    
    def get_format(self, url):
        return url.split('.')[-1]
    
    def get_artwork_url(self, data_id):
        return '{url}{id}'.format(url=self.artworks_url, id=data_id)
    
    def get_original_url(self, url):
        return bs(self.parse_url(url).text, 'html.parser').find_all('meta')[-1]['content'].split(',')[17].split('"')[3]
            
    def next_page(self, url, index):
        page_num = url.split('.')
        page = page_num[-2].split('_')
        page[-1] = page[-1].replace(str(index - 1), str(index))
        page_num[-2] = '_'.join(page)
        return '.'.join(page_num)
            
    def is_connect(self, req):
        return req.status_code == 200
        
    def download_img(self, url, file_name, path):
        with open('{path}/{file_name}'.format(path=path, file_name=file_name), 'wb') as handle:
                print(file_name)
                handle.writelines(self.parse_url(url))
                handle.close()
                
    def download_ugoira(self, url, file_name, path, html):
        gif_name = os.path.join(path, '{}.{}'.format(file_name.split('.')[0], 'gif'))
        with imageio.get_writer(gif_name, mode='I', format='GIF-PIL', fps=18) as writer:
        
            index = 0
            while True:
                req = self.parse_url(self.next_page(url, index))
                if self.is_connect(req) == False:
                    break;
                self.download_img(url, file_name, path)
                img = imageio.imread(os.path.join(path, file_name))
                writer.append_data(img)
                self.delete_img(file_name, path)
                index += 1
                url = self.next_page(url, index)
                file_name = self.get_file_name(html, index, file_name.split('.')[-1])
        print(gif_name)

    def delete_img(self, file_name, path):
        os.remove(os.path.join(path, file_name))

    def mkdir(self, path):
        if os.path.exists(path):
            print('The folder already exists')
        else:
           os.makedirs(path)
