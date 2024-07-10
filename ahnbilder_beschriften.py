#!/home/ahlborn/anaconda3/envs/gpd/bin/python3


from sqlalchemy import text
import  datetime as dt
import pandas as pd
import numpy as np
import math
from sqlalchemy import create_engine
import sys
import colorsys
import re
from  pathlib import Path
from os import walk
import json

db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/ahnen'
db_connection = create_engine(db_connection_str)

q_anam   = text("select * from anam".format())
q_aleben = text("select * from aleben".format())


anam   = pd.read_sql(q_anam, con=db_connection)
aleben = pd.read_sql(q_aleben, con=db_connection)


print (anam)

print (aleben)

Bildverzeichnis = "/home/ahlborn/Documents/HUGO/Fam2/static/ahnbilder/"
Bilder = next(walk(Bildverzeichnis), (None, None, []))[2]  # [] if no file

Kinderbilder = {}

for Bild in Bilder:
    if Bild[0:1] == "e":
       start = 'e'
       end = '.'
       anr = int(Bild.split(start)[1].split(end)[0])
       Person = anam.query('anr == @anr')

       vnm = Person['vornamen'].to_string(index = False)
       nm  = Person['name'].to_string(index = False)
       # Geburtsdatum heraussuchen
       geb = aleben.query('anr == @anr and vorgnr == 1')
       Gb = geb['datum'].to_string(index=False)
       Tag = Gb[8:]
       Monat = Gb[5:7] 
       Jahr = Gb[:4]  
       GbD = Tag + "." + Monat + "." + Jahr  
       Gdtext = "* {:s}".format(GbD)
       Beschreibung = "{:s} {:s}\n{:s}".format(vnm,nm,Gdtext)
       Kinderbilder.update({anr : Beschreibung})


       meta = {"Title" : Beschreibung}
       meta_file = Bildverzeichnis + Bild + ".meta"
       with open(meta_file, "w") as outfile: 
         json.dump(meta, outfile)

       
print(Kinderbilder)
exit()



dias['dat'] = pd.to_datetime(dias['datum'], format='%d.%m.%Y', errors='coerce')
dias['jahr'] = dias['dat'].dt.year

Fotos = dias.join(Fotos.set_index('fid'), on='fid')


#Jahre = [1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999]
Jahre = [1993]

for jahr in Jahre:
    dj  = Fotos.query('jahr == @jahr')
    print(dj)
    for i,r in dj.iterrows():
        pfad     = r.iloc[9]
        fid      = r.iloc[7]
        datei      = r.iloc[10]
              
        try:           
            Datei = pfad + "/" + datei
            Befehl = "cp " + Datei + " /home1/Collections/HUGO/{:d}".format(jahr) +"/"
        except:
            Befehl = ""
            print("#ignore")

        print(Befehl)
      