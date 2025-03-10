from bs4 import BeautifulSoup
import requests
import time
import os
import re
import csv
import math

### Web Scraper

### Setting up parameters
# setup a target url
url = "https://movie.douban.com/top250" 
# header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# manual switch if refresh the page content
force_use_cache = True

# start working on formatting the data
movies = []

def get_page_content(url):
    # get the page content
    response = requests.get(url, headers=header)
    
    if response.status_code != 200:
        print("Failed to get the page content")
        return None
    
    return response.content

def parse_html(html):
    # parse the page content
    soup = BeautifulSoup(html, "html.parser")
    return soup

# save the parsed content to a file, but skip if the file already exists
current_dir = os.path.dirname(__file__)

dirpath = os.path.join(current_dir, "movie_pages_html_cache")
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

# figure out how many movies are in one page
# request the first page content and see how many movies are in the first page
def request_or_read_cache(url, dirpath, index, force_use_cache):
    file_path = os.path.join(dirpath, f"movie_{index}.html")
    if os.path.exists(file_path) and force_use_cache:
        print("Requestor: The file already exists")
        with open(file_path, "r", encoding="utf-8") as f:
            movie = parse_html(f.read())
    else:
        print("Requestor: Requesting the page content")
        time.sleep(2) # add sleep time to avoid being blocked when requesting
        movie = parse_html(get_page_content(url))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(movie))
    return movie

movie_firstpage = request_or_read_cache(url, dirpath, 0, force_use_cache)
# get the number of movies in one page and number of pages
movies_in_one_page = len(movie_firstpage.find_all("div", class_="item"))
pages_of_movies = math.ceil(250/movies_in_one_page)
print(f"movies in one page: {movies_in_one_page}, pages of movies: {pages_of_movies}")

# request all pages and save the content to files
for page_index in range(pages_of_movies):

    # make movie list
    print(f"Handling movie pages")
    if page_index == 0:
        page_content = movie_firstpage
    else:
        page_content = request_or_read_cache(url=f"{url}?start={page_index*movies_in_one_page}", index=page_index, dirpath=dirpath, force_use_cache=force_use_cache)

    all_items = page_content.find_all("div", class_="item")

    for movie_index in range(len(all_items)):

        #get the movie item
        item = all_items[movie_index]

        # print the movie item title name
        print(f"Handling movie item {movie_index} from page {page_index}")

        # set up the list to store the movie information
        movie = []

        # get movie id
        movie_rank = movie_index + page_index*movies_in_one_page + 1
        movie.append(movie_rank)

        # get the movie title and original language title - if exist
        titles = item.find_all("span", class_="title")
        title_main = titles[0].text.replace("\xa0", "")
        movie.append(title_main)
        if len(titles) > 1: # check if the movie has an original language title
            movie.append(titles[1].text.replace("\xa0", "").replace("/", ""))
        else:
            movie.append("N/A")
        
        # get the movie other title's translations
        other = item.find("span", class_="other").text
        other_pattern = re.compile(r'\s*/\s*')
        other_titles = re.sub(other_pattern, ", ", other)
        if other_titles.startswith(", "):
            other_titles = other_titles[2:]
        movie.append(other_titles)
        
        # get the movie rating
        movie.append(item.find("span", class_="rating_num").text.replace("\xa0", ""))
        
        # get the movie rating people
        rate_people = item.find("span", text=re.compile("人评价"))
        if rate_people:
            movie.append(rate_people.text.replace("\xa0", "").replace("人评价", ""))
        
        print(movie)
        movies.append(movie)
        # end of the loop circuling through movies in one page
    
    # end of the loop circuling through all pages

# print the movie list
print(movies)

# save the movie list to a CSV file
csv_file = os.path.join(current_dir, "movie.csv")
with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Original Title", "Other Titles", "Rating", "Rating People"])
    writer.writerows(movies)