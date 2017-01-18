# Modul1

SITE: http://b4bot.site/chat se poate folosi aici

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

#Contributii:
Asofiei Florina Cosmina 

- conceput structura preliminara a robotului si scenariul general de utilizare(https://b4bot.site/team1)
- integrat/modificat modul emotii, taxonomie care identifica emotiile in fraza userului si subiectele despre care vorbeste
- scheletul robotului(modul cum pune intrebari, cand da raspunsuri, cum se foloseste de unele module)
- ajutata la crearea unui robot cu retea neuronala recurenta --> esuat
- research nlg, instalat/testat peste 10 module(cele care faceau o constructie simpla nu se potriveau cerintelor, cele mai avansate nu aveau versiuni compatibile cu OS-urile noastre)
- integrat modulul 3 cu modulul 1(request-uri la modulul 3, corectat conexiunea prin socket)
- antrenat modulul de invatare automata(cu parti din corpusul de dialog din filme de la cornell)
- integrat modulul de invatare automata(cu celelalte functii de la modulul 1)
- asistenta echipei de test
- ajutor pentru crearea si implementarea unor interfete pentru adaptoarele logice, stocare si baza de date
- implementarea stocarii --> folder storage --> jsonfile, storage_adapter
- implementarea utilitarelor pentru text utils.py
- crearea si structurarea unui corpus pentru robot
- crearea unui adaptor pentru input, clasa generala --> input_adapter.py si implementarii input_adapter.py, care transforma diverse obiecte intr-un obiect Statement
- modelarea unui "statement" ca o clasa --> statement.py
- descarcat si integrat Cognitive-LUIS(ulterior am gasit un modul mai bun)

Serediuc Constantin

- construit api pentru interactiunea backend si site;  
- adaugat testele in interfata 
- construit interfata chatbot(html+css)
- ajutat integrare modul 1 cu 3 si 4
- desenat diagrama de clase, use-case pentru afisarea in site
- asistenta echipei de test
- integrare flask in robot ( modul web de comunicare )
- ajutor pentru crearea unor interfete pentru adaptoarele logice, stocare si baza de date
- descarcat si integrat Cognitive-LUIS(ulterior am gasit un modul mai bun)
- crearea si structurarea unui corpus pentru robot


Onutu Codrin Stefan

- diagrama de use-case (cu interactiune om-aplicatie, detaliata pe module)
- stabilit conventiile de comunicare modul1-modul2, modul1-modul3
- implementarea unui mecanism de stocare a sesiunii pentru tratarea cazurilor in care utilizatorul a mai pus aceeasi intrebare, cu stocarea emotiilor, intrebarilor si raspunsurilor pe parcurs ( folderul sessions din modul 1 )
- ajutor pentru crearea si implementarea unor interfete pentru adaptoarele logice, stocare si baza de date
- crearea si structurarea unui corpus pentru robot --> corpus.py
- modelarea raspunsului ca o clasa response.py


Cernescu Stefan

- research pentru nlg
- implementarea modului emotii, folder model--> comparisons.py-->sentiment_comparison
- integrarea modulului 1 cu serverul de la modulul 3
- modificari in serverul de la modulul 3 pt a raspunde mai bine la cerinte
- implementarea si research pentru un Trainer, clasa trainers.py
- implementarea utilitarelor pentru text utils.py
- crearea si structurarea unui corpus pentru robot
- definirea unui adaptor ca o clasa parinte adapters-->adapter.py
- creat robot cu retea neuronala recurenta --> esuat


Cusmuliuc Ciprian-Gabriel

- coordonarea echipelor si stabilirea de comun acord asupra unor interfete de comunicare
- crearea platformelor de versionare
- research pentru robot, tipuri de roboti, metode, tehnologii
- creat robot cu retea neuronala recurenta --> esuat
- integrarea tuturor modulelor si supervizarea activitatii acestor
- comunicarea si suport tehnic pentru toate modulele, inclusiv echipa de testare ( ce a necesitat ajutor pentru configurare si instalare )
- oferirea de explicatii necesare pentru module ce nu au inteles problema propusa, a interfetelor de comunicare, ajutarea rezolvarii
  problemelor tehnice ce le-au intampinat sau a ideilor de design posibile pentru pagina web si a interfetei de comunicare chat
- lansarea aplicatiei, ce include toate modulele pe un server dedicat si asigurarea functionaliataii neintrerupte a robotului, proces ce a implicat cateva ore de configurare pe Linux
- repararea bug-urilor semnalate de echipa de testare
- crearea si structurarea unui corpus pentru robot
- intelegerea functionalitatii celorlalte module pentru a le putea apela intr-o maniera corecta
- conceput structura preliminara a robotului si scenariul general de utilizare(https://b4bot.site/team1)
- integrat/modificat modul emotii, taxonomie care identifica emotiile in fraza userului si subiectele despre care vorbeste
- scheletul robotului(modul cum pune intrebari, cand da raspunsuri, cum se foloseste de unele module)
- crearea si implementarea unor interfete pentru adaptoarele logice, stocare si baza de date
- implementare client pentru baza de date : database_client
- implementarea unei cozi pentru sesiune queues.py si a selectarii unor raspunsuri response_selection.py
- crearea si structurarea unui corpus pentru robot --> corpus.py
- implementarea mecanismelor de decizie ale robotului, adaptoarele logice si research in aceasta zona, module implementate:
	-best_match.py --> selectarea raspunsului din corpus cel mai bun
	-entity_adapter --> interogarea si cautarea de entitati in input si mai apoi interogarea bazei de date pentru a oferi un raspuns inexistent local
	-joke_adapter --> stabilirea ca userul vrea o gluma si interogarea bazei de date pentru o gluma
	-logic_adapter --> clasa parinte pentru toate adaptoarele logice
	-low_confidence --> adaptor ce stabileste ca nu stie sa raspunda la input ul unui utilizator
	-mathematical_evaluation --> cautarea si parsarea de input matematic pentru a oferi un raspuns satisfacator
	-multi_adapter --> da cel mai bun raspuns dat de restul adaptoarelor
	-no_knowlege_adapter
	-time_adapter--> stabileste ca userul vrea sa stie cat este timpul
- research in zona de bayes naiv si fine tuning asupra adaptoarelor pentru a ajunge ca robot sa dea raspunsuri satisfacatoare ( datele de antrenament sa fie potrivite )
- integrarea tuturor componentelor intr-o clasa parinte b4bot.py ce reprezinta robotul efectiv
- corectarea codului scris de alti oameni




