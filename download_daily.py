import Pixiv_Crawler

def main():
    pixiv = Pixiv_Crawler.Pixiv()
    
    params = {
        'mode': 'daily',
        'content': None
    }
    
    ranking_urls = pixiv.get_data_url(params=params, list=True)
    for ranking_url in ranking_urls:
        req = pixiv.parse_url(ranking_url)
        date = pixiv.get_date(req.json())
        path = pixiv.mkdir('Pixiv', new_folder=date, params=params)
        
        for ranking_data in req.json()['contents']:
            illust_id = pixiv.get_illust_id(ranking_data)
            rank = pixiv.get_rank(ranking_data)
            illust_type = pixiv.get_illust_type(ranking_data)
            title = pixiv.get_title(ranking_data)
            user_name = pixiv.get_user_name(ranking_data)
            
            data_url = pixiv.get_data_url(illust_id, illust_type=illust_type)
            data_req = pixiv.parse_url(data_url)
            
            img_urls = pixiv.get_original_img(data_req, illust_type)
            if isinstance(img_urls, str):
                list = []
                list.append(img_urls)
                img_urls = list
            
            index = 0
            for img_url in img_urls:
                if index == 0:
                    file_name = '#{rank} - {title} by {user_name}'.format(rank=rank, title=title, user_name=user_name)
                else:
                    file_name = '#{rank} - {title}[{index}] by {user_name}'.format(rank=rank, title=title, index=index, user_name=user_name)
                print(file_name)
                print()
                if pixiv.is_ugoira(illust_type):
                    delay = pixiv.get_delay(data_req)
                    pixiv.download_ugoira(img_url, path, file_name, delay)
                else:
                    pixiv.download_img(img_url, path, file_name)
                index += 1

if __name__ == '__main__':
    main()
