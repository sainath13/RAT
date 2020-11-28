import pyrebase
import env

config = {
        "apiKey": "AIzaSyCryJ4k18JHLdx04b28bOjRPdcfvosxXg8",
        "authDomain": "apexrat-e6ff5.firebaseapp.com",
        "databaseURL": "https://apexrat-e6ff5.firebaseio.com",
        "storageBucket": "apexrat-e6ff5.appspot.com"
        }

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def insert_stream(streamid, streamer):
    url = "https://www.twitch.tv/videos/" + streamid
    data = {"runner":"","status":"unclaimed","streamer":streamer,"url":url}
    db.child("streams").child(streamid).set(data)

def get_streams():
    #getting last three streams to download
    #TODO change query to select unclaimed records:
    last_three_streams = db.child("streams").order_by_child("status").limit_to_first(3)
    print("Hello " + env.config["RUN"]["person"]+ ": Please copy paste below urls in Twitch Leecher")
    print("\n")
    dict_streams = last_three_streams.get().val()
    #print(dict_streams)
    for key, value in dict_streams.items(): 
            print(value["url"])
            record_key = "streams/"+ key + "/"
            record = value
            record["status"] = "downloading"
            record["runner"] = "mrsaitama"
            updated = {record_key : record}
            #print(record["status"] + " : " + record["url"])
            last_three_streams.update(updated)
    print("\nUpdated in DB. ======> These are marked against your name.")


def mark_clipped(streamid):
    stream = db.child("streams").child(streamid).get().val()
    stream["status"] = "clipped"
    key = "streams/" + str(streamid) + "/"
    updated = {key : stream}
    db.update(updated)


def mark_clipping(streamid):
    stream = db.child("streams").child(streamid).get().val()
    stream["status"] = "clipping"
    key = "streams/" + str(streamid) + "/"
    updated = {key : stream}
    db.update(updated)

