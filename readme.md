# Pixiv Crawler API

> Pixiv Crawler API

## Example Program
<img src="imgs/Pixiv_downloader_cli_test.gif">

## Getting started

To start making a pixiv image downloader with Pixiv Crawler API, initialize an object.

```
import Pixiv_crawler

pixiv = Pixiv_Crawler.Pixiv()
```

There are only two ways to log into Pixiv. One is by logging in with your pixiv id and password.

```
pixiv.login('pixiv_id', 'password')
```

And another is with a refresh token.

```
pixiv.login('refreshtoken')
```

## APIs

### parse_url(url, mode, headers, data, params, stream)

```
Parameters  url(str)  - The url to the Pixiv pages or file.
            mode(str) - The request mode. Supports get, post and delete.
            headers   - The user-agent and referer headers. 
            params    - The url parameters.
            stream    - If false, the response content will be immediately
                        downloaded.
```
              
### login(pixiv_id, password, refresh_token)

```
Parameters  pixiv_id(str)      - The Pixiv account.
            password(str)      - The Pixiv password.
            refresh_token(str) - The Pixiv refresh_token 
```

### user_detail(user_id, filter)

```
Parameters  user_id(str)  - The Pixiv user ID.
            filter        - The page filter.
```

### user_illust(user_id, type, tags, restrict, filter, offset, is_pc)

```
Parameters  user_id(str)  - The Pixiv user ID.
            type(str)     - The type of content
                            [Illust, Manga, Ugoira, Novel]
            tags(str)     - The content tags.
            restrict      - If false, the page will show mature contents.
            filter        - The page filter.
            offset        - The page offset.
```

### user_bookmark_illust(user_id, restrict, filter, offset)

```
Parameters  user_id(str)  - The Pixiv user ID.
            restrict      - If false, the page will show mature contents.
            filter        - The page filter.
            offset        - The page offset.
```

### user_following(user_id, restrict, filter, offset)

```
Parameters  user_id(str)  - The Pixiv user ID.
            restrict      - If false, the page will show mature contents.
            filter        - The page filter.
            offset        - The page offset.
```

### user_mypixiv(user_id, restrict, filter, offset)

```
Parameters  user_id(str)  - The Pixiv user ID.
            restrict      - If false, the page will show mature contents.
            filter        - The page filter.
            offset        - The page offset.
```

### illust_detail(illust_id, is_pc)

```
Parameters  illust_id(str)  - The Pixiv illust ID.
            is_pc           - If true, the page is PC-based.
```

### illust_pages(illust_id)

```
Parameters  illust_id(str)  - The Pixiv illust ID.
```

### illust_comments(illust_id, include_total_comments, offset)

```
Parameters  illust_id(str)         - The Pixiv illust ID.
            include_total_comments - If true, the page will show total
                                     comments on this page.
            offset                 - The page offset.
```

### illust_recommended(illust_id, filter, min_bookmark_id_for_recent_illust, max_bookmark_id_for_recommend, offset, include_ranking_illusts, include_privacy_policy)

```
Parameters  illust_id(str)                    - The Pixiv illust ID.
            filter                            - The page filter.
            min_bookmark_id_for_recent_illust - The minimum bookmarked
                                                illust id for recent illusts.
            max_bookmark_id_for_recommend     - The maximum bookmarked
                                                illust id for recommended
                                                illusts.
            offset                            - The page offset.
            include_ranking_illusts           - If false, the page will not
                                                show ranking illusts.
            include_privacy_policy            - If false, the page will not
                                                show private illusts or mature
                                                contents.
```
        
### illust_ranking(mode, content, index, filter, date, offset, is_pc)

