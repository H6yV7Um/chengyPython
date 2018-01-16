from crawler_bible import crawler_auto
import os

###获取所有书

url = 'https://www.jw.org/ja/%E5%87%BA%E7%89%88%E7%89%A9/%E8%81%96%E6%9B%B8/bi12/%E5%90%84%E6%9B%B8/'

book_info = crawler_auto.get_books(url)
#
# print(book_info)

##下载一本书的链接


# book_url = 'https://www.jw.org/ja/%E5%87%BA%E7%89%88%E7%89%A9/%E8%81%96%E6%9B%B8/bi12/%E5%90%84%E6%9B%B8/%E5%89%B5%E4%B8%96%E8%A8%98/'
#
# chapter_infos = crawler_auto.get_audio_info(book_url)

# book_dict = {}
# record_books = []
#
# with open('data/info.txt', 'r') as info_file:
#     for row in info_file.readlines():
#         infos = row.strip('\n').split('\t')
#         book_dict[infos[1]] = 1
#     record_books = list(book_dict.keys())
#
#
#
# with open('data/info.txt', 'a') as info_file:
#     for k, v in book_info.items():
#         for book, url in v.items():
#             if book in record_books:
#                 continue
#             chapter_infos = crawler_auto.get_audio_info(url)
#             for chapter, audio_url in chapter_infos.items():
#                 info_file.write(k + '\t' + book + '\t' + chapter + '\t' + audio_url + '\n')


crawler_auto.download_bible('data/info.txt')
