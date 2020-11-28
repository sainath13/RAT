from os import listdir, path
import env

class preprocessor:
    #read file name
    def readfilename(self):
        #TODO : change to accurate path as we run from root directory
        #select oldest file from here
        list_of_files = listdir(env.download_location)
        full_path = [str(env.download_location+"{0}").format(x) for x in list_of_files]
        oldest_file = min(full_path, key=path.getctime)
        print("selected oldest file" + oldest_file)
        env.config.set('STREAM','filename',str(oldest_file)) 
        env.config.set('STREAM','framenumber','0')
        filename = oldest_file.split("/")
        fileinfo = filename[-1].split("_")
        env.config.set('STREAM','streamid', fileinfo[1])
        env.config.set('STREAM','streamer', fileinfo[0])
        print("At least i am in preprocessor")
        print(str(type(env.config)))
        with open(env.config_location, "w+") as configfile:
                env.config.write(configfile)

    def sendFileName(self,filename):
        #send to firebase schema
        print("Hello")


#if __name__ == '__main__':
#        prepro = preprocessor()
#        print(prepro.readfilename())
