import Pixiv_Crawler

def main():
    pixiv = Pixiv_Crawler.Pixiv()
    id = '84930667'
    
    detail_url = pixiv.get_data_url(illust_id=id, detail=True)
    detail_req = pixiv.parse_url(detail_url)
    
    title = pixiv.get_title(detail_req)
    illust_type = pixiv.get_illust_type(detail_req)
    
    data_url = pixiv.get_data_url(illust_id=id, illust_type=illust_type)
    data_req = pixiv.parse_url(data_url)
    
    img = pixiv.get_original_img(data_req, illust_type)
    ugoira_delay = pixiv.get_delay(data_req)
    
    path = pixiv.mkdir('Pixiv')
    pixiv.download_ugoira(img, path, title, ugoira_delay)

if __name__ == '__main__':
    main()
