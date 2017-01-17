# Modul1

Vom detalia modulele :

Atentie: inainte de a compila botul vor aparea probleme de dependinte pe care le veti rezolva cu pip, vor exista si probleme de dependinta pentru nltk, pentru tagger si words si inca cateva, acestea se pot dezolva prin inserarea in cod a nltk.download() ce deschide o fereastra unde sa se selecteze dependintele, nu e greu de cautat si instalat.

# Modul 3

Este integrat modulul 3, atentie, este modificat fata de repository-ul de aici: https://github.com/cipriancus/Modul3
Trebuie sa fie Stanford NLP instalat in D:\Stanford, in main.py din Modulul 3 se poate observa

os.environ["JAVAHOME"] = "C:\Program Files\Java\jre1.8.0_111"
os.environ["STANFORD_PARSER"] = "D:\Stanford\stanford-parser-full-2015-12-09"
os.environ["STANFORD_MODELS"] = "D:\Stanford\stanford-parser-full-2015-12-09"

Ori se modifica directoarele, ori se pune la path-ul respectiv.

Stanford link : http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip

Ca sa se execute se intra cu cmd in folderul respectiv si se executa python main.py

Sunt necesare si alte componente ce se vor instala cu pip cand vor aparea ca erori, e usor si intuitiv

#Modul 2

Se iau datele de la modulul 2 : https://github.com/cipriancus/Modul2/tree/master

Se pune arhiva undeva. Modulul compileaza numai cu python 2.7 asa ca mare grija cu ce il rulati.
Sigur vor aparea erori, ca nu gaseste ceva, se vor instala cu pip, ca nu e greu.
Se porneste cu consola si se deschide cu python 2.7 finalserv.py
Interogarile pentru server sunt in database_client.py din modulul 1
