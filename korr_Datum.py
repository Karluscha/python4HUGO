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
import glob

db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/mrm'
db_connection = create_engine(db_connection_str)

#q_F = text("select * from Fotos ".format())
#Fotos = pd.read_sql(q_F, con=db_connection)
#F = Fotos['path'].str.contains('Diasammmlung').any().sum()
#print(F)



Verzeichnisse = ['Dias_1986']
pfad = "/home/ahlborn/Documents/HUGO/Familiengeschichte/content/de/ahnen"
for V in Verzeichnisse:
    meta_Verzeichnis = "{:s}/{:s}".format(pfad, V) 
    Bilder = "{:s}/{:s}".format(meta_Verzeichnis, V)

    print(Bilder)
    Meta_Files = glob.glob("{:s}/*meta".format(Bilder))
    print(Meta_Files)

