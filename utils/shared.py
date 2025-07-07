# from collections import deque

# dict for number of server queues
SONG_QUEUES = {}

SHUFFLED_QUEUES = []
LOOPED_QUEUES = []

def get_queue(guild_id: int) -> deque:
    return sh.SONG_QUEUES.get(str(guild_id), deque())

def get_current_song(guild_id: int):
    queue = get_queue(guild_id)
    return queue[0] if queue else None

def is_playing(guild: discord.Guild) -> bool:
    return (
        guild.voice_client is not None
        and str(guild.id) in sh.SONG_QUEUES
        and len(sh.SONG_QUEUES[str(guild.id)]) > 0
    )
