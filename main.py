import scrape2

URLS = [
    'https://www.imdb.com/search/title/?genres=comedy',
    'https://www.imdb.com/search/title/?genres=sci-fi',
    'https://www.imdb.com/search/title/?genres=horror',
    'https://www.imdb.com/search/title/?genres=romance',
    'https://www.imdb.com/search/title/?genres=action',
    'https://www.imdb.com/search/title/?genres=thriller',
    'https://www.imdb.com/search/title/?genres=drama',
    'https://www.imdb.com/search/title/?genres=mystery',
    'https://www.imdb.com/search/title/?genres=crime',
    'https://www.imdb.com/search/title/?genres=animation',
    'https://www.imdb.com/search/title/?genres=adventure',
    'https://www.imdb.com/search/title/?genres=fantasy',
]


scrape2.download_categories(URLS, file="movies5.json", save=True, numOfPages=20)

movies2 = scrape2.get_movies("asd.json")
print(len(movies2))
