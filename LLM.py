import ollama
from db import get_oneConv, createConv, updateConv
from typing import List, Dict


def generate_prompt(conversation_history: List[Dict[str, str]], user_query: str) -> str:
    prompt = "The following is a conversation between a helpful AI and a user:\n\n"
    for chat in conversation_history:
        prompt += f"User: {chat['Query']}\n"
        prompt += f"AI: {chat['Response']}\n"
    prompt += f"User: {user_query}\n"
    prompt += "AI: "
    return prompt


def existing_chat_with_mistral(convID: str, user_query: str) -> dict:
    conversation = get_oneConv(convID)
    if "error" in conversation:
        return {"error": "Conversation not found."}

    chat_history = conversation.get("Chat", [])[-10:]  
    formatted_prompt = generate_prompt(chat_history, user_query)

    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": formatted_prompt}])
        ai_response = response["message"]
        updateConv(convID, user_query, ai_response)
        return {"success": True, "conversation_id": convID, "response": ai_response}
    except Exception as e:
        return {"error": f"Error generating response: {str(e)}"}



def new_chat_with_mistral(username: str, user_query: str) -> Dict:
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_query}])
        ai_response = response["message"]
        conversation_id = createConv(username=username, query=user_query, response=ai_response)
        return {"success": True, "conversation_id": conversation_id, "response": ai_response}
    except Exception as e:
        return {"error": f"Error generating response: {str(e)}"}