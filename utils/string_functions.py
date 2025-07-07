import re

def get_video_id(url: str) -> str:
    if "youtu.be" in url:
        return re.search(r'youtu.be/(.{11})', url).group(1)

    if "/shorts/" in url:
        return re.search(r'/shorts/(.{11})', url).group(1)

    match = re.search(r'[?&]v=([^&]{11})', url)
    return match.group(1) if match else None


def get_video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"
