import redis
import pymongo

r = redis.Redis(host='127.0.0.1', port=6379, db=0)
conn = pymongo.MongoClient('mongodb://localhost:27017/')


print("============user part================")
users = conn.test.music163User
completed_num = 0
user_id_key = "user_id"
mongo_users = list(users.find().limit(1000).skip(completed_num))
pipe = r.pipeline()
while len(mongo_users) > 0:
    for mongo_user in mongo_users:
        pipe.sadd(user_id_key, mongo_user['_id'])
    pipe.execute()
    completed_num = completed_num + 1000
    mongo_users = list(users.find().limit(1000).skip(completed_num))

print("=========transfer user data over==========")


print("============song part================")
songs = conn.test.music163Song
completed_num = 0
mongo_songs = list(songs.find().limit(1000).skip(completed_num))
song_id_key = "song_id"

pipe = r.pipeline()
while len(mongo_songs) > 0:
    for mongo_song in mongo_songs:
        pipe.sadd(song_id_key, mongo_song['_id'])
    pipe.execute()
    completed_num = completed_num + 1000
    mongo_songs = list(songs.find().limit(1000).skip(completed_num))

print("=========transfer song data over==========")