```
Parameters  mode    - The Pixiv ranking page mode. 
                      If is_pc is false, the available modes are
                      [day, week, month, day_male, day_female, week_original,
                       week_rookie, day_manga]
                      If is_pc is true, the available modes are
                      [daily, daily_r18, weekly, weekly_r18, monthly, rookie,
                       original, male, male_r18, female, female_r18, r18g]
                      p.s. Since API could not access to PC-based Pixiv login
                           page because of reCAPTCHA, only mature contents are
                           available.
            content - The Pixiv ranking page content. Content parameter can be
                      used when is_pc is true. The available modes are
                      [illust, manga, ugoira]
            index   - The Pixiv ranking page index. index parameter can be used
                      when is_pc is true. Maximum indices are 
                      [daily: {None: 10, illust: 10, ugoira: 2, manga: 10},
                       daily_r18: {None: 2, illust: 2, ugoira: 2, manga: 2},
                       weekly: {None: 10, illust: 10, ugoira: 2, manga: 10},
                       weekly_r18: {None: 2, illust: 2, ugoira: 1, manga: 2},
                       monthly: {None: 10, illust: 5, manga: 2},
                       rookie: {None: 6, illust: 6, manga: 2},
                       original: {None: 6},
                       male: {None: 10},
                       male_r18: {None: 6},
                       female: {None: 10},
                       female_r18: {None: 6},
                       r18g: {None: 1, illust: 1}]
            filter  - The page filter.
            date    - The date of Pixiv ranking page.                   
            offset  - The page offset.
            is_pc   - If false, the page will not show private illusts or mature contents.
```
        
### trending_tags_illust(filter)

```
Parameters  filter  - The page filter.
```

### search_illust(word, include_translated_tag_results, merge_plain_keyword_results, filter, search_target, sort, duration, start_date, end_date, offset)

```
parameters  word                            - The keyword for searching illusts on Pixiv.
            include_translated_tag_results  - If false, the translated tag will not be
                                              included on the search result page.
            merge_plain_keyword_results     - If false, the plain keywords will not be
                                              merged.
            filter                          - The page filter.
            search_target                   - The partial match tags.
            sort                            - Sort the search result page.
            duration                        - The max-date for the illusts.
            start_date                      - Set the start date of illust for searching.
            end_date                        - Set the end date of illust for searching.
            offset                          - The page offset.
```

### search_user(word, filter, sort, duration, offset)
        
```
parameters  word        - The keyword for searching users on Pixiv.
            filter      - The page filter.
            sort        - Sort the search result page.
            duration    - The max-date for the users.
            offset      - The page offset.
```
        
### ugoira_metadata(illust_id, is_pc)

```
parameters  illust_id(str)   - The Pixiv illust ID.
            is_pc            - If true, the page is PC-based.
```

### illust_follow(restrict, filter)

```
parameters  restrict    - If false, the page will show mature contents.
            filter      - The page filter.
```
        
### illust_related(illust_id, filter, seed_illust_ids, offset)

```
parameters  illust_id(str)  - The Pixiv illust ID.
            filter          - The page filter.
            seed_illust_ids - The page will show illusts based on seed illust ids.
            offset          - The page offset.
```

### illust_bookmark_detail(illust_id, filter)

```
parameters  illust_id(str)  - The Pixiv illust ID.
            filter          - The page filter.
```
        
### illust_bookmark_add(illust_id, restrict, tags)

```
parameters  illust_id(str)  - The Pixiv illust ID.
            restrict        - If false, bookmark an illust into the public bookmark list.
            tags            - Bookmark an illust into the given bookmark tag list.
```

### illust_bookmark_delete(illust_id)

```
parameters  illust_id(str)  - The Pixiv illust ID.
```
        
### illust_bookmark_detail(illust_id)

```
parameters  illust_id(str)  - The Pixiv illust ID.
```

### illust_bookmark_users(illust_id)

```
parameters  illust_id(str)  - The Pixiv illust ID.
```

### user_follow(user_id, restrict)

```
parameters  user_id(str)  - The Pixiv user ID.
            restrict      - If false, follow an user into the public follow list.
```
        
### user_unfollow(user_id, restrict)

```
parameters  user_d(str)  - The Pixiv user ID.
            restrict     - If false, unfollow an user into the public follow list.
```

### user_follow_detail(user_id)

```
parameters  user_d(str)  - The Pixiv user ID.
```

### spotlight_articles(offset)

```
parameters  offset  - The page offset.
```
        
### emoji()

```

```

### user_list(user_id, filter, offset)

```
parameters  user_id(str)  - The Pixiv user ID.
            filter        - The page filter.
            offset  - The page offset.
```
        
### illust_new(max_illust_id)

```
parameters  max_illust_id(str)  - ///
```
        
### illust_series(illust_series_id)

```
parameters  illust_series_id(str)  - The Pixiv illust series ID.
```

### download(url, delay)

```
parameters  url     - The image url or ugoira zip url.
            delay   - The ugoira delay.
```
