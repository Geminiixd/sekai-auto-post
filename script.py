import requests
import openai
import json
import os
from dotenv import load_dotenv
from pytrends.request import TrendReq

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_URL = os.getenv("WP_URL")

# Function to get trending topics using Pytrends
def get_trending_topics():
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        trending_searches = pytrends.trending_searches(pn="united_states")
        topics = trending_searches[0].tolist()[:5]  # Get top 5 topics
        return topics
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
        return []

# Function to generate post content using OpenAI
def generate_post_content(topic):
    prompt = f"Write an informative blog post about {topic} in a conversational and engaging tone."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error generating content for {topic}: {e}")
        return None

# Function to publish a post on WordPress
def publish_post(title, content):
    if not content:
        print(f"Skipping post for {title} due to empty content.")
        return None

    data = {
        "title": title,
        "content": content,
        "status": "publish"  # Change to "draft" if you want to review before posting
    }
    
    try:
        response = requests.post(WP_URL, auth=(WP_USERNAME, WP_PASSWORD), json=data)
        if response.status_code == 201:
            print(f"Successfully posted: {title}")
        else:
            print(f"Failed to post {title}: {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error publishing post for {title}: {e}")
        return None

# Main automation script
def main():
    topics = get_trending_topics()
    if topics:
        for topic in topics:
            print(f"Generating content for: {topic}...")
            content = generate_post_content(topic)
            publish_post(topic, content)
    else:
        print("No trending topics found.")

if __name__ == "__main__":
    main()
