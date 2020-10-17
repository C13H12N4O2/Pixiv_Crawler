import Pixiv_Crawler

def main():
    pixiv = Pixiv_Crawler.Pixiv()
    id = '14866303'
    
    user_url = pixiv.get_data_url(user_id=id)
    user_req = pixiv.parse_url(user_url)
    
    illust_ids = pixiv.get_illust_id(user_req, True)
    
    for illust_id in illust_ids:
        detail_url = pixiv.get_data_url(illust_id=illust_id, detail=True)
        detail_req = pixiv.parse_url(detail_url)
        
        title = pixiv.get_title(detail_req)
        user_name = pixiv.get_user_name(detail_req)
        illust_type = pixiv.get_illust_type(detail_req)
        
        path = pixiv.mkdir('Pixiv', new_folder=user_name)
        
        data_url = pixiv.get_data_url(illust_id=illust_id)
        data_req = pixiv.parse_url(data_url)
        
        img_urls = pixiv.get_original_img(data_req, illust_type)
        if isinstance(img_urls, str):
            list = []
            list.append(img_urls)
            img_urls = list
    
        index = 0
        for img_url in img_urls:
            if index == 0:
                file_name = '{illust_id} - {title}'.format(illust_id=illust_id, title=title)
            else:
                file_name = '{illust_id} - {title}[{index}]'.format(illust_id=illust_id, title=title, index=index)
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

