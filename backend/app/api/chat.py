from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.rag.pipeline import generate_response
from app.db.mongo import chats_collection
from app.core.deps import get_current_user

from datetime import datetime
import uuid

router = APIRouter()

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


# =========================
# CHAT API (MAIN)
# =========================
@router.post("/")
async def chat(request: ChatRequest, user=Depends(get_current_user)):
    try:
        session_id = request.session_id or str(uuid.uuid4())

        # 🧠 GET HISTORY
        chat_doc = chats_collection.find_one({
            "user_email": user["email"],
            "session_id": session_id
        })

        history = []

        if chat_doc:
            for msg in chat_doc["messages"]:
                history.append({
                    "role": msg["role"],
                    "content": msg.get("content") or msg.get("text")
                })

        # 🤖 AI RESPONSE
        response = generate_response(
            query=request.message,
            history=history,
            session_id=session_id
        )

        answer = response["answer"]

        print("AI ANSWER:", answer) 

        # 💾 SAVE TO MONGO
        chats_collection.update_one(
            {
                "user_email": user["email"],
                "session_id": session_id
            },
            {
                "$push": {
                    "messages": {
                        "$each": [
                            {"role": "user", "content": request.message},
                            {"role": "assistant", "content": answer}
                        ]
                    }
                },
                "$setOnInsert": {
                    "title": request.message[:30],
                    "created_at": datetime.utcnow()
                },
                "$set": {
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )

        return {
            "status": "success",
            "session_id": session_id,
            "response": answer,
            "sources": response.get("sources", [])
        }

    except Exception as e:
        print("CHAT ERROR:", e)
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# GET SINGLE CHAT
# =========================
@router.get("/chat/{session_id}")
def get_chat(session_id: str, user=Depends(get_current_user)):
    try:
        chat = chats_collection.find_one(
            {
                "user_email": user["email"],
                "session_id": session_id
            },
            {"_id": 0}
        )

        return chat if chat else {"messages": []}

    except Exception as e:
        print("GET CHAT ERROR:", e)
        return {"messages": []}


# =========================
# GET HISTORY
# =========================
@router.get("/history")
def get_chat_history(user=Depends(get_current_user)):
    try:
        chats = list(
            chats_collection.find(
                {"user_email": user["email"]},
                {"_id": 0}
            ).sort("updated_at", -1)
        )

        return chats

    except Exception as e:
        print("HISTORY ERROR:", e)
        return []


# =========================
# DELETE CHAT
# =========================
@router.delete("/delete/{session_id}")
def delete_chat(session_id: str, user=Depends(get_current_user)):
    try:
        chats_collection.delete_one({
            "user_email": user["email"],
            "session_id": session_id
        })

        return {"message": "Deleted"}

    except Exception as e:
        print("DELETE ERROR:", e)
        return {"error": "Delete failed"}