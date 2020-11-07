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
        os.mkdir(directory)

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

    index=1
    for vocabs in data.vocabularies:
        content+=f"{index}." + newLine
        for vocab in vocabs.definitions:
            content+=f"* {vocab.text.strip()} [{vocab.kk.strip()}] {vocab.pos.strip()} {vocab.content.strip()}"+newLine
            content+="- " + newLine
        index+=1
        content+=newLine
    return content

def getMessage(challengeId:int, studentNames:List[str])->Dict[str,str]:
    url=f"https://vtapi.voicetube.com/v2.1.1/zhTW/pronunciationChallenges/{challengeId}/comments?platform=Web&page[offset]=0&page[limit]=100&fetchMode=all"
    data=getWebContent(url)
    dicts={}
    data=students_from_dict(json.loads(data))
    data=data.data
    for datum in data:
        if datum.owner.display_name in studentNames:
            note=datum.content.replace("\t","")
            if len(note)>50:
                dicts[datum.owner.display_name]=note
        if len(dicts)==2: break
    return dicts


def main():
    checkFile()
    challengeId=getId()
    content=getContent(challengeId)
    studentsName=["Melody Tai","undefined"]
    data=getMessage(challengeId,studentsName)
    for name in studentsName:
        if name in data:
            content+="\n\n\n\n" + data[name]
            break
    with open(filepath, 'w',encoding='utf-8') as f:
        f.write(content)
    print(f"{filepath=}")
    print("finish")


if __name__ == '__main__':
    main()
    