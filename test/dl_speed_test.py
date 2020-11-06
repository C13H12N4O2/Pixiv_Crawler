import requests
import asyncio
import functools
import shutil
import os
import time
from multiprocessing.pool import ThreadPool

s = time.time()

async def get_req(url):
    req = await loop.run_in_executor(None, requests.get, url)
    dict = req.json()['body']['illusts']
    url = 'https://www.pixiv.net/touch/ajax/illust/details'
    reqs = [await loop.run_in_executor(None, functools.partial(requests.get, url, params={'illust_id': illust_id})) for illust_id in dict]
    return reqs
    
def get_req2(url):
    dict = requests.get(url).json()['body']['illusts']
    urls = ThreadPool(len(dict)).imap_unordered(get_req3, dict)
    imgs = ThreadPool(len(dict)).imap_unordered(get_req4, urls)
    results = ThreadPool(len(dict)).imap_unordered(dl_img2, imgs)
    for r in results:
        r
    
def get_req3(illust_id):
    url = 'https://www.pixiv.net/touch/ajax/illust/details'
    params={'illust_id': illust_id}
    return requests.get(url, params=params, stream=True).json()['body']['illust_details']['url_big']
    
def get_req4(url):
    headers = {'referer': 'https://app-api.pixiv.net/'}
    return requests.get(url, headers=headers, stream=True)
        
async def get_img_req(urls):
    req = [[url, await loop.run_in_executor(None, functools.partial(requests.get, url, headers = {'referer': 'https://app-api.pixiv.net/'}, stream=True))] for url in urls]
    return req
    
def download_img(data):
    file_name = os.path.basename(data)
    res = requests.get(data, headers = {'referer': 'https://app-api.pixiv.net/'}, stream=True)
    with open(file_name, 'wb') as handle:
        shutil.copyfileobj(res.raw, handle)
    handle.close()
    
def dl_img(data):
    file_name = os.path.basename(data[0])
    with open(file_name, 'wb') as handle:
        shutil.copyfileobj(data[1].raw, handle)
    return file_name
    
def dl_img2(data):
    file_name = os.path.basename(data.url)
    with open(file_name, 'wb') as handle:
        shutil.copyfileobj(data.raw, handle)
    handle.close()
    return file_name
    
async def main():
    url = 'https://www.pixiv.net/ajax/user/14866303/profile/all'
    htmls = asyncio.ensure_future(get_req(url))
    imgs = [itr.json()['body']['illust_details']['url_big'] for itr in await htmls]
    data = asyncio.ensure_future(get_img_req(imgs))
    results = ThreadPool(len(imgs)).imap_unordered(dl_img, await data)
    for r in results:
        r
    
async def main2():
    url = 'https://www.pixiv.net/ajax/user/14866303/profile/all'
    htmls = asyncio.ensure_future(get_req(url))
    imgs = [itr.json()['body']['illust_details']['url_big'] for itr in await htmls]
    results = ThreadPool(len(imgs)).imap_unordered(download_img, imgs)
    for r in results:
        r
'''
# 1
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close
e = time.time()
print(e - s)
'''

'''
# 2
s = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main2())
loop.close
e = time.time()
print(e - s)
'''

# 3
s = time.time()
url = 'https://www.pixiv.net/ajax/user/14866303/profile/all'
get_req2(url)

e = time.time()
print(e - s)

'''
# 4
s = time.time()

url = 'https://www.pixiv.net/ajax/user/14866303/profile/all'
dict = requests.get(url).json()['body']['illusts']

url = 'https://www.pixiv.net/touch/ajax/illust/details'
reqs = [requests.get(url, params={'illust_id': illust_id}).json()['body']['illust_details']['url_big'] for illust_id in dict]
results = ThreadPool(len(reqs)).imap_unordered(download_img, reqs)
for r in results:
    r

e = time.time()
print(e - s)
'''

# 5
'''
s = time.time()

url = 'https://www.pixiv.net/ajax/user/14866303/profile/all'
dict = requests.get(url).json()['body']['illusts']

url = 'https://www.pixiv.net/touch/ajax/illust/details'
reqs = [requests.get(url, params={'illust_id': illust_id}).json()['body']['illust_details']['url_big'] for illust_id in dict]
for url in reqs:
    res = requests.get(url, headers = {'referer': 'https://app-api.pixiv.net/'}, stream=True)
    file_name = os.path.basename(url)
    with open(file_name, 'wb') as handle:
        shutil.copyfileobj(res.raw, handle)

e = time.time()
print(e - s)
'''
