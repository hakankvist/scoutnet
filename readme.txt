Känner du dig inte trygg med begreppen kommandorad så bör du inte använda det här programmet.


** Att installera **

För linuxanvändare som kör debian eller ubuntu:

1. sudo apt-get install python python-argparse

För windowsanvändare:

1. Gå till hemsidan: http://python.org/download/
   Välj att ladda ner antingen:
     Python 2.7.3 Windows Installer          - om du kör 32 bitars windows
     Python 2.7.3 Windows X86-64 Installer   - om du kör 64 bitars windows
2. Installera programmet


** Ladda ner skriptet **
1. Gå till sidan: https://github.com/hakankvist/scoutnet
2. Tryck på knappen "ZIP", då laddar du ner alla filerna i en zip-fil
3. Packa upp zip-filen till en valfri katalog

** Att köra skriptet **
1. Gå till katalogen där du packade upp filerna
2. Skriv: "scoutnet_csv.py -h" för att få upp hjälp över de olika parametrarna.



Exempel på hur man kör skriptet:
För att sortera om listan enligt "avdelning,förnamn,efternamn" skriv (filen sparas i filen output.csv):
  scoutnet_csv.py -i scoutnet.csv -g

För slå ihop alla telefonnummer (ej kår- och distriktsnummer) till ett fält som ligger först) skriv:
  scoutnet_csv.py -i scoutnet.csv -p

För att slå ihop alla telefonnummer och sortera enligt avdelning skriv:
  scoutnet_csv.py -i scoutnet.csv -p -g

För att sortera listan i ordningen, "postnummer,adress,efternamn,förnamn" skriv:
  scoutnet_csv.py -i scoutnet.csv -s

För att göra ovanstående men ange ett annat filnamn för resultatet skriv:
  scoutnet_csv.py -i scoutnet.csv -s -o min_nya_sorterade_lista.csv

