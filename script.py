import requests
import openai
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_URL = os.getenv("WP_URL")
# Function to get trending topics (Example: Google Trends scraping)
def get_trending_topics():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    topics = [item.text for item in soup.select(".title")][:5]  # Extract top 5 topics
    return topics

# Function to generate post content
def generate_post_content(topic):
    prompt = f"Write an informative blog post about {topic} in a conversational and engaging tone."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to publish post on WordPress
def publish_post(title, content):
    data = {
        "title": title,
        "content": content,
        "status": "publish"  # Change to "draft" if you want to review before posting
    }
    response = requests.post(WP_URL, auth=(WP_USERNAME, WP_PASSWORD), json=data)
    return response.json()

# Main automation script
def main():
    topics = get_trending_topics()
    if topics:
        for topic in topics:
            content = generate_post_content(topic)
            publish_post(topic, content)
            print(f"Posted: {topic}")
    else:
        print("No trending topics found.")

if __name__ == "__main__":
    main()
