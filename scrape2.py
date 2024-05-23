import json

import contractions
import re
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup



def download_category_page(URL, pageNumber):
    acceptedGenres = ["Action", "Comedy", "Crime", "Adventure", "Drama", "Horror", "Romance", "Sci-Fi", "Animation", "Mystery", "Thriller", "Fantasy"]


    URL = f'{URL}&start={50*pageNumber+1}'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    article = soup.find("div", class_="article")
    results = article.find_all("div", class_="lister-item mode-advanced")
    movies = []
    for index, result in enumerate(results):
        movie = {}

        # extract title
        head = result.find("h3", class_="lister-item-header")
        title = (head.find("a").text)
        movie['title'] = title

        # extract genres
        genreSection = result.find("span", class_="genre")
        genres = genreSection.text.split(',')
        genres = list(map(str.strip, genres))

        genres = [x for x in genres if x in acceptedGenres]

        if len(genres)==0:
            pass

        movie['genres'] = genres



        # extract plot
        r = result.find_all("p", class_="text-muted")
        plot = r[1].text
        movie['plot'] = plot

        movies.append(movie)

    return movies

def download_category(URL, numOfPages):
    movies = []
    for page in range(numOfPages):
        print(f'downloading page {page+1}/{numOfPages}')
        movies.extend(download_category_page(URL, page))
    return movies

def pre_process_data(movies):
    for movie in movies:

        plot = movie['plot']
        plot = plot.lower()
        plot = contractions.fix(plot)
        plot = re.sub(r'[^a-zA-Z0-9]', ' ', plot)
        plot = plot.strip()

        movie['plot'] = plot
    return movies


def download_categories(URLS, file='movies.json', save=False, numOfPages=1):
    allMovies = []
    for index, url in enumerate(URLS):
        print(f'downloading category {index+1}/{len(URLS)}')
        movies = download_category(url, numOfPages)

        print("removing duplicates")
        for movie in movies:
            if not any(d['title'] == movie['title'] for d in allMovies):
                allMovies.append(movie)
        print("done")

    print("preprocessing text for all movies")
    allMovies = pre_process_data(allMovies)
    print("done")

    if save:
        random.shuffle(allMovies)
        file = open(file, "w")
        json.dump(allMovies, file)
        file.close()
    return allMovies


def get_movies(file):
    data = pd.read_json(file)
    return data