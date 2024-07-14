#!/home/ahlborn/anaconda3/envs/gpd/bin/python3

import re
import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
import  datetime as dt



def replace_link (z):
    kla = [pos for pos, char in enumerate(z) if char == '['] 
    klz = [pos for pos, char in enumerate(z) if char == ']'] 
    if len(kla) > 0 :
        s = 0
        zn = z[0:kla[0]]
        for i in range(len(kla)):
            s = kla[i] + 1
            e = klz[i]
            e1 = len(z)
            Verweis = z[s:e]
            [text, nahn] = Verweis.split('#')
            html_link = "<a href=\"/Ahnentafel/C_{:d}.html\">{:s}</a>".format(int(nahn[1:]), text)
            zn += html_link + z[e+1:e1]

        return(zn)
    else:
        return(z)

def Datum_anpassen(datum):
       Gb = datum.strftime("%d.%m.%Y")
       return (Gb)
       
def printSubsInDelimiters(str): 
    regex = "\[(.*?)\]"
    matches = re.findall(regex, str) 
    for match in matches:
        print("---> match", match)
        (text, anr) = match.split("#A")
        print(text,anr)
        html_link = '<a href="A{:s}.html">{:s}</a>'.format(anr,text)
        print(html_link)
        str = str.replace(match, html_link)
        print(type(str), str)
    return(str)



css_file ="A.css"
facs_path = "/ahnbriefe/"

db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/ahnen'
db_connection = create_engine(db_connection_str)

jahr = 1955

                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()

q_ahnbriefe  = text("select * from ahnbriefe where year(adat)={:d}".format(jahr))
ahnbriefe =  pd.read_sql(q_ahnbriefe, con=db_connection)

q_anam  = text("select * from anam".format())
anam =  pd.read_sql(q_anam, con=db_connection)

print(ahnbriefe)
# write md File
Zielpfad = "/home/ahlborn/Documents/HUGO/Fam2/content/de/ahnen/".format()
fmname = "{:s}/Briefe_aus_{:d}.md".format(Zielpfad, jahr)
front_matter = '''
---
title: "Briefe aus dem Jahre {:d}" 
date: 2024-07-08
lastmod: 2024-06-15
tags: ["Familienhistorie"]
author: ["Karl Ahlborn"]
---
'''.format(jahr)

fm = open(fmname, 'w')
print(front_matter, file=fm)


Pfad = "/home1/Collections/Ahnbriefe/"
Verzeichnisse = {}
Leute = []
for i in os.listdir(Pfad):
    anrs = i[0:4]
    try:
        anr = int(anrs)
        Verzeichnisse.update ({anr: i})
    except:
        x = 1

#print(Verzeichnisse)


for i,v in ahnbriefe.iterrows():
    # convert odt to html
    anr = v.loc['anr']
    enr = v.loc['enr']
    brfnr = v.loc['brfnr']
    adatx = v.loc['adat']
    bemerkung = v.loc['bemerkung']
    anam_aktuell = anam.query('anr == @anr')
    print(anam_aktuell)
    Vorname = anam_aktuell['vornamen'].to_string(index=False).split(' ', 1)[0]
    Absender  = Vorname + " " + anam_aktuell['name'].to_string(index=False)
    enam_aktuell = anam.query('anr == @enr')
    print(Absender)
    Vorname = enam_aktuell['vornamen'].to_string(index=False).split(' ', 1)[0]
    Empfänger  = Vorname + " " + enam_aktuell['name'].to_string(index=False)
    adat = Datum_anpassen(adatx)
    tdatei = v.loc['tdatei']
    trans = Pfad + Verzeichnisse[anr]  + "/" +  tdatei
    Befehl = "soffice --convert-to 'txt:Text' {:s} --outdir textfiles".format(trans)
    print(Befehl)
    os.system(Befehl)
    Verschiebe = "mv textfiles/{:s}.txt neu.txt".format(tdatei[:-4])
    print(Verschiebe)
    os.system(Verschiebe)
    print("Ende")
    

    # write html File
    html_header = '''
<!DOCTYPE HTML><html>
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <title>Test Document</title>
   </head>
   <body>
      <link rel="stylesheet" href="{:s}">
         <div class="grid-container">
'''.format(css_file)

    Zielpfad = "/home/ahlborn/Documents/HUGO/Fam2/static/ahnbriefe"                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()

    fname = "{:s}/A{:04d}.html".format(Zielpfad, brfnr)
    with open(fname, 'w') as f:
        seite = 1
        facs_file ="facs_{:d}_{:d}-".format(anr,brfnr)
        print(html_header, file=f)
        html_newpage = '''
 <div class="grid-item"><img width="1200" src="{:s}{:s}{:d}.jpg"></div>
 <div class="grid-item">
'''.format(facs_path, facs_file, seite)
        print(html_newpage, file=f)
        Textdatei ="neu.txt"
        with open(Textdatei, 'r') as t:
            zeilen = t.readlines() 
        for z1 in zeilen:
            z = "<br>" + z1.rstrip('\n')
            if "#A" in z:
                z = replace_link(z)
            if "#newpage" in z:
                z = ""
                print("</div>")
                seite = seite + 1
                facs_file ="facs_{:d}_{:d}-".format(anr,brfnr)
                print(facs_file)
                html_newpage = '''
                </div>
                <div class="grid-item"><img width="1200" src="{:s}{:s}{:d}.jpg"></div>
                <div class="grid-item">                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()

                '''.format(facs_path, facs_file, seite)
                print(html_newpage, file=f)
                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()

            
            print(z, file=f)

    Text = "{:s} an {:s}  \n".format(Absender,Empfänger)
    try:
        Bemerkung = "{:s}  \n".format(bemerkung)
    except:
        Bemerkung = ""                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()

    Eintrag = "[{:}]( /ahnbriefe/A{:04d}.html  )\n\n".format(adat,brfnr)
    print(Text, Bemerkung, Eintrag, file=fm)
                #z = printSubsInDelimiters(z)
                #print(z)
                #exit()
