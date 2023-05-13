from google.cloud import texttospeech
from google.cloud.texttospeech import AudioEncoding as ae
from google.cloud.texttospeech import SsmlVoiceGender as vg
import os
import hashlib
import sys
import subprocess
import importlib

class GCPT2S :
    def __init__(self, credential, langcode, langtype, gender, soundpath, rate, pitch, volume, textdata):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential
        self.credential = credential
        self.langcode = langcode
        self.langtype = langtype
        self.gender = gender.upper()
        self.soundpath = soundpath
        self.rate = rate
        self.pitch = pitch
        self.volume = volume
        self.data_arg = textdata
        self.audioformat='LINEAR16'
        
    def data_analyse(self): 
        credential = self.credential
        Lang_Code = self.langcode
        Lang_Type = self.langtype
        File_Dir = self.soundpath
        arguments=self.data_arg
        filelist = []
        
        for i in range(0, len(arguments)):
            GCPT2S.text = arguments[i]
            GCPT2S.textdata=arguments[i]+Lang_Code+Lang_Type
            File, status = self.synthesize()
            if status == "No":
                filelist.append(File)
            else:
                filelist.append(File)
        return (filelist)
            
    def synthesize(self):
        GENDER=getattr(vg,self.gender)
        AUDIOFORMAT=getattr(ae,self.audioformat)
        status, GCPT2S.data = self.createvarify_Md5()
        if status == "Absent":
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=self.textdata)
            voice = texttospeech.VoiceSelectionParams(
                    language_code=self.langcode, name=self.langtype, ssml_gender=GENDER
                    )
            audio_config = texttospeech.AudioConfig(
                    speaking_rate=float(self.rate),pitch=float(self.pitch),volume_gain_db=float(self.volume),sample_rate_hertz=8000, audio_encoding=AUDIOFORMAT
                    )
            GCPT2S.response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                    )
            FL = self.save()
            FL = FL.split('.')
            return FL[0], "No"
        else:
            return self.data, "Yes"

    def save(self):
        if not os.path.exists(self.soundpath):
            os.makedirs(self.soundpath, 0o764)
            try:
                os.system(f'chown root:root {self.soundpath}')
                os.system(f'chmod 777 -R {self.soundpath}')
            except:
                print(f'Error:{e}')
        filename = self.data+".raw"
        filename = os.path.join(self.soundpath,filename)
        with open(filename, "wb") as out:
            out.write(self.response.audio_content)
        return os.path.basename(filename)


    def createvarify_Md5(self):
        checksum = hashlib.md5(self.textdata.encode()).hexdigest()
        file_1 = checksum+'.raw'
        self.makedir(self.soundpath)
        for root, dirs, files in os.walk(self.soundpath):
            if file_1 in files:
                #return_file = file_1.split('.')
                return ('Present', checksum)
            else:
                return ('Absent', checksum)
    
    def makedir(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)
