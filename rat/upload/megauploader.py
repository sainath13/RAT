import env
from mega import Mega
from firebae import firebae


mega = Mega()

m = mega.login("latkarsai@gmail.com", "saitamaSensei")

quota = m.get_quota()
print(quota)

space = m.get_storage_space(kilo=True)
unused_space = (space["total"] - space["used"])/1024/1024


if(unused_space < 2):
    print("Not much space is available on Mega. Contact Sainath Or Vignesh")
    exit()
else:
    print("Space is available. Proceeding with clipping")

#file = m.upload("knock.mp4")
#upload_url = m.get_upload_link(file)
#print(upload_url[21:])
#print(upload_url)
#https://mega.co.nz/#!QF1CiBYD!ygg36CUMF4DK6lasOpeJt3ZUMhvqaKc7jXJ1K8LENx0

def upload_clip_to_mega(filename):
    print("uploading clip")
    file = m.upload(env.clips_location + filename)
    upload_url = m.get_upload_link(file)
    print("Success : Clip uploaded to Mega")
    upload_url_id = upload_url[21:]
    url = env.mega_embed_url + upload_url_id
    firebae.send_clip_details(filename, url)
    #trim the upload url and send to firebae
