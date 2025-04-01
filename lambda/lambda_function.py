from dotenv import load_dotenv
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os

from google import genai

load_dotenv()

def ask(subtitles):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"```{subtitles}```이 내용을 한글로 요약해줘",
    )

    return response.text


def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]
    return video_id

def lambda_handler(event, context):
    print(event)
    print('----------')
    print(context)
    video_url = "https://www.youtube.com/watch?v=7xTGNNLPyMI"
    video_id = get_video_id(video_url)

    # issues: https://github.com/jdepoix/youtube-transcript-api/issues/303
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ko'], proxies={"https": "http://localhost:8080"})

    text_formatter = TextFormatter()
    text_formatted = text_formatter.format_transcript(transcript)

    subtitles = text_formatted.replace("\n", " ")

    response = ask(subtitles)
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }