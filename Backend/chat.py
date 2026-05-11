import os
from dotenv import load_dotenv
from google import genai 
from fastapi import APIRouter
from fastapi import WebSocket
from Backend.prompt import SYSTEM_PROMPT
import Backend.rag as rag
from Backend.config import GOOGLE_API_KEY
from fastapi import WebSocketDisconnect

load_dotenv()

client = genai.Client(api_key=GOOGLE_API_KEY)
router = APIRouter(tags=["websocket"])

@router.get("/")
def home():
    return {"message":"running successfully"}

@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    try:

        while True:
            user_msg = await websocket.receive_text()
            if rag.retriever is None:
                await websocket.send_text( "Please upload PDF first" )
                await websocket.send_text("[END]") 
                continue
            docs =rag.retriever.invoke(user_msg)
            context = "\n\n".join([doc.page_content for doc in docs])
            full_prompt = f"""
        {SYSTEM_PROMPT}
        context:
        {context}
        user:
        {user_msg}

        """
        
            reply = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=full_prompt
)
            await websocket.send_text(reply.text)
            await websocket.send_text("[END]")
    except WebSocketDisconnect:
        print("Client Disconnected")