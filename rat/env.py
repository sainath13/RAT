download_location = r'resources/streams/'
config_location = r'resources/generated/metadata/config.ini'
frames_location = r'resources/generated/individualframes/'
clips_location = r'resources/generated/clips/'
mega_embed_url = 'https://mega.nz/embed/'


from configparser import ConfigParser
config = ConfigParser()
config.read(config_location)

