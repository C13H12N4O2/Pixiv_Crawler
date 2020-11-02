import Pixiv_Crawler

def on_PC(illust_id):
    pixiv = Pixiv_Crawler.Pixiv()
    res = pixiv.illust_detail(illust_id, is_pc=True)
    details = res['body']['illust_details']
    html = pixiv.illust_pages(illust_id)['body']
    for data in html:
        url = data['urls']['original']
        pixiv.download(url)
        
def on_APP(illust_id):
    pixiv = Pixiv_Crawler.Pixiv()
    pixiv.login('pixiv_id', 'password')
    res = pixiv.illust_detail(illust_id)
    
    try:
        details = res['illust']
    except:
        details = res['illusts']
    
    try:
        urls = details['meta_single_page']['original_image_url']
        pixiv.download(urls)
    except:
        html = details['meta_pages']
        for data in html:
            url = data['image_urls']['original']
            pixiv.download(url)

def main():
    illust_id = '84278666'      # illust
    #illust_id = '66808665'     # manga
    
    on_PC(illust_id)
    #on_APP(illust_id)

if __name__ == '__main__':
    main()

