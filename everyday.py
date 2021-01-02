from typing import Dict
import urllib.request as req
import json
import bs4
from datetime import date,timedelta
import os
import sys
import argparse
from Models.Host import *
from Models.Students import *


parser = argparse.ArgumentParser(description='Get Setence and Vocabs')
parser.add_argument('--day',nargs='?', type=int, default=0, help='get note count today')
args = parser.parse_args()


date=date.today()
date=date+timedelta(days=args.day)


directory=os.path.join(date.strftime("%Y"),date.strftime("%Y-%m"))
filename=f"{date.strftime('%Y%m%d')}-1.txt"
filepath=os.path.join(directory,filename)



def getWebContent(url:str)->str:
    request=req.Request(url,headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
})
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    return data


def checkFile():
    if not os.path.isdir(directory):
        os.makedirs(directory)

    if os.path.exists(filepath):
        print(f"檔案已存在：{filepath}")
        sys.exit()


# get id
def getId()->int:
    url=f"https://tw.voicetube.com/everyday/{date.strftime('%Y%m%d')}"

    data=getWebContent(url)

    root=bs4.BeautifulSoup(data,"html.parser")
    challengeId=1
    scripts=root.find_all("script")

    for script in scripts:
        if(script.string and "challengeId" in script.string):
            challengeId=int(script.string.split('challengeId:')[1].split(',')[0].split("'")[1])
            break

    return challengeId

# 句子
def getContent(challengeId:int)->str:
    url=f"https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/{challengeId}?platform=Web&userId="

    data=getWebContent(url)

    content=""
    data=host_from_dict(json.loads(data))

    data=data.data

    newLine="\r\n"

    content+= data.content.strip()+newLine*2+data.translated_content.strip()+newLine*2+data.title.strip()+newLine*3

    vocabCount=0
    index=1
    for vocabs in data.vocabularies:
        content+=f"{index}." + newLine
        for vocab in vocabs.definitions:
            partOfSpeech=vocab.pos.strip().replace("..",".")
            content+=f"* {vocab.text.strip()} [{vocab.kk.strip()}] {partOfSpeech} {vocab.content.strip()}"+newLine
            content+="- " + newLine
            vocabCount+=1
        index+=1
        content+=newLine
    return content,vocabCount

def getMessage(challengeId:int, usernames:List[str],vocabCount:int)->Dict[str,str]:
    url=f"https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/{challengeId}/comments?platform=Web&page[offset]=0&page[limit]=500&fetchMode=all"
    data=getWebContent(url)
    dicts={}
    data=students_from_dict(json.loads(data))
    data=data.data
    for datum in data:
        if datum.owner.user_name in usernames:
            note=datum.content.replace("\t","")
            if len(note)>vocabCount*10:
                dicts[datum.owner.user_name]=note
        if len(dicts)==len(usernames): break
    return dicts


def main():
    checkFile()
    challengeId=getId()
    content,vocabCount=getContent(challengeId)
    # displaynames=["Melody Tai","undefined","Emma","Wen Tsai"]
    usernames=["10205256245518930","gotraveltoworld","1264052757005391","1009638965715348"]
    data=getMessage(challengeId,usernames,vocabCount)
    for name in usernames:
        if name in data:
            content+="\n\n\n\n" + data[name]
            break
    with open(filepath, 'w',encoding='utf-8') as f:
        f.write(content)
    print(f"{filepath=}")
    print("finish")


if __name__ == '__main__':
    main()
    