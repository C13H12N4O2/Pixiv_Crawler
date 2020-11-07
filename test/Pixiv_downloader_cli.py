import click
import requests
import shutil
import os
import curses
import pyfiglet

def get_orig_url(illust_detail):
    return illust_detail['url_big']
    
def get_title(illust_detail):
    return illust_detail['title']
    
def get_author(illust_detail):
    return illust_detail['author_details']['user_name']
    
def get_description(illust_detail):
    return '\n              '.join(str(illust_detail['meta']['twitter_card']['description']).split('\r\n'))
    
def get_bookmark(illust_detail):
    return illust_detail['bookmark_user_total']

@click.command()
@click.option('--uid', default=None, help='Pixiv user page id.')
def download(uid):
    user_url = f'https://www.pixiv.net/ajax/user/{uid}/profile/all'
    illust_ids = requests.get(user_url).json()['body']['illusts']
    
    illust_url = 'https://www.pixiv.net/touch/ajax/illust/details'
    illust_details = [requests.get(illust_url, params={'illust_id': illust_id}).json()['body']['illust_details'] for illust_id in illust_ids]
    
    stdscr.clear()
    progress = 1
    length = len(illust_details)
    for illust_detail in illust_details:
        url = get_orig_url(illust_detail)
        title = get_title(illust_detail)
        author = get_author(illust_detail)
        description = get_description(illust_detail)
        bookmark = get_bookmark(illust_detail)
        headers = {'referer': 'https://app-api.pixiv.net/'}
        
        res = requests.get(url, headers = headers, stream=True)
        stdscr.addstr(0, 0, 'Total progress: [{1:10}] {0}%'.format(round((progress - 1) / length * 100), '#' * int((progress - 1) / length * 10)))
        stdscr.addstr(1, 0, f'Download      {url}')
        stdscr.addstr(2, 0, f'Title         {title}')
        stdscr.addstr(3, 0, f'Author        {author}')
        stdscr.addstr(4, 0, f'Bookmark      {bookmark}')
        stdscr.addstr(5, 0, f'Description   {description}')
        stdscr.refresh()
        
        file_name = os.path.basename(url)
        with open(file_name, 'wb') as handle:
            shutil.copyfileobj(res.raw, handle)
        stdscr.addstr(0, 0, 'Total progress: [{1:10}] {0}%'.format(round(progress / length * 100), '#' * int(progress / length * 10)))
        stdscr.refresh()
        stdscr.clear()
        
        progress += 1

if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("PIXIV DOWNLOADER")
    stdscr = curses.initscr()
    stdscr.addstr(0, 0, ascii_banner)
    stdscr.refresh()
    download()
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    

