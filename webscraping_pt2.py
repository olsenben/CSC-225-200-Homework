import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3

data_dir = "scraped_data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

class BookScraper:
    def __init__(self):
        self.base_url = "http://books.toscrape.com/"
        self.books = []
    
    def fetch_webpage(self, url):
        """Fetch data from a webpage - reusing our function from last class"""
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text 
            else:
                print(f"Error: status code {response.status_code}") 
                return None
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")  
            return None
    
    def scrape_books_from_page(self, page_num=1):
        """Scrape book data from specific book page"""
        
        url = f"{self.base_url}catalogue/page-{page_num}.html"
        html_content = self.fetch_webpage(url)
        
        if not html_content:
            return False
        
        soup = BeautifulSoup(html_content, 'html.parser')
        book_containers = soup.select('article.product_pod')
        
        if not book_containers:
            return False
            
        for book in book_containers:
            # Extract book details
            title = book.h3.a['title']
            price = book.select_one('p.price_color').text
            availability = book.select_one('p.availability').text.strip()
            rating = book.select_one('p.star-rating')['class'][1]
            
            # Get book URL for additional details
            book_url = book.h3.a['href']
            if 'catalogue/' not in book_url:
                book_url = 'catalogue/' + book_url
            book_full_url = self.base_url + book_url
            
            self.books.append({
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating,
                'url': book_full_url
            })
        
        return True
    
    def scrape_multiple_pages(self, num_pages=3):
        for page in range(1, num_pages + 1):
            print(f"Scraping page {page}...")
            success = self.scrape_books_from_page(page)
            if not success:
                print(f"Failed to scrape page {page} or no more pages available.")
                break
        
        print(f"Scraped a total of {len(self.books)} books.")
        return self.books
    
    def save_to_json(self, filename="books_data.json"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, indent=4)
        print(f"Book data saved to {filepath}")


def run_scraping():
    scraper = BookScraper()
    books = scraper.scrape_multiple_pages(3)  
    scraper.save_to_json()
    return books

class BookDataAnalyzer:
    def __init__(self, books_data=None, json_file=None):
        if books_data:
            self.df = pd.DataFrame(books_data)
        elif json_file:
            filepath = os.path.join(data_dir, json_file)
            with open(filepath, "r", encoding='utf-8') as f:
                books_data = json.load(f)
            self.df = pd.DataFrame(books_data)
        else:
            self.df = pd.DataFrame()
        
        if not self.df.empty:
            self._preprocess_data()

    def _preprocess_data(self):
        """ allows us to clean and prepare data"""
        self.df['price_numeric'] = self.df['price'].str.replace('Â£','', regex=False).astype(float)

        rating_map = {
            'One': 1,
            'Two' : 2,
            'Three' : 3,
            'Four' : 4,
            'Five' : 5,
        }
            
        self.df['rating_numeric'] = self.df['rating'].map(rating_map)

        self.df['rating_clean'] = self.df['availability'].str.strip()

    def get_summary_stats(self):

        stats = {
           'total_books': len(self.df),
            'ave_price' : self.df['price_numeric'].mean(),
            'min_price' : self.df['price_numeric'].min(),
            'max_price' : self.df['price_numeric'].max(),
            'rating_counts' : self.df['rating'].value_counts().to_dict(),
            'ave_rating' : self.df['rating_numeric'].mean(),
        }
        return stats

    def get_best_value_book(self, min_rating=4, n=5):
        value_books = self.df[self.df['rating_numeric'] >= min]
        return value_books.sort_values('price__numeric').head(n)
    
    def save_processed_data_csv(self, filename='processed_books.csv'):
        filepath = os.path.join(data_dir, filename)
        self.df.to_csv(filepath, index=False)
        print(f'data saved to {filepath}')

class BookDatabase:
    """managing books using SQLITE"""
    def __init__(self, db_name='books_database.db'):
        self.db_path = os.path.join(data_dir,db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        print(f'Connected to Database at {self.db_path}')
    
    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                rating INTEGER NOT NULL,
                availability TEXT,
                url TEXT
            )                
        ''')
        self.conn.commit()
        print(f'successfully created tables')

    def insert_books(self, books_df):
        """inserts from data frame into database"""
        self.cursor.execute('SELECT title from books')
        existing_titles = [row[0] for row in self.cursor.fetchall()]

        #added_date = datetime.now().strftime("%Y-%m-%d")

        insert_count = 0

        for _, row in books_df.iterrows():
            if row['title'] not in existing_titles:
                self.cursor.execute('''
                    INSERT INTO books (title, price, rating, availability, url) 
                        VALUES (?, ?, ?, ?, ?)
                        ''', (
                            row['title'],
                            row['price_numeric'],
                            row['rating_numeric'],
                            row['availability'],
                            row['url']
                        ))                
                insert_count += 1
        
    def get_book_by_id(self, book_id):
        """ get book by id"""
        self.cursor.execute('''
            SELECT id, title, price, rating, availability, url
            FROM books
            WHERE id = ?
        ''', (book_id,))
        
        book = db.cursor.fetchone()

        return book

if __name__ == "__main__":
    books = run_scraping()
    analyzer = BookDataAnalyzer(books_data=books)
    summary_stats = analyzer.get_summary_stats()
    db = BookDatabase()
    db.insert_books(analyzer.df)

    id_book = db.get_book_by_id(1)
    print(f'Title: {id_book[1]}')
