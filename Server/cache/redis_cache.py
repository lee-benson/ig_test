import redis

# Connect to Redis (Has its own databases)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Get cached data function
def get_data_from_cache(cache_key):
    cached_data = redis_client.get(cache_key)
    if cached_data is not None:
        return cached_data.decode('utf-8')
    return None

# Setting cached data
def set_data_in_cache(cache_key, ttl, data):
    redis_client.setex(cache_key, ttl, data)

# post_cache_key = f'cache_key_post_user_{user_id}'
# comment_cache_key = f'cache_key_comment_user_{user_id}'
# chat_cache_key = f'cache_key_chat_user_{user_id}'
# message_cache_key = f'cache_key_message_user_{user_id}'

# Set TTLs for different data
posts_ttl = 3600 # 1 hour
comments_ttl = 300 # 5 minutes 
messages_ttl = 300 
chats_ttl = 300

# Cache pruning could be implemented for Posts, Message, Comments (Chat(?))




