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

db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/mrm'
db_connection = create_engine(db_connection_str)

q_F = text("select * from Fotos ".format())




Fotos = pd.read_sql(q_F, con=db_connection)

F = Fotos['path'].str.contains('Diasammmlung').any().sum()

print(F)


exit()


dias['dat'] = pd.to_datetime(dias['datum'], format='%d.%m.%Y', errors='coerce')
dias['jahr'] = dias['dat'].dt.year

Fotos = dias.join(Fotos.set_index('fid'), on='fid')


#Jahre = [1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999]
Jahre = [1992]

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
      