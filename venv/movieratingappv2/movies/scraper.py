from bs4 import BeautifulSoup
import requests
import re


class Scraper:
    url = 'http://www.imdb.com/chart/top'

    def __init__(self,url):
        self.url = url 

    def getMovies(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        movies = soup.select('td.titleColumn')
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        imdb = []
        # Store each item into dictionary (data), then put those into a list (imdb)
        for index in range(0, len(movies)):
            # Seperate movie into: 'place', 'title', 'year'
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            rating = ratings[index]

            try :
                year = int(year)
            except:
                year = 0 
            
            try :
                rating = float(rating)
            except:
                rating = 0

            data = {
                    "name": movie_title,
                    "year": year,
                    "rating": rating
                    }
            imdb.append(data)
        return imdb