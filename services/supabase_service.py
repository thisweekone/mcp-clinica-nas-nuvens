from supabase import create_client, Client
from typing import Dict, Optional
from config import get_settings

settings = get_settings()

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    async def get_clinica_by_cnpj(self, cnpj: str) -> Optional[Dict]:
        response = self.client.table('companies').select('*').eq('cnpj', cnpj).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def create_clinica(self, clinica_data: Dict) -> Dict:
        response = self.client.table('companies').insert(clinica_data).execute()
        return response.data[0]
    
    async def update_clinica(self, cnpj: str, clinica_data: Dict) -> Dict:
        response = self.client.table('companies').update(clinica_data).eq('cnpj', cnpj).execute()
        return response.data[0]
    
    async def delete_clinica(self, cnpj: str) -> Dict:
        response = self.client.table('companies').delete().eq('cnpj', cnpj).execute()
        return response.data[0] 