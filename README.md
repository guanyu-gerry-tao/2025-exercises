# 2025-exercises
🧑‍💻This repository documents my early coding journey as I started learning programming.  
It includes my first practice projects, basic exercises, and initial explorations in coding.  

## 📝About  
- 📖 **Purpose**: To track my progress and improvements over time.  
- 🛠 **Content**: Early coding exercises, small projects, and experiments.  
- 🚀 **Note**: These are my first steps in programming, and the code quality may not reflect my current skills.  

I know those code would be sucks, especially those early codes,
But I will keep learning, improving, and building better projects in the future!

## 🤖AI use disclaimer
I realize AI in VSCode was overkill for beginner programmer who wish to remember and practice. I use it for reference only.
ChatGPT is used for consulting only, not for generating codes.
Not yet using Cursor.

# project list
### 📌exercise-hello-world
finished on 2025-03-08

This project is the starting point, helping setting up and study
- the VSCode venv
- the Github workflow

### 📌exercise-web-scraper
finished on 2025-03-09

This project is my first study project, learning web scraper: scraping data, parsing and formatting the movie data from Douban.html, one of largest Chinese film websites.

#### This project revisited my previous Python knowledge:
- Practicing web scraping
- file caching using `with open() as f`
- requesting and the BeautifulSoup
- basic logic, looping
- `os` module and dir operation
- regex

#### result:
Scripts extracted multiple-page contents from https://movie.douban.com/top250 and its following pages (such as https://movie.douban.com/top250?start=25), generated a CSV file with top 250 movies in Douban and saved in local disk.
