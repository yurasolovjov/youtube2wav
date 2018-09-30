from __future__ import unicode_literals

import youtube_dl
import json
import argparse
from glob import glob
import pickle
import os
import sys
import shutil
import termcolor
import requests
import plotly
import plotly.graph_objs as go
import json
import csv

# Ограничение на максимальное количество страниц
LIMIT_PAGE = int(10)

def makeWaveFilesList(catalogs):

    listWavFiles = list()

    for catalog in catalogs:
        catalog = catalog + "//*.wav"
        wavs = glob(catalog);
        for wav in wavs:
            listWavFiles.append(wav);

    return listWavFiles, len(listWavFiles)

def getListFiles(json_file, filter):

    listFiles = list()
    names = list()

    with open(json_file) as f:
        config = json.load(f)

        for data in config:
            name = str(data["name"]).lower()
            if(str(name).find(filter) >= 0):
                listFiles += data["positive_examples"]

    return listFiles

def main():

    mainfile = os.path.abspath(sys.modules['__main__'].__file__)
    t,h = os.path.split(mainfile)

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-s", "--search", help="Keyword for search", action="append", default=None, nargs="*")
    parser.add_argument("-o", "--out", help="Output catalog", default="../youtube_sound")
    parser.add_argument("-i", "--input",  help="Input file of ontology. JSON file", default=os.path.normpath(t + '//ontology//ontology.json'))
    parser.add_argument("-l", "--lim_page", help="Limit of page", default=LIMIT_PAGE)
    parser.add_argument("--histogram", help="Create histogram of classes AudioSet(Evaluate,balanced,unbalanced)", default=False, type=bool)
    parser.add_argument("--dataset", help="Dataset of AudioSet(Evaluate,balanced,unbalanced)")

    args = parser.parse_args()

    search_tokens = list()
    keywords = args.search
    lim_page_count = args.lim_page
    output = os.path.normpath(args.out)
    input = os.path.normpath(args.input)
    histogram = bool(args.histogram)
    audioset_file = str(args.dataset)

    if histogram == True:

        if not os.path.exists(input) or not os.path.exists(audioset_file):
            raise Exception("Can not found file")

        with open(audioset_file,'r') as fe:
            csv_data = csv.reader(fe)

            sx = list()

            with open(input) as f:
                data = json.load(f)

                for row in csv_data:

                    if row[0][0] == '#':
                        continue


                    classes = row[3:-1]

                    for cl in classes:
                        for dt in data:

                            cl = str(cl).strip().replace('"',"")

                            if cl == dt['id']:
                                sx.append(dt['name'])

                                # status_string = "append: "+str(row)
                                # color = "green"

                            # else:
                            #     for
                                # status_string = "not found: "+str(row)
                                # color = "red"

                            # print(termcolor.colored(status_string, color))

            data = [
                go.Histogram(
                    histfunc="count",
                    x=sx,
                    name="count"
                ),
            ]

            plotly.offline.plot({
                "data": data,
                "layout": go.Layout(title="Histogram")
            }, auto_open=True)

        return


    if not os.path.exists(output):
        os.makedirs(output)


    for keyword in keywords:
        fusion_keyword = str()
        for k in keyword:
            fusion_keyword += k + ' '

        if fusion_keyword[-1] == ' ':
            fusion_keyword = fusion_keyword[:-1]

        search_tokens.append(fusion_keyword)

    if not os.path.exists(output):
        os.makedirs(output)

    if search_tokens == None:
        raise Exception("Not found keywords")

    for keyword in search_tokens:

        keyword = str(keyword).lower()

        ls = getListFiles(input,keyword)

        output_catalog = os.path.normpath(output + "\\" + keyword)
        if not os.path.exists(output_catalog):
            os.makedirs(output_catalog)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.normpath(output_catalog +"\\"+ '%(title)s-%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }

        for data in ls:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([data])
            except:
                print("Can`t load file")
                continue

if __name__ == "__main__":
    main()