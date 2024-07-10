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
q_ahnbriefe  = text("select * from ahnbriefe".format())


anam   = pd.read_sql(q_anam, con=db_connection)
aleben = pd.read_sql(q_aleben, con=db_connection)
ahnbriefe = pd.read_sql(q_ahnbriefe, con=db_connection)

ahnbriefe['dat'] = pd.to_datetime(ahnbriefe['adat'], format='%d.%m.%Y', errors='coerce')
ahnbriefe['jahr'] = ahnbriefe['dat'].dt.year


#print (anam)
#print (aleben)
#print(ahnbriefe)

#print(ahnbriefe.dtypes)

#Jahre = range(1940, 1965)
Jahre = [1948, 1949]

for Jahr in Jahre:
    print("Erzeuge Briefliste für das Jahr {:d}".format(Jahr))
    Briefe = ahnbriefe.query('jahr == @Jahr')
    Originalpfad = "/home/ahlborn/Documents/Collection/Ahndaten/"
    FaksimilePfad = "/home/ahlborn/Documents/HUGO/Fam2/static/ahnbriefe/"
    xmlPfad = "/home/ahlborn/Documents/HUGO/python_tools/ahnbriefe/"


    for i,r in Briefe.iterrows():
        brfnr= r.iloc[0]
        anr = r.iloc[1]
        enr = r.iloc[4]
        adat = r.iloc[2]
        edat = r.iloc[4]
        bemerkung = r.iloc[7]
        OriginalFaksimile = r.iloc[5]
        OrigiinalTransskript = r.iloc[6]
        Faksimile = "{:s}facs_{:d}_{:d}".format(FaksimilePfad,anr,brfnr)
        xmlDatei = "{:s}A{:d}.xml".format(xmlPfad,brfnr)
        htmlDatei = "{:s}A{:d}.html".format(FaksimilePfad,brfnr)
        print("#konvertiere {:s} nach  {:s}".format(xmlDatei, htmlDatei))


        # java -jar saxon-he-10.3.jar -o:../../Fam2/static/ahnbriefe/A441.html ../../Fam2/static/ahnbriefe/A441.xml A78a.xsl 
        Befehl = "java -jar saxon-he-10.3.jar  -o:{:s} {:s} Konversion.xsl".format(htmlDatei, xmlDatei)
        print(Befehl)
