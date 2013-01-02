#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import argparse

class Member:
    """Describes a member"""

    def __init__(self, labels, values):
        if len(labels) != len(values):
            raise Exception("label and values are not of the same length: %s" % (" ".join(values)))

        self.properties = dict(zip(labels, values))

def sortGroup(primary, other):
    sortorder = [("avdelning", ["avdelning"]),
                 ("förnamn", ["förnamn"]),
                 ("efternamn", ["efternamn"])]

    for tup in sortorder:
        source = tup[0]
        for target in tup[1]:
            if (not primary.properties[source] or
                not other.properties[target]):
                continue

            if (primary.properties[source].lower() <
                other.properties[target].lower()):
                return -1
            if (primary.properties[source].lower() >
                other.properties[target].lower()):
                return 1
    return 0

def sortAddress(primary, other):
    sortorder = [("postnr", ["postnr"]),
                 ("adress, rad 1", ["adress, rad 1", "adress, rad 2", "adress, rad 3"]),
                 ("adress, rad 2", ["adress, rad 1", "adress, rad 3"]),
                 ("adress, rad 3", ["addres, rad 3"]),
                 ("efternamn", ["efternamn"]),
                 ("förnamn", ["förnamn"])]

    for tup in sortorder:
        source = tup[0]
        for target in tup[1]:
            if (not primary.properties[source] or
                not other.properties[target]):
                continue

            if (primary.properties[source].lower() <
                other.properties[target].lower()):
                return -1
            if (primary.properties[source].lower() >
                other.properties[target].lower()):
                return 1
    return 0

def cleanPhones(labels, members):
    phoneLabels = []

    # find all labels that contains "telefon" or "mobil"

    for label in labels:
        if ("telefon" in label or
            "mobil" in label):
            phoneLabels.append(label)

    for member in members:
        for label in phoneLabels:
            if member.properties[label]:
                p = member.properties[label]
                if p.startswith("46 "):
                    member.properties[label] = p[3:]

def mergePhones(labels, members):
    phoneLabels = []

    # find all labels that contains "telefon" or "mobil"
    # but not "kårlokal", "distriktskansli"

    for label in labels:
        if (("telefon" in label or
             "mobil" in label) and
            not "kårlokal" in label and
            not "distriktskansli" in label):
            phoneLabels.append(label)

    totPhone = "totaltelefon"
    labels.insert(0, totPhone)

    for member in members:
        member.properties[totPhone] = ""
        for label in phoneLabels:
            if member.properties[label]:
                p = member.properties[label]
                if not member.properties[totPhone]:
                    member.properties[totPhone] = (label + ": " +
                                                   p)
                else:
                    member.properties[totPhone] = (member.properties[totPhone]
                                                   + ", " +
                                                   label + ": " +
                                                   p)

