#!/home/ahlborn/anaconda3/envs/gpd/bin/python3

# erzeuge eine html Visitenkarte für eine anr

#    vv    mv         vm    mm
#       v                 m
#                k
# e1 e2 e3 e4....
#
#

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



anr = int(sys.argv[1])


def Datum_anpassen(datum):
       Gb = datum.strftime("%d.%m.%Y")
       return (Gb)
       


def erzeuge_html ( Ahnkarte):
    Person = Ahnkarte['P']



db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/ahnen'
db_connection = create_engine(db_connection_str)

q_anam   = text("select * from anam".format())
q_aleben = text("select * from aleben".format())
q_alink  = text("select * from alink".format())


anam   = pd.read_sql(q_anam, con=db_connection)
aleben = pd.read_sql(q_aleben, con=db_connection)
alink = pd.read_sql(q_alink, con=db_connection)

aleben['dat'] = pd.to_datetime(aleben['datum'], format='%d.%m.%Y', errors='coerce')



def Kinder (anr, g):
    if g == 'm':
        Kinder = alink.query("vater == @anr")
    if g == 'w':
        Kinder = alink.query("mutter == @anr")

    Kids = []
    for i,r in Kinder.iterrows():
        kanr = r.loc['anr']
        Kids.append(P_Info(kanr))

    return (Kids)


def P_Info (anr):
    K_geb=""
    info = {}
    K  = anam.query('anr == @anr')
    for i,r in K.iterrows():
        K_n = r.loc['name']
        K_v = r.loc['vornamen']
        K_g = r.loc['geschlecht']
    Leben = aleben.query("anr == @anr")
    for i,r in Leben.iterrows():
        L_v = r.loc['vorgnr']
        if L_v == 1:
            K_gebr = r['datum']
            K_geb = Datum_anpassen(K_gebr)
    Eltern = alink.query("anr == @anr")
    for i,r in Eltern.iterrows():
        V = r.loc['vater']
        M = r.loc['mutter']


    info.update({'anr': anr })
    info.update({'Name': K_n })
    info.update({'Vorname': K_v })
    info.update({'geschlecht': K_g })
    info.update({'Vater': V })
    info.update({'Mutter': M })
    info.update({'geb': K_geb })
    return (info)


P  = P_Info(anr)
V  = P_Info(P['Vater'])
M  = P_Info(P['Mutter'])
VV = P_Info(V['Vater'])
MV = P_Info(V['Mutter'])
VM = P_Info(M['Vater'])
MM = P_Info(M['Mutter'])

Kids = Kinder(anr, P['geschlecht'])

Ahnkarte = {'P':P, 'V': V, 'M': M, 'VV': VV, 'MV': MV, 'VM':VM, 'MM': MM, 'Kinder':Kids}


erzeuge_html(Ahnkarte)


kopf = '''
<!DOCTYPE HTML><html>
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <title>Test Document</title>
   </head>
   <body>
      <link rel="stylesheet" href="Ahnkarte.css">

'''

print(kopf)


VV_Text = "{:s} {:s}<br>* {:}".format(VV['Vorname'],VV['Name'], VV['geb'])
VV_Bild = "../ahnbilder/g{:d}.jpg".format(VV['anr'])

MV_Text = "{:s} {:s}<br>* {:}".format(VV['Vorname'],MV['Name'], MV['geb'])
MV_Bild = "../ahnbilder/g{:d}.jpg".format(MV['anr'])

VM_Text = "{:s} {:s}<br>* {:}".format(VV['Vorname'],VM['Name'], VM['geb'])
VM_Bild = "../ahnbilder/g{:d}.jpg".format(VM['anr'])

MM_Text = "{:s} {:s}<br>* {:}".format(VV['Vorname'],MM['Name'], MM['geb'])
MM_Bild = "../ahnbilder/g{:d}.jpg".format(MM['anr'])


GrossEltern = '''
<div class="Grosseltern">
    <div class="box a">
        {:s}
        <img src="{:s}" width="100%">
    </div>
    <div class="box b">
         {:s}
        <img src="{:s}" width="100%">
    </div>
    <div class="box leer"></div>
    <div class="box d">
         {:s}
        <img src="{:s}" width="100%">
     </div>
    <div class="box e">
         {:s}
        <img src="{:s}" width="100%">
     </div>
  </div>
'''.format(VV_Text, VV_Bild, MV_Text, MV_Bild, VM_Text, VM_Bild, MM_Text, MM_Bild)

print(GrossEltern)


V_Text = "{:s} {:s}<br>* {:}".format(V['Vorname'],V['Name'], V['geb'])
V_Bild = "../ahnbilder/e{:d}.jpg".format(V['anr'])

M_Text = "{:s} {:s}<br>* {:}".format(M['Vorname'],M['Name'], M['geb'])
M_Bild = "../ahnbilder/e{:d}.jpg".format(M['anr'])




Eltern = '''
<br>

  <div class="Eltern">
    <div class="box leer"></div>
    <div class="box b">
        {:s}
        <img src="{:s}" width="100%">
    </div>
    <div class="box leer"></div>
    <div class="box b">
        {:s}
        <img src="{:s}" width="100%">
    </div>
 </div>
'''.format(V_Text, V_Bild, M_Text, M_Bild)

print(Eltern)



P_Text = "{:s} {:s}<br>* {:}".format(P['Vorname'],P['Name'], P['geb'])
P_Bild = "../ahnbilder/k{:d}.jpg".format(P['anr'])

Person = '''
<br>
   <div class="Person">
        <div class="box leer"></div>
        <div class="box b">
        {:s} 
        <img src="{:s}" width="100%">
         </div>
 </div>
'''.format(P_Text, P_Bild)

print (Person)



Kids = Ahnkarte['Kinder']
print('''<div class="Kind">''')
 
for kid in Kids:
    k_Text = "{:s} {:s}<br>* {:}".format(kid['Vorname'],kid['Name'], kid['geb'])
    k_Bild = "../ahnbilder/k{:d}.jpg".format(kid['anr'])


    Kind='''
        <div class="box b">
           {:s}
           <img src="{:s}" width="100%">
        </div>
    '''.format(k_Text, k_Bild)
    print(Kind)
print("</div>")
