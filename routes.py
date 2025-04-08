from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from models import MensagemWhatsApp, ContextoConversa, Clinica
from services import (
    EvolutionService,
    MCPService,
    CNNService,
    SupabaseService
)

router = APIRouter()

@router.post("/webhook/whatsapp")
async def webhook_whatsapp(message: Dict):
    try:
        # Inicializa serviços
        evolution_service = EvolutionService()
        mcp_service = MCPService()
        supabase_service = SupabaseService()
        
        # Extrai informações da mensagem
        numero = message.get("from")
        mensagem = message.get("body")
        
        if not numero or not mensagem:
            raise HTTPException(status_code=400, detail="Mensagem inválida")
        
        # Identifica a clínica pelo número
        clinica_data = await supabase_service.get_clinica_by_cnpj(numero)
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN com as credenciais da clínica
        cnn_service = CNNService(clinica)
        
        # Processa a mensagem com o MCP
        contexto = ContextoConversa(clinica=clinica)
        resposta_mcp = await mcp_service.process_message(
            message=mensagem,
            context=contexto.model_dump()
        )
        
        # Executa ações necessárias baseadas na resposta do MCP
        if resposta_mcp.get("action"):
            if resposta_mcp["action"] == "agendar_consulta":
                # Implementar lógica de agendamento
                pass
            elif resposta_mcp["action"] == "remarcar_consulta":
                # Implementar lógica de remarcação
                pass
            elif resposta_mcp["action"] == "cancelar_consulta":
                # Implementar lógica de cancelamento
                pass
        
        # Envia resposta ao paciente
        await evolution_service.send_message(
            number=numero,
            message=resposta_mcp.get("response", "Desculpe, não entendi sua mensagem.")
        )
        
        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clinicas")
async def criar_clinica(clinica_data: Dict):
    try:
        supabase_service = SupabaseService()
        nova_clinica = await supabase_service.create_clinica(clinica_data)
        return nova_clinica
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clinicas/{cnpj}")
async def obter_clinica(cnpj: str):
    try:
        supabase_service = SupabaseService()
        clinica = await supabase_service.get_clinica_by_cnpj(cnpj)
        if not clinica:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        return clinica
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/clinicas/{cnpj}")
async def atualizar_clinica(cnpj: str, clinica_data: Dict):
    try:
        supabase_service = SupabaseService()
        clinica_atualizada = await supabase_service.update_clinica(cnpj, clinica_data)
        return clinica_atualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clinicas/{cnpj}")
async def deletar_clinica(cnpj: str):
    try:
        supabase_service = SupabaseService()
        await supabase_service.delete_clinica(cnpj)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pacientes/{cpf}")
async def obter_paciente(cpf: str):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        # Usando uma clínica específica para teste
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN com as credenciais da clínica
        cnn_service = CNNService(clinica)
        
        # Busca o paciente
        paciente_data = await cnn_service.get_paciente(cpf)
        
        # Verifica se encontrou o paciente
        if not paciente_data.get("lista") or len(paciente_data["lista"]) == 0:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        
        # Obtém o primeiro paciente da lista
        paciente = paciente_data["lista"][0]
        
        # Busca os convênios do paciente
        convenios_data = await cnn_service.get_convenios_paciente(paciente["id"])
        
        # Adiciona os convênios ao paciente
        paciente["convenios"] = convenios_data.get("lista", [])
        
        return paciente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clinicas/teste/{cnpj}")
async def teste_clinica(cnpj: str):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj(cnpj)
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Retorna os dados da clínica (exceto a chave API por segurança)
        safe_data = {k: v for k, v in clinica_data.items() if k != 'api_key'}
        safe_data['api_key_length'] = len(clinica_data.get('api_key', '')) if 'api_key' in clinica_data else 0
        
        return safe_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/auth/{cnpj}")
