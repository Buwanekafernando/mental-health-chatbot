from app.database import chat_collection

def get_recent_conversation(user_id: str, limit: int = 5):
    chats = chat_collection.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)

    conversation = []

    for chat in reversed(list(chats)):
        conversation.append(f"User: {chat['message']}")
        conversation.append(f"Assistant: {chat['reply']}")

    return "\n".join(conversation)
