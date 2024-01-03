import openai
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from loguru import logger


API_KEY_NAME = "Authorization"
PREFIX = "Bearer"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    if not api_key.startswith(PREFIX):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key format")
    api_key_without_prefix = api_key[len(PREFIX) :].strip()
    logger.debug(f"API Key without prefix : {api_key_without_prefix}")
    openai.api_key = api_key_without_prefix
    try:
        openai.models.list()
    except openai.AuthenticationError as e:
        logger.error(f"API Key verification failed : {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return api_key_without_prefix
