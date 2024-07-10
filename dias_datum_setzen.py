#!/home/ahlborn/anaconda3/envs/gpd/bin/python3


from sqlalchemy import text
import  datetime as dt
import pandas as pd
import numpy as np
import math
from sqlalchemy import create_engine
import sys
import colorsys


db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/mrm'
db_connection = create_engine(db_connection_str)


Jahr = 1997



q_dias = text("select * from dias".format())
dias = pd.read_sql(q_dias, con=db_connection)
q_Fotos = text("select * from Fotos".format())
Fotos = pd.read_sql(q_Fotos, con=db_connection)


dias['dat'] = pd.to_datetime(dias['datum'], format='%d.%m.%Y')

t1 = dias.sort_values(by='dat')

tkombi = dias.join(Fotos.set_index('fid'), on='fid')

MB  = tkombi.query('jahr == 1997')



for i,r in MB.iterrows():
    datum = r['datum']
    ort = r['ort']
    person = r['person']
    text = r['text']
    datei = r['datei']
    ZielPfad = "/home/ahlborn/Documents/HUGO/Familiengeschichte/content/de/ahnen/Dias_{:d}/Dias_{:d}/".format(Jahr, Jahr)
    try:
        Datei = ZielPfad + "s_" + datei + '.meta'
    except:
        print('# konnte kein meta file erzeugen')
    ka = '{'
    kz = '}'
    #Beschreibung = '{:}{:s} {:s} {:s}'.format(datum,person[0:20],ort[0:20],text[0:20])
    Beschreibung = '{:}\\n {:s}\\n {:s}\\n {:s}'.format(datum, ort, person, text)
    B1 = Beschreibung.replace ("'", "")
    B2 = B1.replace ('"', '')
    dp = ":"
    print (Datei)
    with open(Datei, 'w') as f:
        print("{", file=f)
        print("\"Tags\" {:s} [\"Familie\"],".format(dp), file=f)
        print("\"Title\" {:s} \"{:s}\",".format(dp, B2), file=f)
        print("\"Rating\" {:s} [\"RG\"]".format(dp), file=f)
        print("}", file=f)
    f.close()

    