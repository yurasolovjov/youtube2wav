from __future__ import unicode_literals
import youtube_dl
import json


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def getListFiles(json_file, filter):

    listFiles = list()
    names = list()

    with open(json_file) as f:
        config = json.load(f)

        for data in config:
            name = data["name"]

            if name == filter:
                return  data["positive_examples"]

def main():

    ls = getListFiles('D:\\repo\\ontology\\ontology.json',"Glass")

    for data in ls:
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
                ydl.download([data])
        except:
            print("Can`t load file")
            continue

if __name__ == "__main__":
    main()