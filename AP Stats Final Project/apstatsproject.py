# coding: utf-8
#
# Jeffrey Zhong 

import requests
from bs4 import BeautifulSoup
import csv  
import random 


def clean_digits(s):  
    """
    returns only the digits in the input string s
    """
    numbers = ['1','2','3','4','5','6','7','8','9','0','.']
    string = ''
    for i in range(len(s)):
        if s[i] in numbers:
            string += s[i] 
    return string 


def pokemongo():
    """
    webscrapes gamepress's webiste for CP values of each pokemon in Go
    returns a list of [pokedex number, max CP]
    pokemon ordered in alphabetical order
    """
    url = 'https://gamepress.gg/pokemongo/pokemongo/pokemongo/pokemongo/pokemongo/pokemongo/pokemon-list'
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    #print(soup)
    raw_html = list()
    for line in soup.findAll('tr', attrs={'class': 'pokemon-row'}):
        raw_html.append(line.text)
    #print(raw_html)
    raw_html = str(raw_html)
    cpdata = []
    pokenum = []
    for line in soup.findAll('span', attrs={'class': 'cp-40'}):
        cpdata.append(line.text)
    for x in range(len(raw_html)): 
        if raw_html[x] == '#':
            number = raw_html[x+1:x+5]
            number = clean_digits(number)
            #print(number)
            pokenum.append(number)
    listdata = []
    #print (cpdata)
    #print (pokenum)  
    for x in range(len(cpdata)):
        t1 = [pokenum[x] , cpdata[x]]
        listdata.append(t1) 
    return listdata

def clean_data():
    """
    cleans up pokemongo() and orders it  by pokedex number
    returns cleaned up list
    """
    data = pokemongo()
    for x in range(len(data)-1):
        try:
            data[x][0] = int(data[x][0])
        except(ValueError):
            del data[x]
    #for some reason the above code dosen't work for #221; idk why
    for x in range(len(data)):
        if data[x][0] == '221':
            data[x][0] = 221 
    #above is a janky work around
    #print(data) 
    data.sort(key=lambda x:x[0])
    return data

def data_csv():
    """
    turns our data into a csv file
    and saves it on our computer
    """
    fields = ['Pokedex #', 'CP']
    rows = clean_data()
    filename = "Pokemon_GO_CSV.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)   
        csvwriter.writerows(rows) 

def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

def pokemonstrat():
    """
    prints out the size of what each stratum needs to be for each geneation 
    for our random sample to be of size 30
    """
    Pokemon = readcsv('Pokemon.csv')
    generation = []
    for x in range(len(Pokemon)):
        generation.append(Pokemon[x][11])
    gen1 = generation.count('1')
    gen2 = generation.count('2')
    gen3 = generation.count('3')
    gen4 = generation.count('4')
    gen5 = generation.count('5')
    total = gen1 + gen2 + gen3 + gen4 + gen5 
    print( round((gen1/total)*30) , ':' , 'size of stratum for Gen 1')
    print( round((gen2/total)*30) , ':' , 'size of stratum for Gen 2')
    print( round((gen3/total)*30) , ':' , 'size of stratum for Gen 3')
    print( round((gen4/total)*30) , ':' , 'size of stratum for Gen 4')
    print( round((gen5/total)*30) , ':' , 'size of stratum for Gen 5')
    """
    7 : size of stratum for Gen 1
    4 : size of stratum for Gen 2
    7 : size of stratum for Gen 3
    5 : size of stratum for Gen 4
    7 : size of stratum for Gen 5
    """

def get_random_sample():
    """
    retunrs our random stratified sample as a list 
    with Pokedex numbers as our population
    """
    gen1 = []
    for x in range(7):
        value = random.randint(1,151)
        if value not in gen1:
            gen1.append(value)
    gen2 = []
    for x in range(4):
        value = random.randint(152,251)
        if value not in gen2:
            gen2.append(value)
    gen3 = []
    for x in range(7):
        value = random.randint(251,386)
        if value not in gen3:
            gen3.append(value)
    gen4 = []
    for x in range(5):
        value = random.randint(387,493)
        if value not in gen4:
            gen4.append(value)
    gen5 = []
    for x in range(7):
        value = random.randint(494,649)
        if value not in gen2:
            gen5.append(value)
    random_sample = gen1 + gen2 + gen3 + gen4 + gen5 
    return random_sample 

def sample_csv():
    """
    formats our data
    turns our data into a new csv file
    and saves it on our computer
    """ 
    Pokemon = readcsv('Pokemon.csv')
    Pokemon_Go = readcsv('Pokemon_GO_CSV.csv')
    sample = get_random_sample()
    Go_data = []
    for x in range(len(sample)):
        pokenum = sample[x]
        for y in range(len(Pokemon_Go)):
            try: 
                if int(Pokemon_Go[y+1][0]) == pokenum:
                    Go_data.append(int(Pokemon_Go[y+1][1]))
                    break
            except(IndexError):
                Go_data = Go_data
    Game_data = []
    for x in range(len(sample)):
        pokenum = sample[x]
        for y in range(len(Pokemon)):
            try: 
                if int(Pokemon[y+1][0]) == pokenum:
                    Game_data.append(int(Pokemon[y+1][4]))
                    break
            except(IndexError):
                Game_data = Game_data
    data = []
    for x in range(len(sample)): 
        list1 = [sample[x], Game_data[x], Go_data[x]]
        data.append(list1)
    fields = ['Pokedex #', 'Sum of Game Stats', 'CP']
    rows = data
    filename = "Final_Sample.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)  
        csvwriter.writerow(fields)   
        csvwriter.writerows(rows) 

