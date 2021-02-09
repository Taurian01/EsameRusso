#creo le 2 liste che userò in get_data e in daily_stats
lista1 = []
lista2 = []

#creo la classe ExamException per gestire le eccezioni
class ExamException(Exception):
    pass

#creo la classe principale
class CSVTimeSeriesFile:

    #la variabile name rappresenta il nome del file che verrà aperto per prendere i dati
    def __init__(self, name):
        self.name = name
        pass

    #il metodo get_data(self) mi restituisce una lista contenente altre liste composte da 2 elementi che sono la data di quando sono state fatte le misurazioni e le misurazioni stesse della temperatura
    def get_data(self):

        #primo controllo: provo ad aprire il file con il comando try, se il file non esiste allora alzo l'eccezione
        try: 
            dati = open(self.name, 'r')
        except:
            raise ExamException("Errore nell'apretura del file: il file è mancante")

        #contatore usato per verificare l'ordine delle date e le possibili ripetizioni di valori epoch
        cont3=-1
        for line in dati:

            #divido la riga in 2 elementi usando come elemento separatore la "," 
            split = line.split(',')
            var = 0

            #salto la prima riga che contiene solo i nomi delle variabili
            if split[1] != 'temperature\n':

                #secondo controllo: devo verificare che le due variabili del epoch e delle temperature siano valori int o float, per le temperature ho usato int poichè se la data mi viene data come valore folating point è rischiesto di trasformarla in in intero. Se non posso convertire le date o le temperature, a interi e floating point rispettivamente, salto la riga ma non alzo una eccezione
                try:
                    temp = float(split[1])
                    data = int(split[0])

                    #terzo conmtrollo: verifico che tutte le date siano in ordine crescente e che non ci siano ripetizioni. Se non lo sono alzo un eccezione
                    #uso la variabile var per portare gli ExamException fuori dal try
                    if data == cont3:
                        var = 1
                    elif data<cont3:
                        var = 2
                    sub_lista = [data,temp]
                    lista1.append(sub_lista)
                    cont3 = data
                except:
                    pass

                if var == 1:
                    raise ExamException('Errore nella scrittura delle date: due date hanno lo stesso valore')
                elif var == 2:
                    raise ExamException('Errore nella scrittura delle date: le date non sono in ordine cronologico')


        #chiuso il file da cui prendo i dati
        dati.close()

        #ritorno la lista contenente tutte le misurazioni fatte e i momenti in cui sono state fatte
        return lista1


def daily_stats(self):

    #definisco gli estremi del while, essendo le date in ordine cronologicoo mi basta prendere il primo valore e l'ultimo
    mintot = lista1[0][0]
    maxtot = lista1[len(lista1)-1][0]

    #il comando int mi permette di prendere solo la parte intera dopo una divisione, quindi posso usarlo efficacemente per definire i giorni se divido l'epoch per 86400 (i secondi in un giorno)
    #il comando int se trova un numumero molto elevato dopo la virgola (es:0.99999999999999999) può arrotondare al valore successivo ma questo non accade per 86399/86400, quindi non può accadere per altri valori. Il comando int è quindi sicuro da usare
    base = int(mintot/86400)

    #per vedere se le misurazioni sono fatte nello stesso giorno faccio la divisione e controllo che l'intero sia uguale
    while base>=int(mintot/86400) and base<= int(maxtot/86400):

        #calcolo la media e trovo i valori massimi e minimi in una giornata
        min_day=''
        max_day=0
        med_day=0
        sum_day = 0 
        cont = 0
        for line in lista1:
            
            if int(line[0]/86400)==base:
                
                #massimo
                if line[1]>max_day:
                    max_day = line[1]

                #minimo
                if min_day == '':
                    min_day = line[1]
                elif line[1]<min_day:
                    min_day = line[1]

                #media      
                cont+=1                  
                sum_day += line[1]
        med_day = sum_day/cont

        #creo la lista contenente min, max e media
        sub_lista_day = [min_day,max_day,med_day]

        #le inserisco all'interno di 'lista2'
        lista2.append(sub_lista_day)

        #aumento il contatore 'base' di 1 che sigifica che controllo i valori per il giorno successivo
        base+=1
    
    #ritorno la 'lista2'
    return lista2