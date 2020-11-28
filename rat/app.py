from download.preprocessor import preprocessor
from clipper.clipmaker import clipmaker
from os import listdir, remove
import env
from firebae import firebae

class rat:
    #def __init__(self):
    #    print("Hello from init")
    def run(self):
        if(listdir(env.download_location) == []):
            print("No files to process, please download new files in Twitch leecher")
            firebae.get_streams()
            exit()

        while(listdir(env.download_location) != []):
            filename = env.config["STREAM"]["filename"]
            if(filename == ""):
                print("No file is being processed, selecting the oldest file")
                pre = preprocessor()
                pre.readfilename()
            else:
                print("Already a file in progress")

            #TODO : send filename being processed to server

            #if(status):
            clipper = clipmaker()
            finished = clipper.clip()

            if(finished):
                filename = env.config["STREAM"]["filename"]
                firebae.mark_clipped(env.config["STREAM"]["streamid"])
                remove(filename)
                print("deleted stream: "+ filename)
                env.config.set('STREAM','filename','')
                env.config.set('STREAM','framenumber','')
                env.config.set('STREAM','streamer','')
                env.config.set('STREAM','streamid','')
                with open(env.config_location, "w+") as configfile:
                    env.config.write(configfile)
                
            #run this in a loop
            print("running for file :" )
        print("finished processing all the files. download some files now")
        print("Update status to server")
        exit()

    def getDownloadLinks(self):
        #Decided to process one file only for now
        print("here is one new download link")
