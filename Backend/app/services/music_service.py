
from googleapiclient.discovery import build
from app.core.config import settings
import random

EMOTION_QUERY_MAP = {
    "happy": [
        "Melody", "Viral Melody",
        "Romantic", "viral Romantic",
        "Romantic Remix",
        "Mashup", 
        "Cover", "old Song"
    ],

    "sad": [
        "Sad", "viral sad",
        "Lo-fi",
        "Acoustic",
        "Sufi",
        "Classical"
    ],

    "angry": [
        "Rap / Hip-Hop",
        "EDM",
        "Remix"
    ],

    "neutral": [
        "Remix",
        "Melody",
        "Mashup",
        "slowed-reverb", "bgm", "old song"
    ],

    "fear": [
        "Classical",
        "Lo-fi",
        "Sufi",
        "Acoustic"
    ],

    "surprise": [
        "Mashup",
        "Remix",
        "EDM",
        "Cover",
        "Melody"
    ],

    "disgust": [
        "Acoustic",
        "Classical",
        "Melody",
        "Cover",
        "Lo-fi"
    ]
}

def search_music_by_emotion(emotion:str, language:str):

    emotion_query = random.choice(EMOTION_QUERY_MAP.get(emotion.lower()))
    query = f"{language} {emotion_query}"

    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        request = youtube.search().list(
            part = 'snippet',
            maxResults = 30,
            q = query,
            type = "video",
            videoCategoryId = 10
        )

        response = request.execute()
        video = []

        # if response.get('items'):
        #     item = random.choice(response['items'])
        #     video_id = item['id']['videoId']
        #     title = item['snippet']['title']
        #     embed_url = f"https://www.youtube.com/embed/{video_id}?enablejsapi=1"
        #     return{
        #         "title":title,
        #         "video_id":video_id,
        #         "embed_url":embed_url
        #     }

        for item in response.get("items",[]):
            video_id = item['id']['videoId']

            video.append({
                "title" : item["snippet"]["title"],
                "video_id" : video_id,
                "embed_url": f"https://www.youtube.com/embed/{video_id}?enablejsapi=1"
            })
        return {
            "videos":video
        }
     
    except Exception as e:
        print(f"Error calling YouTube API: {e}")
    
    return {"error": "unable to Search song. Error Occured"}