# import the required python modules
from bs4 import BeautifulSoup
import requests
import pandas as pd

# access the HTML content from the webpage
# create a BeautifulSoup object
url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# extract desired data table from HTML data by inspecting the DOM
telly = soup.find("tbody", class_="lister-list").find_all("tr")

# create an empty list to store parsed data
tv_list = []
# create dictionary to store parsed data onto another list
for tv in telly:
    rank = tv.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]
    title = tv.find("td", class_="titleColumn").a.text
    year = tv.find("td", class_="titleColumn").span.text.strip("()")
    rating = tv.find("td", class_="ratingColumn imdbRating").strong.text
    data = {"rank": rank, "title": title, "year": year, "rating": rating}
    tv_list.append(data)

df = pd.DataFrame(tv_list)
df.index = range(1, df.shape[0] + 1)
df.set_index("rank", inplace=True)
print(df)
df.to_csv("/Users/marshall/Downloads/imdb_top_250_tv_shows.csv")