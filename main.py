import Pixiv_Crawler
import sys

def make_path(today, mode, content='general'):
    if mode == 'weekly' or mode == 'monthly':
        return './Pixiv/{}/{}/'.format(today, content)
    else:
        return './Pixiv/{}/{}/{}/'.format(today, mode, content)

if __name__ == '__main__':
    pixiv = Pixiv_Crawler.Pixiv()
    params = pixiv.set_params('weekly', 'ugoira')
    
    url = 'https://www.pixiv.net/ranking.php?'
    req = pixiv.parse_url(url)
    print(req)
    print(pixiv.get_today(req))
    path = make_path(pixiv.get_today(req), params['mode'], params['content'])
    print(path)
    pixiv.mkdir(path)
    '''
    res = pixiv.get_artwork_html(req)
    for html in res:
        artwork_id = pixiv.get_artwork_id(html)
        img_cnt = pixiv.get_page_count(html)
        artwork_url = pixiv.get_artwork_url(artwork_id)
        original_url = pixiv.get_original_url(artwork_url)
        img_format = pixiv.get_format(original_url)
        
        for i in range(0, img_cnt):
            original_url = pixiv.next_page(original_url, i)
            file_name = pixiv.get_file_name(html, i, img_format)
            pixiv.download_img(original_url, file_name, path, html)
    '''
    
    res = pixiv.get_artwork_html(req)
    for html in res:
        artwork_id = pixiv.get_artwork_id(html)
        img_cnt = pixiv.get_page_count(html)
        artwork_url = pixiv.get_artwork_url(artwork_id)
        original_url = pixiv.get_original_url(artwork_url)
        img_format = pixiv.get_format(original_url)
        file_name = pixiv.get_file_name(html, 0, img_format)
        pixiv.download_ugoira(original_url, file_name, path, html)
        print()
