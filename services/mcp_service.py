import httpx
from typing import Dict, List, Optional
from config import get_settings

settings = get_settings()

class MCPService:
    def __init__(self):
        self.base_url = settings.MCP_SERVER_URL
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.MCP_API_KEY}"
        }
    
    async def process_message(
        self,
        message: str,
        context: Optional[Dict] = None,
        tools: Optional[List[str]] = None
    ) -> Dict:
        payload = {
            "message": message,
            "context": context or {},
            "tools": tools or []
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/process",
                json=payload,
                headers=self.headers
            )
            return response.json()
    
    async def get_available_tools(self) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tools",
                headers=self.headers
            )
            return response.json()
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict,
        context: Optional[Dict] = None
    ) -> Dict:
        payload = {
            "tool": tool_name,
            "parameters": parameters,
            "context": context or {}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/execute",
                json=payload,
                headers=self.headers
            )
            return response.json()
    
    async def update_context(self, context: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/context",
                json=context,
                headers=self.headers
            )
            return response.json() 