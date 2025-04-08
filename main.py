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
            "name": "listar_pacientes",
            "description": "Lista todos os pacientes da clínica",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "nome": "string (opcional, filtro por nome)",
                "cpf": "string (opcional, filtro por CPF)"
            }
        },
        {
            "name": "criar_paciente",
            "description": "Cria um novo paciente na clínica",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "nome": "string",
                "cpf": "string",
                "data_nascimento": "string (YYYY-MM-DD)",
                "telefone": "string",
                "email": "string"
            }
        },
        {
            "name": "obter_paciente",
            "description": "Obtém os dados de um paciente específico",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "cpf": "string"
            }
        },
        {
            "name": "listar_convenios_paciente",
            "description": "Lista os convênios de um paciente específico",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "id_paciente": "integer"
            }
        },
        {
            "name": "associar_convenio_paciente",
            "description": "Associa um convênio a um paciente",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "paciente_id": "string",
                "convenio_id": "string",
                "numero_carteira": "string"
            }
        },
        {
            "name": "listar_tipos_convenios",
            "description": "Lista todos os tipos de convênios disponíveis",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)"
            }
        },
        {
            "name": "listar_executores",
            "description": "Lista todos os médicos/executores disponíveis",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "id_especialidade": "integer (opcional)",
                "id_tipo_convenio": "integer (opcional)",
                "nome": "string (opcional)"
            }
        },
        {
            "name": "listar_especialidades",
            "description": "Lista todas as especialidades disponíveis",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "nome": "string (opcional, filtro por nome)"
            }
        },
        {
            "name": "verificar_disponibilidade",
            "description": "Verifica a disponibilidade de horários",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "executor_id": "string",
                "data_inicio": "string (YYYY-MM-DD)",
                "data_fim": "string (YYYY-MM-DD)"
            }
        },
        {
            "name": "criar_agendamento",
            "description": "Cria um novo agendamento",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "paciente_id": "string",
                "executor_id": "string",
                "data": "string (YYYY-MM-DD)",
                "hora": "string (HH:MM)",
                "convenio_id": "string (opcional)",
                "observacoes": "string (opcional)"
            }
        },
        {
            "name": "listar_agendamentos",
            "description": "Lista os agendamentos",
            "parameters": {
                "cnpj": "string (CNPJ da clínica)",
                "paciente_id": "string (opcional)",
                "executor_id": "string (opcional)",
                "data_inicio": "string (YYYY-MM-DD, opcional)",
                "data_fim": "string (YYYY-MM-DD, opcional)"
            }
        },
        {
            "name": "obter_clinica",
            "description": "Obtém os dados de uma clínica pelo CNPJ",
            "parameters": {
                "cnpj": "string"
            }
        }
    ]
    return {"tools": tools}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 