async def debug_auth(cnpj: str):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj(cnpj)
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Cria a string de autenticação no formato correto
        import base64
        auth_string = f"apiCnn:{clinica.api_key}"
        auth_base64 = base64.b64encode(auth_string.encode()).decode()
        
        # Retorna informações de depuração
        return {
            "cnpj": clinica.cnpj,
            "cnn_id": clinica.cnn_id,
            "api_key_length": len(clinica.api_key),
            "auth_string": auth_string[:10] + "..." + auth_string[-10:],  # Mostra apenas partes da string
            "auth_base64": auth_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/especialidades")
async def listar_especialidades(nome: str = ""):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        # Usando uma clínica específica para teste
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN com as credenciais da clínica
        cnn_service = CNNService(clinica)
        
        # Busca as especialidades
        especialidades_data = await cnn_service.get_especialidades(nome)
        
        return especialidades_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para buscar convênios do paciente
@router.get("/pacientes/{id_paciente}/convenios")
async def listar_convenios_paciente(id_paciente: int):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os convênios do paciente
        convenios_data = await cnn_service.get_convenios_paciente(id_paciente)
        
        return convenios_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para buscar executores de agenda
@router.get("/executores")
async def listar_executores(id_especialidade: Optional[int] = None, id_tipo_convenio: Optional[int] = None, nome: Optional[str] = None):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os executores de agenda
        executores_data = await cnn_service.get_executores_agenda(
            id_especialidade=id_especialidade,
            id_tipo_convenio=id_tipo_convenio,
            nome=nome
        )
        
        return executores_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para verificar disponibilidade do executor
@router.get("/disponibilidade")
async def verificar_disponibilidade(
    id_executor: int, 
    cod_tipo_atendimento: int, 
    data_inicio: str, 
    data_fim: str
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Verifica a disponibilidade do executor
        disponibilidade_data = await cnn_service.get_disponibilidade_executor(
            id_executor=id_executor,
            cod_tipo_atendimento=cod_tipo_atendimento,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        return disponibilidade_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para criar agendamento
@router.post("/agendamentos")
async def criar_agendamento(dados_agendamento: Dict):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Cria o agendamento
        agendamento_data = await cnn_service.criar_agendamento(dados_agendamento)
        
        return agendamento_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para remarcar agendamento
@router.put("/agendamentos/{id_agenda}/remarcar")
async def remarcar_agendamento(
    id_agenda: int,
    dados_remarcacao: Dict
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Verifica se todos os campos necessários estão presentes
        required_fields = ["nova_data", "novo_horario_inicial", "novo_horario_final", "motivo"]
        for field in required_fields:
            if field not in dados_remarcacao:
                raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {field}")
        
        # Remarca o agendamento
        remarcacao_data = await cnn_service.remarcar_agendamento(
            id_agenda=id_agenda,
            nova_data=dados_remarcacao["nova_data"],
            novo_horario_inicial=dados_remarcacao["novo_horario_inicial"],
            novo_horario_final=dados_remarcacao["novo_horario_final"],
            motivo=dados_remarcacao["motivo"]
        )
        
        return remarcacao_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para alterar status do agendamento
@router.put("/agendamentos/{id_agenda}/status")
async def alterar_status_agendamento(
    id_agenda: int,
    status: str
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Altera o status do agendamento
        status_data = await cnn_service.alterar_status_agendamento(
            id_agenda=id_agenda,
            status=status
        )
        
        return status_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para criar paciente
@router.post("/pacientes")
async def criar_paciente(dados_paciente: Dict):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Cria o paciente
        paciente_data = await cnn_service.criar_paciente(dados_paciente)
        
        return paciente_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para associar convênio ao paciente
@router.post("/pacientes/{id_paciente}/convenios/{id_tipo_convenio}")
async def associar_convenio_paciente(
    id_paciente: int,
    id_tipo_convenio: int
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Associa o convênio ao paciente
        convenio_data = await cnn_service.associar_convenio(
            id_paciente=id_paciente,
            id_tipo_convenio=id_tipo_convenio
        )
        
        return convenio_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar tipos de convênios
@router.get("/tipos-convenios")
async def listar_tipos_convenios():
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os tipos de convênios
        convenios_data = await cnn_service.get_tipo_convenios()
        
        return convenios_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar tipos de procedimentos
@router.get("/tipos-procedimentos")
async def listar_tipos_procedimentos(nome: str = "", somente_ativos: bool = True):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os tipos de procedimentos
        procedimentos_data = await cnn_service.get_tipo_procedimentos(nome, somente_ativos)
        
        return procedimentos_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar tipos de consultas
@router.get("/tipos-consultas")
async def listar_tipos_consultas(nome: str = ""):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os tipos de consultas
        consultas_data = await cnn_service.get_tipo_consultas(nome)
        
        return consultas_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para buscar executor por ID
@router.get("/executores/{id_executor}")
async def buscar_executor(id_executor: int):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca o executor por ID
        executor_data = await cnn_service.get_executor_by_id(id_executor)
        
        return executor_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar agendamentos
@router.get("/agendamentos")
async def listar_agendamentos(
    codigo_paciente: Optional[int] = None,
    data_inicial: Optional[str] = None,
    data_final: Optional[str] = None,
    data_por: str = "AGENDAMENTO"
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os agendamentos
        agendamentos_data = await cnn_service.get_agendamentos(
            codigo_paciente=codigo_paciente,
            data_inicial=data_inicial,
            data_final=data_final,
            data_por=data_por
        )
        
        return agendamentos_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obter valores de venda de procedimentos
@router.get("/procedimentos/{id_tipo_procedimento}/valores")
async def obter_valores_procedimento(
    id_tipo_procedimento: int,
    id_tipo_convenio: int,
    data_base: str,
    hora_base: str
):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os valores do procedimento
        valores_data = await cnn_service.get_valores_procedimento(
            id_tipo_procedimento=id_tipo_procedimento,
            id_tipo_convenio=id_tipo_convenio,
            data_base=data_base,
            hora_base=hora_base
        )
        
        return valores_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar pacientes
@router.get("/pacientes")
async def listar_pacientes(nome: str = "", email: str = "", telefone: str = ""):
    try:
        # Busca a clínica para usar nas credenciais
        supabase_service = SupabaseService()
        clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
        
        if not clinica_data:
            raise HTTPException(status_code=404, detail="Clínica não encontrada")
        
        # Cria instância da clínica
        clinica = Clinica(**clinica_data)
        
        # Inicializa serviço da CNN
        cnn_service = CNNService(clinica)
        
        # Busca os pacientes
        pacientes_data = await cnn_service.get_pacientes(nome, email, telefone)
        
        return pacientes_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))