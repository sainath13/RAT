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
    data = {"runner":"","status":"UNCLAIMED","streamer":streamer,"url":url}
    db.child("streams").child(streamid).set(data)

def get_streams():
    #TODO change query to select unclaimed records:
    is_downloading = False
    my_marked_streams = db.child("streams").order_by_child("runner").equal_to(env.config["RUN"]['person']).get().val()
    if len(my_marked_streams) > 0 :
        for key, value in my_marked_streams.items():
            if(value["status"]  == "DOWNLOADING"):
                is_downloading = True
                print("Please download this file first. It was marked against your name",value["url"])

    if(is_downloading == False):
        last_three_streams = db.child("streams").order_by_child("status").equal_to("UNCLAIMED").limit_to_first(3)
        print("Hello " + env.config["RUN"]["person"]+ ": Please copy paste below urls in Twitch Leecher")
        print("\n")
        dict_streams = last_three_streams.get().val()
        #print(dict_streams)
        for key, value in dict_streams.items(): 
                print(value["url"])
                record_key = "streams/"+ key + "/"
                record = value
                record["status"] = "DOWNLOADING"
                record["runner"] = env.config["RUN"]["person"] 
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
    stream["status"] = "CLIPPING"
    key = "streams/" + str(streamid) + "/"
    updated = {key : stream}
    db.update(updated)

def send_clip_details(filename,url):
    print("Sending clip data to firebase")
    clips = db.child("clips")
    clip_data = {
            "filename" : filename,
            "game" : "Apex Legends",
            "streamer" : env.config["STREAM"]["streamer"],
            "url" : url,
            "category" : "NA"
            }
    clips.push(clip_data)
    print("Sent clips data to firebase") 
