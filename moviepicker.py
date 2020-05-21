# coding: utf-8
#
# Jeffrey Zhong 

import requests
from bs4 import BeautifulSoup

def clean_digits( s ):  
    """returns only the digits in the input string s"""
    numbers = ['1','2','3','4','5','6','7','8','9','0','.']
    string = ''
    for i in range(len(s)):
        if s[i] in numbers:
            string += s[i] 
    return string 

def rottentitle(movie):
    """
    turns movie title to a rottentomatoes() compatible movie
    """
    title = movie
    title = title.lower()
    return (title.replace(' ', '_'))

def rottentomatoes(movie):
    """
    returns the rotten tomato ratting of a movie 
    movie e.g = 'black_panther_2018' or 'spider_man_into_the_spider_verse' 
    """
    url = 'https://www.rottentomatoes.com/'
    ulrplus = 'm/'+ movie 
    url += ulrplus
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    #return soup
    score = soup.find('span', attrs={'class': 'mop-ratings-wrap__percentage'})
    score = str(score)
    score = int(clean_digits(score))
    return score

def imdb(title) :
    """
    returns imdb score of movie and multiplies it by 10
    examples 'Logan' or 'Rocky'
    """ 
    url = 'https://www.imdb.com/chart/top'
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    movie = soup.select('td.titleColumn')
    ratings = soup.select('td.posterColumn span[name=ir]')
    for x in range(len(movie)-1): 
        if title in str(movie[x]):
            index = x 
    score = str(ratings[index])
    score = clean_digits(score)
    score = float(score)
    score = score * 10
    score = int(score)
    return score 

def whichmovie(movie1, movie2):
    """
    returns which movie you should watch 
    """ 
    score1 = (rottentomatoes(rottentitle(movie1)) + imdb(movie1)) / 2 
    score2 = (rottentomatoes(rottentitle(movie2)) + imdb(movie2)) / 2 
    if score1 > score2:
        print(str(score1) + ' versus '  + str(score2))
        print('Watch: '  + movie1 )
    elif score2 > score1:
        print(str(score1) + ' versus ' + str(score2))
        print ('Watch: ' + movie2)
    else:
        print( "I don't know")


        
def main():
    """
    print('Huh which movie should I watch ....') 
    print('The Dark Knight or Pulp Fiction')
    whichmovie('The Dark Knight', 'Pulp Fiction')
    print()
    print('How about Fight Club or Forrest Gump')
    whichmovie('Fight Club', 'Forrest Gump')
    print()
    print('or Goodfellas or Matrix')
    whichmovie('Goodfellas', 'The Matrix')
    print()
    print("Ugh, too many choices ... ")
    print("I'll just watch Shrek again")
    """
    movieone = input("Enter first movie : ") 
    print (movieone)
    movietwo = str(input("Enter second movie : ")) 
    print (movietwo)
    try:
        whichmovie(movieone, movietwo)
    except UnboundLocalError: 
        print('Movie(s) entered may be mispelled; please try again...')
    # """

if __name__ == "__main__":
    main()  

    