def printTex(labels, members):
    """Output latEx formated labels"""

    print '''
\\documentclass[a4paper,12pt]{article}

\usepackage[utf8]{inputenc} % utf8
\\usepackage[T1]{fontenc}    %enable good characters
\\usepackage[swedish]{babel} %setup language
\\usepackage{palatino}
\\usepackage{graphicx}

%a4 - 210 x 297 mm
%ruta: 70 x 37 mm

%no headers
\\thispagestyle{empty}

%there seems to be a default "margin" of 1 inch
%compensate...
\\setlength{\\topmargin}{-1in}
\\setlength{\\rightmargin}{0in}
\\setlength{\\leftmargin}{0in}
\\setlength{\\evensidemargin}{0in}
%default margin is 1 inch + oddsidemargin
%compensate...
\\setlength{\\oddsidemargin}{-1in}

%paragraphs are not indented
\\setlength{\\parindent}{0mm}

\\setlength{\\headheight}{0mm}

%set text height and width for a4 paper
\\setlength{\\textwidth}{210mm}
\\setlength{\\textheight}{297mm}

%there is a 5 mm margin between top of the page and the first sticker
\\setlength{\\headsep}{5mm}

%set unitlenght to 1mm, this makes it a little bit
%easier to work in the picture environment
\\setlength{\\unitlength}{1mm}


%DO NOT put empty lines in the picture environment, it will screw thingies up
\\newcommand{\\addresssticker}[3]{
%one sticker is 70 x 36 mm
\\begin{picture}(70,36)
%note that the coordianates is relative to the lower
%left corner
%enable next line to put a frame around the sticker
%  \\put(1,1){\\framebox(70,36){}} 
%makebox(x-pos, ypos)[adjust left]{content}
  \\put(10,5){\\makebox(65,15)[l]{\\ascaledfont #3}}
  \\put(10,12){\\makebox(65,15)[l]{\\ascaledfont #2}}
  \\put(10,19){\\makebox(65,15)[l]{\\ascaledfont #1}}
\\end{picture}
}

%DO NOT put empty lines in the picture environment, it will screw thingies up
\\newcommand{\\addressstickerext}[4]{
%one sticker is 70 x 36 mm
\\begin{picture}(70,36)
%note that the coordianates is relative to the lower
%left corner
%enable next line to put a frame around the sticker
%  \\put(1,1){\\framebox(70,36){}} 
%makebox(x-pos, ypos)[adjust left]{content}
  \\put(10,0){\\makebox(65,15)[l]{\\ascaledfont #4}}
  \\put(10,8){\\makebox(65,15)[l]{\\ascaledfont #3}}
  \\put(10,15){\\makebox(65,15)[l]{\\ascaledfont #2}}
  \\put(10,22){\\makebox(65,15)[l]{\\ascaledfont #1}}
\\end{picture}
}



%
% Document starts here.
%
\\begin{document}

%scale font, call it \ascaledfont
%this could probably be done in another way
%adjust number to get a font of the right size
\\newfont{\\ascaledfont}{pncr scaled 1300}
'''

    for member in members:
        if not member.properties["c/o (ange c/o i rutan)"]:
            if (member.properties["land"].lower() ==
                "sverige"):
                print ("\\addresssticker{%s %s}{%s}{%s %s}" %
                       (member.properties["förnamn"],
                        member.properties["efternamn"],
                        member.properties["adress, rad 1"],
                        member.properties["postnr"],
                        member.properties["postort"]))
            else:
                print ("\\addressstickerext{%s %s}{%s}{%s %s}{%s}" %
                       (member.properties["förnamn"],
                        member.properties["efternamn"],
                        member.properties["adress, rad 1"],
                        member.properties["postnr"],
                        member.properties["postort"],
                        member.properties["land"]))
        else:
            if (member.properties["land"].lower() ==
                "sverige"):
                print ("\\addressstickerext{%s %s}{%s}{%s}{%s %s}" %
                       (member.properties["förnamn"],
                        member.properties["efternamn"],
                        member.properties["c/o (ange c/o i rutan)"],
                        member.properties["adress, rad 1"],
                        member.properties["postnr"],
                        member.properties["postort"]))
            else:
                raise Exception("Case not handled!")

    print '''
\\end{document}
'''

if __name__ == "__main__":
    labels = []
    members = []
    inputFile = None

    parser = argparse.ArgumentParser(description='Scoutnets little helper.')
    parser.add_argument('-c', dest='cleanPhone', action='store_true', default=False, help='Remove country prefix from phone numbers if "46 "')
    parser.add_argument('-g', dest='groupSort', action='store_true', default=False, help='Reorder according to groups-name')
    parser.add_argument('-i', dest='inputFile', action='store', help='Set input file name', required=True)
    parser.add_argument('-o', dest='outputFile', action='store', default='output.csv',help='Set output file name')
    parser.add_argument('-p', dest='mergePhone', action='store_true', default=False, help='Merge phone-numbers')
    parser.add_argument('-s', dest='sort', action='store_true', default=False, help='Sort input file according to address-name')
    parser.add_argument('-t', dest='tex', action='store_true', default=False, help='Generate LaTEX output for labels, will be printed to standard out')

    options = parser.parse_args()

    inputFile = open(options.inputFile)

    if inputFile is None:
        raise Exception("Please provide valid input file")

    memcsv = csv.reader(inputFile, delimiter=",")

    labels = memcsv.next()
    labels = map(lambda x:x.lower(), labels)

    for line in memcsv:
        members.append(Member(labels,line))

    inputFile.close()

    if options.cleanPhone:
        cleanPhones(labels, members)

    if options.mergePhone:
        mergePhones(labels, members)

    if options.sort:
        members = sorted(members, cmp=sortAddress)

    if options.groupSort:
        members = sorted(members, cmp=sortGroup)

    # Finally the output
    if options.tex:
        printTex(labels, members)
    else:
        outputFile = open(options.outputFile, 'w')
        if outputFile is None:
            raise Exception("Failed to create output file %s" % (options.outputFile))

        outputFile.write('"' + '","'.join(labels) + '"\n')
        for mem in members:
            outputFile.write('"' + '","'.join(map(lambda x: mem.properties[x], labels)) + '"\n')

        outputFile.close()



