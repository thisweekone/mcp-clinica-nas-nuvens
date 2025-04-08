from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routes import router

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="MCP Clínica nas Nuvens",
    description="API de integração para atendimento automatizado via WhatsApp",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API MCP Clínica nas Nuvens"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/tools")
async def list_tools():
    tools = [
        {
            "name": "send_message",
            "description": "Envia uma mensagem para um número via WhatsApp",
            "parameters": {
                "cnpj": "string",
                "number": "string",
                "message": "string"
            }
        },
        {
            "name": "check_status",
            "description": "Verifica o status de uma mensagem",
            "parameters": {
                "cnpj": "string",
                "message_id": "string"
            }
        }
    ]
    return {"tools": tools}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 