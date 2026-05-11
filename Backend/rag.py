from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from Backend.config import GOOGLE_API_KEY
from langchain_community.vectorstores import FAISS
from fastapi import UploadFile,File,APIRouter
import shutil

rag = APIRouter(tags=["Upload"])
retriever = None

@rag.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    global retriever
    saved_path = f"uploads/{file.filename}"
    with open(saved_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    loader = PyPDFLoader(saved_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)
    chunks = splitter.split_documents(document)
    embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=GOOGLE_API_KEY
)
    vectordb = FAISS.from_documents(chunks,embeddings)
    retriever = vectordb.as_retriever(search_kwargs = {"k":3})

    return {"filename":file.filename,
            "pages"   :len(document),
            "uploaded":"pdf uploaded successfully"}
