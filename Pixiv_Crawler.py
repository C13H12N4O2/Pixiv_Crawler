import requests
import imageio
import os, sys
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
            'referer': 'https://accounts.pixiv.net/login',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'connection': 'keep-alive'
        }
        
        self.login_info = {}
        self.params = {}
        self.cookies = []
        self.current_path = './Pixiv/'
        
    def login(self):
        self.get_info()
        post_key_html = self.s.get(self.base_url, data = self.login_info, headers = self.headers).text
        post_key_soup = bs(post_key_html, 'html.parser')
        self.login_info['post_key'] = post_key_soup.find('input', {'name': 'post_key'})['value']
        self.login_info['return_to'] = self.main_url
        login_req = self.s.post(self.base_url, data = self.login_info, headers = self.headers)
        self.cookies = self.s.cookies.get_dict()
        self.headers = {**self.headers, **self.cookies}
    
    def get_info(self):
        modes = ['daily', 'weekly', 'monthly', 'rookie', 'original', 'male', 'female', 'daily_r18', 'weekly_r18', 'male_r18', 'female_r18', 'r18g']
        contents = ['illust', 'ugoira', 'manga']
        
        try:
            self.login_info['pixiv_id'] = sys.argv[1];
            self.login_info['password'] = sys.argv[2];
        except:
            print('Enter your pixiv ID and password')
            sys.exit(0)
        
        try:
            self.params['mode'] = modes[modes.index(sys.argv[3])]
        except:
            self.set_default('mode', modes)
            
        try:
            self.params['content'] = contents[contents.index(sys.argv[4])]
        except IndexError:
            pass
        except ValueError:
            self.set_default('content', contents)
    
    def set_default(self, condition, list):
        print('Your input is not valid or is empty')
        print('Set as default')
        self.params[condition] = list[0]
    
    def get_artwork_url(self):
        ranking_html = self.s.get(self.ranking_url, data = self.login_info, headers = self.headers, params = self.params, cookies = self.cookies).text
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
                
        target_url = self.get_orig_img(target_content)
        
        index = 0
        while True:
            img_url = self.next_page(target_url, index)
            img_format = self.get_img_format(target_url)
                
            img_data = self.s.get(img_url, headers = self.headers)
            if img_data.status_code != 200:
                break;
            
            file_name = self.make_file_name(data_rank, data_title, index, user_name, img_format)
            print(file_name)
            if not self.download_img(img_data, file_name):
                break;
            
            index += 1
        
        if len(self.params) == 2 and self.params['content'] == 'ugoira':
            self.download_ugoira(data_rank, data_title, index, user_name, img_format)
        
    def download_img(self, img_data, file_name):
        path = os.path.join(self.current_path, file_name)
        if not os.path.exists(path):
            try:
                with open(path, 'wb') as handle:
                    handle.writelines(img_data)
                    handle.close()
            except FileNotFoundError:
                print('File name [{file_name}] is too long!'.format(file_name = file_name))
                print('Download failed')
                return False
        else:
            print('The file already exists')
        return True
            
    def download_ugoira(self, data_rank, data_title, index, user_name, img_format):
        gif_name = self.make_file_name(data_rank, data_title, 0, user_name, 'gif')
        print(gif_name)
        try:
            path = os.path.join(self.current_path, gif_name)
            with imageio.get_writer(path, mode = 'I', format = 'GIF-PIL', fps = 24 / 60 * index) as writer:
                for i in range(0, index):
                    file_name = self.make_file_name(data_rank, data_title, i, user_name, img_format)
                    img = imageio.imread(os.path.join(self.current_path, file_name))
                    writer.append_data(img)
                    os.remove(os.path.join(self.current_path, file_name))
        except FileNotFoundError:
            print('File name [{name}] is too long!'.format(name = gif_name))
            print('Download failed')
            
    def get_orig_img(self, target_content):
        target_url = ''
        for html in target_content:
            if html.find('"original"') != -1:
                target_url = max(target_url, html, key = len)
        target_url = max(target_url.split('"'), key = len)
        return target_url
            
    def make_file_name(self, data_rank, data_title, index, user_name, img_format):
        if index == 0:
            file_name = '#{rank} - {title} by {name}.{format}'.format(rank = data_rank, title = data_title, name = user_name, format = img_format)
        else:
            file_name = '#{rank} - {title}[{index}] by {name}.{format}'.format(rank = data_rank, title = data_title, index = index, name = user_name, format = img_format)
        return file_name
        
    def next_page(self, target_url, index):
        img_url = target_url.split('.')
        if index != 0:
            img_page = img_url[-2].split('_')
            img_page[-1] = img_page[-1].replace('0', '{index}'.format(index = index))
            img_url[-2] = '_'.join(img_page)
        img_url = '.'.join(img_url)
        return img_url
        
    def get_img_format(self, target_url):
        img_format = target_url.split('.')
        img_format = img_format[-1]
        return img_format
        
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
