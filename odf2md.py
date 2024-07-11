#!/home/ahlborn/anaconda3/envs/gpd/bin/python3


import os
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine



css_file ="A.css"
facs_path = "/ahnbriefe/"

db_connection_str = 'mysql+pymysql://ahlborn:kalli@localhost/ahnen'
db_connection = create_engine(db_connection_str)


q_ahnbriefe  = text("select * from ahnbriefe where year(adat)=1955".format())
ahnbriefe =  pd.read_sql(q_ahnbriefe, con=db_connection)

print(ahnbriefe)


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
    brfnr = v.loc['brfnr']
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

    Zielpfad = "/home/ahlborn/Documents/HUGO/Fam2/static/ahnbriefe"
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
            if "#newpage" in z:
                z = ""
                print("</div>")
                seite = seite + 1
                facs_file ="facs_{:d}_{:d}-".format(anr,brfnr)
                print(facs_file)
                html_newpage = '''
                </div>
                <div class="grid-item"><img width="1200" src="{:s}{:s}{:d}.jpg"></div>
                <div class="grid-item">
                '''.format(facs_path, facs_file, seite)
                print(html_newpage, file=f)

            
            print(z, file=f)

