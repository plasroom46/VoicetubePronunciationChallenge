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
            challengeId=script.string.split('challengeId:')[1].split(',')[0].split("'")[1]
            if challengeId=='':
                challengeId=-1
            else:
                challengeId=int(challengeId)
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
            partOfSpeech=vocab.pos.strip()
            partOfSpeech=f'{partOfSpeech[:partOfSpeech.index(".")]}.)'
            content+=f"* {vocab.text.strip()} [{vocab.kk.strip()}] {partOfSpeech} {vocab.content.strip()}"+newLine
            content+="- " + newLine
            vocabCount+=1
        index+=1
        content+=newLine
    return content,vocabCount

def getMessage(challengeId:int, ids:List[str],vocabCount:int)->Dict[str,str]:
    url=f"https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/{challengeId}/comments?platform=Web&page[offset]=0&page[limit]=500&fetchMode=all"
    data=getWebContent(url)
    dicts={}
    data=students_from_dict(json.loads(data))
    data=data.data
    for datum in data:
        if datum.owner.id in ids:
            note=datum.content.replace("\t","")
            if len(note)>vocabCount*10:
                dicts[datum.owner.user_name]=note
                break
    return dicts


def main():
    checkFile()
    challengeId=getId()
    if challengeId==-1:
        print(f'The date {date} is not recorded')
        sys.exit()
    content,vocabCount=getContent(challengeId)

    # hostDisplaynames=["Ashley","Selina","Ken Miao","Annie Huang","Wen","Doris","Minjane"]
    hostIds=[1958356,3981877,3791759,4030764,4209610,4030768,4034826]
    # displaynames=["Melody Tai","undefined","Emma","Wen Tsai"]
    ids=[545319,1352160,1895762,1958505]
    hostIds.extend(ids)
    data=getMessage(challengeId,hostIds,vocabCount)
    for key in data.keys():
        content+="\n\n\n\n" + data[key]
        break
    with open(filepath, 'w',encoding='utf-8') as f:
        f.write(content)
    print(f"{filepath=}")
    print("finish")


if __name__ == '__main__':
    main()
    