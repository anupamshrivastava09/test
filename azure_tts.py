import requests
import os
import hashlib
import sys
import subprocess

class azure:

    def __init__(self,credential,langcode,speakervoice,gender,soundpath,rate,pitch,volume,args) :
        self.credential = credential
        self.langcode = langcode
        self.speakervoice = speakervoice
        self.gender=gender
        self.soundpath = soundpath
        self.rate=rate
        self.pitch=pitch
        self.volume=volume
        self.text_data = args
        self.audioformat='raw'
        
    def atts (self):
        filelist = []
        arguments = self.text_data
        for i in range(0, len(arguments)):
            
            azure.text = arguments[i]
            azure.textdata=arguments[i]+self.langcode+self.speakervoice
            File, status = self.synthesize()
            if status == "No":
                filelist.append(File)
            else:
                filelist.append(File)
        return (filelist)

    def get_token(self):
        fetch_token_url = 'https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        headers = {
                'Ocp-Apim-Subscription-Key': self.credential
                }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)
        return access_token

    def createvarify_Md5(self):
        checksum = hashlib.md5(self.textdata.encode()).hexdigest()
        file1 = checksum+'.raw'
        self.makedir(self.soundpath)
        for root, dirs, files in os.walk(self.soundpath):
            if file1 in files:
                #return_file = file1.split('.')
                return ('Present', checksum)
            else:
                return ('Absent', checksum)


    def synthesize(self):
        status, azure.data = self.createvarify_Md5()
        if status == 'Absent':
            Token = self.get_token()
            url = 'https://centralindia.tts.speech.microsoft.com/cognitiveservices/v1'
            headers = {
                    'Authorization':'Bearer'+Token,
                    'Ocp-Apim-Subscription-Key':self.credential,
                    'Content-Type':'application/ssml+xml',
                    'X-Microsoft-OutputFormat':'raw-8khz-16bit-mono-pcm'
                    }
            xml = "<speak version='1.0' xml:lang="+"\'"+self.langcode+"\'"+"><voice xml:lang="+"\'"+self.langcode+"\'"+" xml:gender="+"\'"+self.gender+"\'"+" name="+"\'"+self.speakervoice+"\'"+">"+self.textdata+"<prosody pitch='"+self.pitch+"' rate='"+self.rate+"' volume='"+self.volume+"'></prosody></voice></speak> "
            response =  requests.post(url, data=xml, headers=headers)
            Sound = self.save(response)
            Sound = Sound.split('.')
            return Sound[0], "No"
        else:
            return self.data, "Yes"

    def save(self,response):
        music_name = self.data+'.raw'
        music_name = os.path.join(self.soundpath, music_name)
        with open(music_name, "wb") as out:
            out.write(response.content)
        return os.path.basename(music_name)

    def makedir(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)
