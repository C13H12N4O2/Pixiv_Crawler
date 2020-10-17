import requests
import imageio
import os
import shutil
from zipfile import ZipFile

class Pixiv():
    def __init__(self):
        self.s = requests.Session()
        
        self.headers = {
            'referer': 'https://accounts.pixiv.net',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        
        self.login_info = {}
        self.params = {}
        self.cookies = []
        
        self.pages = {
            'daily': {None: 10, 'illust': 10, 'ugoira': 2, 'manga': 10},
            'daily_r18': {None: 2, 'illust': 2, 'ugoira': 2, 'manga': 2},
            'weekly': {None: 10, 'illust': 10, 'ugoira': 2, 'manga': 10},
            'weekly_r18': {None: 2, 'illust': 2, 'ugoira': 1, 'manga': 2},
            'monthly': {None: 10, 'illust': 5, 'manga': 2},
            'rookie': {None: 6, 'illust': 6, 'manga': 2},
            'original': {None: 6},
            'male': {None: 10},
            'male_r18': {None: 6},
            'female': {None: 10},
            'female_r18': {None: 6},
            'r18g': {None: 1, 'illust': 1}
        }

    def parse_url(self, url, headers=None, data=None, auth=None, cookies=None):
        if not headers:
            headers = self.headers
        return self.s.get(url, headers=headers, data=data, auth=auth, cookies=cookies)

    def get_data_url(self, illust_id=None, user_id=None, illust_type=None, params=None, index=None, detail=False, list=False):
        if illust_id:
            if detail:
                return 'https://www.pixiv.net/touch/ajax/illust/details?illust_id={illust_id}'.format(illust_id=illust_id)
            elif illust_type == '2':
                return 'https://www.pixiv.net/ajax/illust/{illust_id}/ugoira_meta'.format(illust_id=illust_id)
            return 'https://www.pixiv.net/ajax/illust/{illust_id}/pages'.format(illust_id=illust_id)
        if user_id:
            return 'https://www.pixiv.net/ajax/user/{user_id}/profile/all'.format(user_id=user_id)
        url = 'https://www.pixiv.net/ranking.php?'
        if params['mode']:
            url = '{url}mode={mode}'.format(url=url, mode=params['mode'])
        if params['content']:
            url = '{url}&content={content}'.format(url=url, content=params['content'])
        if list:
            urls = []
            if index:
                index = min(index, self.pages[params['mode']][params['content']])
            else:
                index = self.pages[params['mode']][params['content']]
            for i in range(1, index + 1):
                urls.append('{url}&p={index}&format=json'.format(url=url, index=i))
            return urls
        else:
            url = '{url}&p={index}'.format(url=url, index=1)
        return '{url}&format=json'.format(url=url)

    def get_original_img(self, request, illust_type):
        if illust_type != '2':
            urls = []
            for html in request.json()['body']:
                urls.append(html['urls']['original'])
            if len(urls) == 1:
                return urls[0]
            return urls
        return request.json()['body']['originalSrc']
        
    def get_title(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['illust_details']['title'].replace('/', '_')
        return request['title'].replace('/', '_')
        
    def get_user_name(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['author_details']['user_name'].replace('/', '_')
        return request['user_name'].replace('/', '_')
        
    def get_user_profile(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['author_details']['profile_img']['main']
        return request['profile_img']
        
    def get_tag(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['illust_details']['tags']
        return request['tags']
        
    def get_illust_type(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['illust_details']['type']
        return request['illust_type']
        
    def get_rating_count(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['illust_details']['rating_count']
        return html['rating_count']
                
    def get_rating_view(self, request):
        if not isinstance(type(request), str):
            return request.json()['body']['illust_details']['rating_view']
        return html['view_count']
        
    def get_illust_id(self, request, is_user_page=False):
        if not isinstance(type(request), str):
            if is_user_page:
                ids = []
                for section in request.json()['body']:
                    if section == 'novels':
                        break;
                    for illust_id in request.json()['body'][section]:
                        ids.append(illust_id)
                ids.sort(reverse=True, key=lambda id: int(id))
                return ids
            return request.json()['body']['illust_details']['id']
        return request['illust_id']
        
    def get_rank(self, request):
        return request('rank')
        
    def get_yesterday_rank(self, request):
        return request('yes_rank')
    
    def get_illust_page_count(self, request):
        return request('illust_page_count')
                
    def get_date(self, request):
        return request['date']
        
    def get_description(self, request):
        return request.json()['body']['illust_details']['description']
        
    def get_user_account(self, request):
        return request.json()['body']['author_details']['user_account']
        
    def get_bookmark_user(self, request):
        return request.json()['body']['illust_details']['bookmark_user_total']
        
    def get_delay(self, request):
        list = []
        for dict in request.json()['body']['frames']:
            list.append(dict['delay']/1000)
        return list
        
    def get_img_format(self, img):
        return img.split('.')[-1]
        
    def get_img_name(self, img):
        return img.split('.')[0]

    def download_img(self, data, path, file_name):
        if not isinstance(type(data), str):
            data = self.parse_url(data)
        with open(os.path.join(path, file_name), 'wb') as handle:
            handle.writelines(data)
            handle.close()

    def download_ugoira(self, data, path, file_name, delay):
        if not isinstance(type(data), str):
            data = self.parse_url(data)
        zip_file = '{}.zip'.format(file_name)
        gif_file = '{}.gif'.format(file_name)
        new_path = self.mkdir(path, new_folder=file_name)
        with open(os.path.join(new_path, zip_file), 'wb') as handle:
            handle.writelines(data)
            handle.close()
        with ZipFile(os.path.join(new_path, zip_file), 'r') as zip:
            zip.extractall(new_path)
            list = zip.namelist()
        with imageio.get_writer(os.path.join(path, gif_file), mode='I', format='GIF-PIL', duration=delay) as writer:
            for file in list:
                img = imageio.imread(os.path.join(new_path, file))
                writer.append_data(img)
        shutil.rmtree(new_path)
                
    def mkdir(self, path, new_folder=None, params=None):
        if params:
            for key, value in params.items():
                path = os.path.join(path, value)
        if new_folder:
            path = os.path.join(path, new_folder)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
