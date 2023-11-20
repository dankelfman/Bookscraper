import requests
from bs4 import BeautifulSoup
import re  # Importing the regex module

# URL of the Goodreads book page
url = 'https://www.goodreads.com/book/show/6043781-blood-of-elves'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Extracting book details
title = soup.find('h1', {'data-testid': 'bookTitle'}).text.strip()
author = soup.find('span',{'data-testid': 'name'}).text.strip()
rating = soup.find('div', class_='RatingStatistics__rating').text.strip()
ratings_text = soup.find('span', {'data-testid': 'ratingsCount'}).text.strip()
num_ratings = int(ratings_text.split()[0].replace(',', ''))
reviews_text = soup.find('span', {'data-testid': 'reviewsCount'}).text.strip()
num_reviews = int(reviews_text.split()[0].replace(',', ''))
description_html = soup.find('span', class_='Formatted')
description = '\n'.join([x for x in description_html.stripped_strings])

# Extracting the ISBN using regex
isbn = 'ISBN not found'
isbn_match = re.search(r'\b\d{13}\b', response.text)  # Regex pattern for a 13-digit number
if isbn_match:
    isbn = isbn_match.group()

# Display the extracted information
print(f'Title: {title}')
print(f'Author: {author}')
print(f'Rating: {rating} stars')
print(f'Number of Ratings: {num_ratings}')
print(f'Number of Reviews: {num_reviews}')
print(f'Description: {description[:200]}...')  # Displaying first 200 characters of the description
print(f'ISBN: {isbn}')