import datetime

import urllib2, sys

from bs4 import BeautifulSoup


##function definition
def openConfig ():
    
    config_dictionary = {}
    
    config_name = "./dataScrapper.conf"
    
    try:
        print "\n" + "Reading configuration file" + "\n"
        config_file = open(config_name, "r")
    
    except:
        
        print "Cant find config file" 
        print "...exiting program..."
        sys.exit(1)
    
    for line in config_file:
            
        words = line.split("=")

        if "#" not in words[0]:
            
            if "linkSource" in words[0]:
                
                print "Found valid HTML archive: " + words[1]
                
                config_dict = {words[0].strip() : words[1].strip()}
                
                config_dictionary.update(config_dict)
                # add here other config code
            if "destFile"in words[0]:

                print "Destination File: " + words[1] 

                config_dict = {words[0].strip() : words[1].strip()}

                config_dictionary.update(config_dict)

    return config_dictionary
            

def scrapeData (listaA , shipsDictionary):
    
    nome_assetto = ""

    destinazione = ""

    coordinate = ""

    for i in range(len(listaA)):

        new_link = listaA[i][2] # link list
        
        nome_assetto = listaA[i][1] # link list

        new_link_html = urllib2.urlopen(new_link)

        try:
                new_link_soup = BeautifulSoup(new_link_html,'html.parser')

                raw_data_paring = new_link_soup.find_all('tr')
        
        except:
                print "The provided link is not consistent, or you are not connected to the network"
                print "....exiting program..."
                sys.exit(1)

        for item_link in raw_data_paring:

            try:

                if hasattr(item_link.contents[0], "text") and hasattr(item_link.contents[1], "text"):

                    if (item_link.contents[0].text.encode('ascii','ignore')  == 'Destinazione'):

                        destinazione = item_link.contents[1].text

                    if (item_link.contents[0].text.encode('ascii','ignore')  == 'Coordinate'):

                        coordinate = item_link.contents[1].text
            except:

                pass

        print str(listaA[i][0]) + " Nave: " + nome_assetto + " Destinazione: " + destinazione + " Coordinate: " + coordinate

        new_dic = {"Num": str(listaA[i][0]), "Nave": nome_assetto , "Destinazione": destinazione , "Coordinate" : coordinate}

        shipsDictionary.append(new_dic)
    return

def saveData (shipsDictionaryA ,file_to_save):

    print "-----------------------------------------------------"
    print "-   Saving data CSV format: shipdatafile.csv        -"
    print "-----------------------------------------------------"

    #file_to_save = "shipdatafile.csv"

    csvFile = open(file_to_save, "w")

    csvFile.write(datetime.datetime.now().strftime("Data, %d/%m/%y,Ora, %H:%M")+"\n")

    columnTitleRow = "SEQ, SHIP, DESTINATION, COORDINATES\n"

    csvFile.write(columnTitleRow)
    
    for i in range(len(shipsDictionaryA)):
        count = shipsDictionaryA[i]['Num']
        nave = shipsDictionaryA[i]['Nave']
        destinazione = shipsDictionaryA[i]['Destinazione']
        coordinate = shipsDictionaryA[i]['Coordinate']
        row = count+" ,"+nave+" ,"+destinazione+" ,"+coordinate+"\n"
        csvFile.write(row)
    return

def printLista (listaA):
    try:
        
        for i in range(len(listaA)):
            print listaA[i]
    except:
        print "Error in given list"
    
    return

####-----------------------------------------------------------------------
#### MAIN START 
####-----------------------------------------------------------------------
def main ():

    shipsDictionary = []

    listaAssets = [] # creo la lista vuota di assetti

    index = 0

    config_dictionary = openConfig()

    try:
        bookmarks = config_dictionary.get("linkSource")

        bookmarks_soup = BeautifulSoup(open(bookmarks).read(), 'html.parser')
    except:
        print "Cant find: " + bookmarks
        print "...exiting program..."
        sys.exit(1)

    raw_data = bookmarks_soup.find_all('a') # collect al links from WEBARCHIVE
 
    print "-----------------------------------------------------"
    print " Gathering Ships information from provided DATAFILE  "
    print "-----------------------------------------------------"

    for item in raw_data:
        index = index + 1
        new_element = (index, item.contents[0].encode('ascii','ignore') , item.get("href").encode('ascii','ignore'))
        listaAssets.append(new_element)

    ## add all links in a dictionary

    try:
        
        scrapeData (listaAssets , shipsDictionary)

    except:
        
        print "link doesnt exist, or you are not connected to the network"
        print "...exiting program..."
        sys.exit(1)
        
    saveData(shipsDictionary,config_dictionary.get("destFile"))


#--------------------------------------------------------
#--------------------------- starting app----------------
#--------------------------------------------------------
main()
