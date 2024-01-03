import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger

from lang_playground.common.aop.auth import get_api_key
from lang_playground.common.resp import BaseApiResp
from lang_playground.common.utils.file_utils import load_pdf
from lang_playground.internal.llm import parse_resume
from lang_playground.schemas.career.models import ResumeModel


router = APIRouter(prefix="/career", tags=["career"])


@router.post(
    "/resume",
    response_model=BaseApiResp,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"model": BaseApiResp, "description": "Unsupported Media Type"},
        status.HTTP_404_NOT_FOUND: {"model": BaseApiResp, "description": "Not Found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseApiResp, "description": "Internal Server Error"},
    },
)
async def upload_resume(
    model: str = "gpt-3.5-turbo-16k", file: UploadFile = File(...), api_key: str = Depends(get_api_key)
) -> BaseApiResp[ResumeModel]:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Please upload a PDF file.",
        )
    try:
        documents = await load_pdf(await file.read())
        pdf_contents = "".join([document.page_content for document in documents])
        logger.info(f"PDF contents length: {len(pdf_contents)}")
        # FIXME: api_key 넣을 수 있는 다른 방법 리서치 하기
        os.environ["OPENAI_API_KEY"] = api_key
        v1_resume = await parse_resume(pdf_contents, model=model)
        resume = v1_resume.to_model()
        os.environ["OPENAI_API_KEY"] = ""
        return BaseApiResp(data=resume)
    except Exception as e:
        logger.error(f"Failed to load PDF : {e}")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Please upload a PDF file.",
        )
