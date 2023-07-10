import requests
from bs4 import BeautifulSoup
import openai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Set up OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def get_fb_reels_metadata_and_transcript(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract metadata
        metadata = {
            "author": soup.find("a", class_="i18nContentAuthor").text.strip(),
            "title": soup.find("h1", class_="i18nContentTitle").text.strip(),
            # Add any additional metadata fields you want to extract
        }

        # Extract video URL
        video_url = soup.find("video", class_="video-stream html5-main-video")["src"]

        # Download video and save it (optional)

        # Extract transcript using OpenAI Whisper
        transcript = generate_transcript(video_url)

        return metadata, transcript

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None, None


def generate_transcript(video_url):
    try:
        # Generate transcript using OpenAI Whisper
        prompt = f"Translate the following English video into English:\nVideo URL: {video_url}\n\nTranscript:"
        response = openai.Completion.create(
            engine="whisper",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
            log_level="info"
        )
        transcript = response.choices[0].text.strip()

        return transcript

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None

# Example usage
video_url = "https://www.facebook.com/reels/video/123456789"
metadata, transcript = get_fb_reels_metadata_and_transcript(video_url)

if metadata and transcript:
    print("Metadata:", metadata)
    print("Transcript:", transcript)
else:
    print("Error occurred. Please check the logs.")
