from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.chat_models import (
    Conversation,
    ConversationCreate,
    Message,
    ChatRequest,
    ChatResponse
)
from ..models.db_models import Conversation as DBConversation, Message as DBMessage
from ..auth.utils import get_current_active_user
from ..models.db_models import User

router = APIRouter()

@router.post("/conversations", response_model=Conversation)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_conversation = DBConversation(
        user_id=current_user.id,
        title=conversation.title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conversations = db.query(DBConversation).filter(
        DBConversation.user_id == current_user.id
    ).all()
    return conversations

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(DBConversation).filter(
        DBConversation.id == conversation_id,
        DBConversation.user_id == current_user.id
    ).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get or create conversation
    conversation = None
    if request.conversation_id:
        conversation = db.query(DBConversation).filter(
            DBConversation.id == request.conversation_id,
            DBConversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        conversation = DBConversation(
            user_id=current_user.id,
            title="New Conversation"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = DBMessage(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)

    # TODO: Process message with chatbot and get response
    # This is where you'll integrate with your chatbot logic
    bot_response = "This is a placeholder response"
    symptoms = []  # Extract symptoms from the conversation
    diagnosis = None  # Get diagnosis if applicable

    # Save bot response
    bot_message = DBMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=bot_response
    )
    db.add(bot_message)
    db.commit()

    return ChatResponse(
        message=bot_response,
        conversation_id=conversation.id,
        symptoms=symptoms,
        diagnosis=diagnosis
    ) 