import os

# m3u8_url = crawler_rekion.get_audio_url_from_page('http://rekion.dl.ndl.go.jp/info:ndljp/pid/1314804')
# print(m3u8_url)
#
# crawler_rekion.download_m3ufile(m3u8_url)


source_m3ufile = 'data/test.m3u'
target_mp3file = 'data/xxx.mp3'
cmd = 'ffmpeg -protocol_whitelist file,tcp,http,crypto -i ' + source_m3ufile + ' -c copy ' + target_mp3file
res = os.popen(cmd).readlines()
print(res)
