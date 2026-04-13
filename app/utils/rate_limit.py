from slowapi import Limiter
from slowapi.util import get_remote_address

# Default to in-memory storage for rate limiting. 
# This ensures the app works locally without Redis.
# In production, this can be configured to use Redis.
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")