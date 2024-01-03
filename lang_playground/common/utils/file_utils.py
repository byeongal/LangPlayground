import os
from tempfile import NamedTemporaryFile

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing_extensions import List


async def load_pdf(contents: bytes) -> List[Document]:
    temp_file_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
            pdf_loader = PyPDFLoader(file_path=temp_file_path)
        return pdf_loader.load()
    except Exception as e:
        raise e
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
