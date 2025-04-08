import httpx
from typing import Dict, Optional
from config import get_settings

settings = get_settings()

class EvolutionService:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.headers = {
            "accept": "application/json",
            "apikey": settings.EVOLUTION_API_KEY
        }
    
    async def send_message(self, number: str, message: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/send",
                json={
                    "number": number,
                    "text": message
                },
                headers=self.headers
            )
            return response.json()
    
    async def send_file(self, number: str, file_url: str, caption: Optional[str] = None) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/send",
                json={
                    "number": number,
                    "file": file_url,
                    "caption": caption
                },
                headers=self.headers
            )
            return response.json()
    
    async def get_message_status(self, message_id: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/message/status/{message_id}",
                headers=self.headers
            )
            return response.json()
    
    async def get_chat_history(self, number: str, limit: int = 50) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/chat/history",
                params={
                    "number": number,
                    "limit": limit
                },
                headers=self.headers
            )
            return response.json() 