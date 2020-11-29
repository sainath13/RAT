import env
import time
import cv2 
import os
import easyocr
from datetime import datetime
from PIL import Image 
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os, re, os.path
import glob
import sys
reader = easyocr.Reader(['ch_sim','en'])
from upload import megauploader


class clipmaker:

    def __init__(self):
        print("initializing")

    def clip(self):
        print("Clipping")
        firebae.mark_clipping(env.config["STREAM"]["streamid"])
        current_frame = 0
        frame_check_rate = 60
        start_minus = 20
        end_plus = 20
        result_list = []
        left = 600
        top = 600
        right = 1200
        bottom = 900
        is_clip = False
        start_time = 0
        latest_knockdown_time = 0

        stream = env.config["STREAM"] 
        print("clipping the file",stream["filename"])
        print("framenumber is ",stream["framenumber"])
        framenumber = int(stream["framenumber"])
        cam = cv2.VideoCapture(stream["filename"])
         
        if(framenumber > 0):
            temp_frame = 0
            while(temp_frame < framenumber):
                ret, frame = cam.read()
                temp_frame += 1
            print("Skipped "+str(temp_frame)+ " frames as they are already processed")
        

        while(True):
            ret, frame = cam.read()
            if ret:
                print("True")
                name = env.frames_location + str(current_frame) + '.jpg'
                if(current_frame%frame_check_rate == 0):
                    status = cv2.imwrite(name,frame)
                    #print(status)
                    im = Image.open(name)
                    im1 = im.crop((left, top, right, bottom))
                    im1 = im1.save(name)
                    result = reader.readtext(name, detail = 0)
                    curr_time = cam.get(cv2.CAP_PROP_POS_MSEC)/1000
                    result_list.append(result)

                    os.remove(name)

                    for res in result:
                        if "KNOCK" in res or "KOCK" in res or "NATED" in res or "ELMI" in res or "ASS" in res or "IST" in res or "KNU" in res or "DOwN" in res or "ELM" in res or "EUM" in res:
                            #TODO : find a better way to do this
                            print('knocked!!!!' + str(curr_time))
                            latest_knockdown_time = curr_time
                            if(is_clip == False):
                                print("is clip is false")
                                start_time = curr_time
                                is_clip = True

                    if(is_clip):
                        if( (curr_time - latest_knockdown_time) >= int(env.config["CLIP"]["after_clip_margin"])) :
                            end_time = latest_knockdown_time + end_plus
                            start_time = start_time - start_minus
                            print("Making a clip from" + str(start_time) + "to" + str(end_time))
                            filename = "Knock_" + str(env.config["STREAM"]["streamer"] + "_" + str(env.config["STREAM"]["streamid"]+"_"+str(start_time)+"_"+str(end_time)+".mp4"))
                            ffmpeg_extract_subclip(stream["filename"],start_time,end_time,targetname=env.clips_location+filename)
                            megauploader.upload_clip_to_mega(filename)
                            is_clip = False

                if(current_frame%1000 == 0):
                    env.config.set('STREAM','framenumber',str(current_frame))
                    with open(env.config_location, "w+") as configfile:
                        env.config.write(configfile)


                current_frame += 1
            else: 
                print("Good job, reading all the frames is complete")
                #Export footage if not done already
                if(is_clip):
                    end_time = latest_knockdown_time + end_plus
                    start_time = start_time - start_minus
                    print("Making a clip from" + str(start_time) + "to" + str(end_time))
                    filename = "Knock_" + str(env.config["STREAM"]["streamer"] + "_" + str(env.config["STREAM"]["streamid"]+"_"+str(start_time)+"_"+str(end_time)+".mp4"))
                    ffmpeg_extract_subclip(stream["filename"],start_time,end_time,targetname=filename)
                    megauploader.upload_clip_to_mega(filename)
                    break
                break


        #skip those many frames and then start processing
        #while(framenumber < 2000):
        #    framenumber += 1
        #    if(framenumber%1000 == 0):
        #        time.sleep(5)
        #        env.config.set('STREAM', 'framenumber', str(framenumber))
        #        with open(env.config_location, "w+") as configfile:
        #            env.config.write(configfile)
        #        print("knocked"+str(framenumber))
        #
        return True
