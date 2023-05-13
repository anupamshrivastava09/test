from typing import Optional, List
from fastapi import FastAPI,Response,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from configparser import ConfigParser
from google_tts import *
from azure_tts import *
from awspolly_tts import *
import uvicorn
import json

configure = ConfigParser()
app = FastAPI()


class Item(BaseModel):
    clientname: str
    rate : Optional[str] = None
    pitch : Optional[str] = None
    volume : Optional[str] = None
    lang : str
    data : List[str]

class Message(BaseModel):
    message: str

@app.post("/tts/")
async def create_tts(item : Item):
    configure.read("config.ini")
    sections = configure.sections()
    try:
         getname = item.clientname
         getname = getname.upper()
    except Exception as e :
         return JSONResponse(status_code=400,content={"status": "failure", "message": f"Bad Request - Client Name is Missing"})
    if getname not in sections:
         return JSONResponse(status_code=401,content={"status": "failure", "message": f"Given Client Name {item.clientname} is Unauthorized"})
    getname = getname.upper()
    resp=[]
    language=item.lang
    language=language[0:3]
    lang = language.lower()

    lang_data=configure[getname]["lang"]
    
    if lang == "":
         return JSONResponse(status_code=404,content={"status": "failure", "message": f"Given language is not found in Configurations"})
    
    lang_part=json.loads(lang_data)
    try:
        lang_code = lang_part[lang]['lang_code']
    except Exception as e :
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"Language Code for {lang} is not found in configuration"})
    
    speaker_voice = lang_part[lang]['speaker_voice']
    
    gender = lang_part[lang]['gender']
    
    if lang_code == "":
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"lang code is not found against {lang} langauge in Configurations"})
    if speaker_voice == "":
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"Speaker Voice is not found against {lang} langauge in Configurations"})
    if gender == "":
        #raise HTTPException(status_code=404,content={"status": "failure", "message": f"Gender is not found against {lang} languague in Configurations"})
        return JSONResponse(status_code=404, content={"status": "failure","message": f"Gender is not found against {lang} languague in Configurations"})

    if  item.rate :
        rate=item.rate
        rate=rate.strip('"')
    else :
        rate=configure[getname]['rate']
        rate=rate.strip('"')
    if rate == "":
        return JSONResponse(status_code=404, content={"status": "failure","message": f"Speaking rate of the text is not defined in Configurations"})
    if item.pitch :
        pitch=item.pitch
        pitch=pitch.strip('"')
    else :
        pitch=configure[getname]['pitch']
        pitch=pitch.strip('"')
    if pitch == "":
        return JSONResponse(status_code=404, content={"status": "failure","message": f"Baseline pitch for the text is not defined in Configurations"})
    if item.volume :
        volume=item.volume
        volume=volume.strip('"')
    else :
        volume=configure[getname]['volume']
        #print(volume)
        volume=volume.strip('"')
    if volume == "":
        return JSONResponse(status_code=404, content={"status": "failure","message": f"volume level of the speaking voice is not defined in Configurations"})
    data_len=len(item.data)
    tts = configure[getname]['tts_type']
    tts=tts.strip('"')
    if tts == "" :
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"TTS type is not defined"})
    
    voicepath = configure[getname]['voicepath']
    voicepath = voicepath.strip('"')
    #print(f"{type(voicepath)} and {type(getname)}")
    tts_voicepath = voicepath+getname
    if tts_voicepath == "" :
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"TTS Voice path  is not defined"})
    
    #print(configure[getname]"secret_path"])
    try :
        key=configure[getname]["secret_path"]
        key=key.strip('"')
    except Exception as e:
        #print(e)
        return JSONResponse(status_code=404,content={"status": "failure", "message": f"{e} Id is not found in Configurations"})
    
    if tts == "awspolly_tts":
        try :
            #aws_resp = AWSTTS(profile,region,lang_code,speaker_voice,gender,tts_voicepath,rate,pitch,volume,item.data)
            aws_resp = AWSTTS(key,lang_code,speaker_voice,gender,tts_voicepath,rate,pitch,volume,item.data)
            resp = aws_resp.tts()
        except Exception as e:
            #raise HTTPException(status_code=404,detail={"status": "failure", "message": f"{e}"})
            return JSONResponse(status_code=404, content={"status": "failure","message": f"{e}"})
    
    elif tts == "azure_tts":
    
        try:
            azure_resp=azure(key,lang_code,speaker_voice,gender,tts_voicepath,rate,pitch,volume,item.data)
            resp=azure_resp.atts()
        except Exception as e :
            return JSONResponse(status_code=404, content={"status": "failure","message": f"{e}"})
        
    elif tts == "google_tts":
        
        try :
            #gtts=GCPT2S(key_path,lang_code,speaker_voice,gender,tts_voicepath,rate,pitch,volume,item.data)
            gtts=GCPT2S(key,lang_code,speaker_voice,gender,tts_voicepath,rate,pitch,volume,item.data)
            resp=gtts.data_analyse() 
        except Exception as e :
            return JSONResponse(status_code=404, content={"status": "failure","message": f"{e}"})
    
    
    if len(resp) == 0:
        return JSONResponse(status_code=404, content={"status": "failure","message": "Data not found"})
    else :
        return JSONResponse(status_code=200, content={"status": "success","message": "Data Found","VoiceData":resp})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1")
