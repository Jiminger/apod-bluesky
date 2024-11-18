import os
from typing import Any, Dict
from atproto import Client, client_utils
import requests


# Load environment variables
APOD_URL = "https://api.nasa.gov/planetary/apod"
APOD_API_KEY = os.environ["APOD_API_KEY"]  
BLUESKY_HANDLE = os.environ["BLUESKY_HANDLE"]
BLUESKY_PASSWORD = os.environ["BLUESKY_PASSWORD"]


def get_apod() -> requests.Response:
    response = requests.get(APOD_URL, params={"api_key": APOD_API_KEY, "thumbs": True})
    if response.status_code == 200:
        return response  
    else:
        raise Exception("Failed to retrieve APOD!")

def parse_apod_response(response: requests.Response) -> Dict[str, Any]:
    data = response.json()
    title = data.get('title')
    copyright = data.get('copyright').strip()
    explanation = data.get('explanation')
    media_type = data.get('media_type')

    url = data.get('url')
    thumbnail_url = data.get('thumbnail_url')

    if media_type == 'video':
        image_data = requests.get(thumbnail_url).content
    else:
        image_data = requests.get(url).content

    return {
        "title": title,
        "copyright": copyright.strip(),
        "explanation": explanation,
        "url": url,
        "thumbnail_url": thumbnail_url,
        "image_data": image_data,
        "media_type": media_type
    }

def post_to_bluesky(parsed_response: Dict) -> None:
    client = Client()
    client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)

    text_builder = client_utils.TextBuilder()
    text_builder.text(parsed_response['title'])
    
    if parsed_response['copyright'] is not None:
        print('\nCopyright: ' + parsed_response['copyright'])
        text_builder.text('\nCopyright: ' + parsed_response['copyright'])

    if parsed_response['media_type'] == 'video':
        text_builder.text('\n\nClick ')
        text_builder.link('here', parsed_response['url'])
        text_builder.text(' to watch the video.')
    
    client.send_image(text=text_builder, image=parsed_response['image_data'], image_alt=parsed_response['explanation'])
    
        

def lambda_handler(event, context):
    try:
        response = get_apod()
        parsed_response = parse_apod_response(response)
        post_to_bluesky(parsed_response)
        return {"statusCode": 200, "body": "APOD posted to BlueSky successfully!"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}