import tweepy
import requests
import twitch
import time
import shutil
from PIL import Image


class TwitterBot:

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located
    # under "Your access token")
    consumer_key = "" # Insert your own Twitter Consumer Key here:
    consumer_secret = "" # Insert your own Twitter Consumer Secret here:
    access_token = "" # Insert your own Twitter Access Token here:
    access_token_secret = "" # Insert your own Twitter Access Token Secret here:
    client_id = ""  # Insert your own Twitch Client ID here:
    client_secret = ""  # Insert your own Twitch Client Secret here:
    twitch_username = "" # Insert your Twitch username here:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    originalName = api.me().screen_name
    originalDescription = api.me().description
    originalImageUrl = api.me().profile_image_url
    actualOriginalImage = originalImageUrl[0: len(originalImageUrl)-11] + ".png"
    image = requests.get(actualOriginalImage, stream=True)
    image.raw.decode_content = True


    with open('original.png', 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)
        out_file.close()

    request = requests.post('https://id.twitch.tv/oauth2/token?client_id='+ client_id + '&client_secret=' + client_secret + '&grant_type=client_credentials')
    for key, value in request.json().items():
        if key == 'access_token':
            oauthstring = value
            print(key, ":", value)
    helix = twitch.TwitchHelix(client_id=client_id, oauth_token=oauthstring)
    data = helix.get_streams(user_logins=twitch_username)
    islive = False
    nameReset = False
    nameChanged = False
    pictureReset = False
    pictureChanged = False



    def changeprofilepicture(self):
        if self.pictureChanged:
            return
        self.pictureChanged = True
        self.pictureReset = False

        img = Image.open("redcircle.png")
        background = Image.open('original.png')

        background.paste(img, (0, 0), img)
        background.save('uploadImage.png', "PNG")
        self.api.update_profile_image('uploadImage.png')

    def resetprofilepicture(self):
        if self.pictureReset:
            return
        self.pictureChanged = False
        self.pictureReset = True
        self.api.update_profile_image('original.png')

    def changenameandbio(self):
        if self.nameChanged:
            return
        self.nameChanged = True
        self.nameReset = False
        self.api.update_profile("🔴Live ttv/" + test.twitch_username)
        self.api.update_profile(description="🔴Live twitch.tv/" + + test.twitch_username + "\n" + self.originalDescription)

    def resetnameandbio(self):
        if self.nameReset:
            return
        self.nameChanged = False
        self.nameReset = True
        self.api.update_profile(self.originalName)
        self.api.update_profile(description=self.originalDescription)

    def is_live_stream(self):
        if str(self.data) != '[]':
            self.islive = True
        print(self.islive)
        print(str(self.data))
        return self.islive

    def __init__(self):
        while True:
            print("done1")
            if self.is_live_stream():
                print('a')
                self.changenameandbio()
                self.changeprofilepicture()
            else:
                print('b')
                self.resetnameandbio()
                self.resetprofilepicture()
            time.sleep(600000)

test = TwitterBot()



