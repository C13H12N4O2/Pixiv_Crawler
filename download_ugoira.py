import Pixiv_Crawler

def on_PC(illust_id):
    pixiv = Pixiv_Crawler.Pixiv()
    res = pixiv.ugoira_metadata(illust_id, is_pc=True)
    
    url = res['body']['src']
    delay = []
    for data in res['body']['frames']:
        delay.append(data['delay']/1000)
    pixiv.download(url, delay)
    
def on_APP(illust_id):
    pixiv = Pixiv_Crawler.Pixiv()
    pixiv.login('pixiv_id', 'password')
    res = pixiv.ugoira_metadata(illust_id)
    
    url = res['ugoira_metadata']['zip_urls']['medium']
    delay = []
    for data in res['ugoira_metadata']['frames']:
        delay.append(data['delay']/1000)
    pixiv.download(url, delay)
    
def main():
    illust_id = '49109712'
    
    on_PC(illust_id)
    #on_APP(illust_id)

if __name__ == '__main__':
    main()
