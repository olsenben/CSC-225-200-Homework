import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

data_dir = 'api_data'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

class JSONPlaceHolderAPI:
    """ class for working with API """

    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com/"

    def get_resource(self, resource_type, resource_id=None):
        url = f"{self.base_url}/{resource_type}"

        if resource_id:
            url += f"{resource_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_users(self):
        """gets users"""
        return self.get_resource("users")
    
    def get_user(self,user_id=None):
        """ get posts from specific user """
        if user_id:
            url = f"{self.base_url}/users/{user_id}/posts"
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            
            else:
                print(f"Error: {response.status_code}")
                return None
        
        else:
            return self.get_resource("posts")
        
    def get_comments(self, post_id=None):
        
        if post_id:
            url = f"{self.base_url}/posts/{post_id}/comments"
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            
            else:
                print(f"Error: {response.status_code}")
                return None
        
        else:
            return self.get_resource("comments")
        
class NotesManager:
    """ class for managing notes of users posts"""
    def __init__(self, storage_dir=data_dir):
        self.storage_dir = storage_dir
        self.notes_file = os.path.join(storage_dir,"user_notes.json")
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, "r") as file:
                return json.load(file)

    def save_notes(self):
        with open(self.notes_file, "w") as file:
            json.dump(self.notes, file, indent=4)

    def add_note(self, user_id, note_text):
        user_id = str(user_id)
        if user_id not in self.notes:
            self.notes[user_id] = []
        
        self.notes[user_id].append({
            "text": note_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_notes()
        print(f"note has been saved for {user_id}")

    def get_notes(self, user_id):
        """ get all notes for a single user"""

        user_id = str(user_id)
        return self.notes.get(user_id, [])

def fetch_webpage(url):
    """ fetch data from webpage"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text
        
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
def save_html(html_content, filename="sample_page.html"):
    """ Save html data for further analysis"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"HTML has been saved to {filename}")

def simple_html_parser(html_content, tag_name):
    results = []

    html_lower = html_content.lower()
    tag_name = tag_name.lower()

    start_tag = f"<{tag_name}>"
    end_tag = f"</{tag_name}>"

    pos = 0

    while True:

        start_pos = html_lower.find(start_tag, pos)
        if start_pos == -1:
            break

        tag_end = html_lower.find(">", start_pos)
        if tag_end == -1:
            break

        end_pos = html_lower.find(end_tag, tag_end)
        if end_pos == -1:
            break

        content_start = tag_end + 1
        content_end = end_pos
        content = html_lower[content_start:content_end].strip()

        results.append(content)

        pos = end_pos + len(end_tag)
    return results

def parse_with_beautifulsoup(html_content):

    soup = BeautifulSoup(html_content, "html.parser")

    title = soup.title
    if title:
        print(f"Page Title: {title}")

    links = soup.find_all('a')
    print(f"Links: {links}")
        
if __name__ == "__main__":
    web_url = "https://aquariums.yodls.co/"

    page = fetch_webpage(web_url)

    parse_with_beautifulsoup(page)