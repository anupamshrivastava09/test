import boto3
import hashlib
import os
import sys
import time
import subprocess

class AWSTTS():
    def __init__(self,profile,lang,speaker_voice,gender,soundpath,rate,pitch,volume,text_data,*args,**kwargs):
        #self.profile=profile
        os.environ['AWS_PROFILE'] = profile
        #self.region=region
        self.lang=lang
        self.speaker_voice=speaker_voice
        self.gender=gender
        self.soundpath=soundpath
        self.rate=rate
        self.pitch=pitch
        self.volume=volume
        self.text_data=text_data
        self.audioformat="pcm"

    def tts (self) :
        self.polly = boto3.client('polly')
        filelist = []
        arguments = self.text_data
        
        for i in range(0, len(arguments)):
            AWSTTS.text = arguments[i]
            AWSTTS.md5text=arguments[i]+self.lang+self.speaker_voice
            File, status = self.synthesize()
            if status == "NO":
                FF = File.split('.')
                filelist.append(FF[0])
            else:
                
                filelist.append(File)
        return (filelist)
    
    def synthesize(self):
        status, data = self.createVerifyMD5()
        if status == 'absent':
            text='<speak><prosody rate="'+self.rate+'" pitch="'+self.pitch+'" volume="'+self.volume+'">"'+self.md5text+'"</prosody></speak>'
            self.spoken = self.polly.synthesize_speech(Text=text, TextType="ssml",SampleRate="8000", OutputFormat=self.audioformat, VoiceId=self.speaker_voice)
            return (self.saveStream(),"NO")
        elif status == "present":
            return (data,"YES")

    def saveStream(self):
        if not os.path.exists(self.soundpath):
            os.makedirs(self.soundpath, 0o764)
            try:
                os.system(f'chown root:root {self.soundpath}')
            except Exception as e:
                print(f'Warn: {e}')

        filename = self.checksum + '.raw'
        filename = os.path.join(self.soundpath, filename)
        with open(filename, 'wb') as rvn:
            rvn.write(self.spoken['AudioStream'].read())
            rvn.close()
        return os.path.basename(filename)

    def createVerifyMD5(self):
        self.checksum = hashlib.md5(self.md5text.encode()).hexdigest()
        file_1 = self.checksum+'.raw'
        self.makedir(self.soundpath)
        try:
            for root, dirs, files in os.walk(self.soundpath):
                if file_1 in files:
                    #return_file = self.checksum.split('.')
                    return ('present', self.checksum )
                else:
                    return ('absent', self.checksum)
        except Exception as e:
            print(e)

    def makedir(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)
