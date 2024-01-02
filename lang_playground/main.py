import random
from typing import List

import openai
from fastapi import Depends, FastAPI
from loguru import logger

from lang_playground.common.aop.auth import get_api_key
from lang_playground.common.error import include_exception_handler
from lang_playground.common.resp import BaseApiResp


app = FastAPI()
include_exception_handler(app)


@app.get("/models")
async def root(api_key: str = Depends(get_api_key)) -> BaseApiResp[List[str]]:
    openai.api_key = api_key
    val = random.randint(0, 10)
    logger.info(f"val : {val}")
    if val % 2 == 0:
        raise Exception("random exception")
    model_list_response = openai.models.list()
    model_names = [model.id for model in model_list_response.data]
    return BaseApiResp[List[str]](data=model_names)
