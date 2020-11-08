import click
import curses
import pyfiglet
import Pixiv_Crawler

class Pixiv_Downloader():
    def __init__(self):
        self.pixiv = Pixiv_Crawler.Pixiv()
        self.stdscr = curses.initscr()
        self.init_ui()
        self.length = None
        
    def init_ui(self):
        ascii_banner = pyfiglet.figlet_format("PIXIV DOWNLOADER")
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.addstr(0, 0, ascii_banner)
        self.stdscr.refresh()
  
    def get_data(self, illust_detail):
        data = {
            'url': illust_detail['url_big'],
            'title': illust_detail['title'],
            'author': illust_detail['author_details']['user_name'],
            'bookmark': illust_detail['bookmark_user_total'],
            'description': '\n              '.join(str(illust_detail['meta']['twitter_card']['description']).split('\r\n'))
        }
        return data
        
    def print_detail(self, illust_data):
        self.stdscr.addstr(1, 0, f'Download      {illust_data["url"]}')
        self.stdscr.addstr(2, 0, f'Title         {illust_data["title"]}')
        self.stdscr.addstr(3, 0, f'Author        {illust_data["author"]}')
        self.stdscr.addstr(4, 0, f'Bookmark      {illust_data["bookmark"]}')
        self.stdscr.addstr(5, 0, f'Description   {illust_data["description"]}')
        self.stdscr.refresh()
        
    def print_total_progress(self, progress):
        self.stdscr.addstr(0, 0, 'Total progress: [{1:10}] {0}%'.format(round((progress) / self.length * 100), '#' * int((progress) / self.length * 10)))
        self.stdscr.refresh()
  
    def user_illusts_download(self, uid):
        res = self.pixiv.user_illust(uid, is_pc=True)
        illust_ids = res['body']['illusts']
        
        illust_details = [self.pixiv.illust_detail(illust_id, is_pc=True)['body']['illust_details'] for illust_id in illust_ids]
        
        self.stdscr.clear()
        progress = 1
        self.length = len(illust_details)
        for illust_detail in illust_details:
            illust_data = self.get_data(illust_detail)
            
            self.print_total_progress(progress - 1)
            self.print_detail(illust_data)
            
            self.pixiv.download(illust_data['url'])
            
            self.print_total_progress(progress)
            self.stdscr.clear()
            progress += 1
        self.stdscr.refresh()
            
@click.command()
@click.option('--uid', default=None, help='Pixiv user page id.')
def run_user_illusts_download(uid):
    Pixiv_Downloader().user_illusts_download(uid)

if __name__ == '__main__':
    run_user_illusts_download()
    curses.endwin()
