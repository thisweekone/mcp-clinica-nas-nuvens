from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

class Clinica(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    cnpj: str = Field(..., description="CNPJ da clínica")
    cnn_id: str = Field(..., description="ID da clínica no sistema Clínica nas Nuvens", alias="clinica_cid")
    api_key: str = Field(..., description="Chave de API para autenticação")
    id_rotulo: Optional[int] = Field(None, description="ID do rótulo padrão")
    id_local: Optional[int] = Field(None, description="ID do local padrão")
    id_origem_paciente: Optional[int] = Field(None, description="ID da origem do paciente padrão")

class Paciente(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: Optional[int] = None
    nome: str
    cpf_cnpj: str
    data_nascimento: str
    telefone_celular: str
    convenios: Optional[List[Dict]] = None

class Agendamento(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: Optional[int] = None
    id_paciente: int
    id_especialidade: int
    id_executor: int
    id_tipo_consulta: int
    data: str
    hora_inicio: str
    hora_fim: str
    status: str = "AGENDADO"
    observacoes: Optional[str] = None

class MensagemWhatsApp(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    numero: str
    mensagem: str
    tipo: str = "texto"
    arquivo_url: Optional[str] = None
    legenda: Optional[str] = None

class ContextoConversa(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    paciente: Optional[Paciente] = None
    clinica: Optional[Clinica] = None
    ultimo_agendamento: Optional[Agendamento] = None
    etapa_atual: str = "inicio"
    dados_coletados: Dict = Field(default_factory=dict)