from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(extra="allow", env_file=".env")
    
    # Configurações do Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Configurações do Evolution API
    EVOLUTION_API_URL: str
    EVOLUTION_API_KEY: str
    
    # Configurações do MCP
    MCP_SERVER_URL: str
    MCP_API_KEY: str

@lru_cache()
def get_settings():
    return Settings()