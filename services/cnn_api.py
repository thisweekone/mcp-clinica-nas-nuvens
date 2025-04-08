import httpx
from typing import Dict, List, Optional
import base64
from models import Clinica

class CNNService:
    def __init__(self, clinica: Clinica):
        self.base_url = "https://api.clinicanasnuvens.com.br"
        # Cria a string de autenticação no formato correto: "apiCnn:{api_key}"
        auth_string = f"apiCnn:{clinica.api_key}"
        # Codifica em Base64
        auth_base64 = base64.b64encode(auth_string.encode()).decode()
        
        self.headers = {
            "accept": "application/json",
            "clinicaNasNuvens-cid": clinica.cnn_id,
            "authorization": f"Basic {auth_base64}"
        }
    
    async def get_paciente(self, cpf_cnpj: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/paciente/lista",
                params={"cpfCnpj": cpf_cnpj},
                headers=self.headers
            )
            return response.json()
    
    async def get_pacientes(self, nome: str = "", email: str = "", telefone: str = "") -> Dict:
        async with httpx.AsyncClient() as client:
            params = {}
            if nome:
                params["nomeContem"] = nome
            if email:
                params["email"] = email
            if telefone:
                params["telefone"] = telefone
                
            response = await client.get(
                f"{self.base_url}/paciente/lista",
                params=params,
                headers=self.headers
            )
            return response.json()
    
    async def get_convenios_paciente(self, id_paciente: int) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/convenio-paciente/lista",
                params={"idPaciente": id_paciente},
                headers=self.headers
            )
            return response.json()
    
    async def criar_paciente(self, dados_paciente: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/paciente/novo",
                json=dados_paciente,
                headers=self.headers
            )
            return response.json()
    
    async def associar_convenio(self, id_paciente: int, id_tipo_convenio: int) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/convenio-paciente/associar",
                json={
                    "idPaciente": id_paciente,
                    "idTipoConvenio": id_tipo_convenio
                },
                headers=self.headers
            )
            return response.json()
    
    async def get_especialidades(self, nome: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/especialidade/lista",
                params={
                    "nomeContem": nome,
                    "somenteAtendidasNaClinica": True
                },
                headers=self.headers
            )
            return response.json()
    
    async def get_executores_agenda(
        self,
        id_especialidade: Optional[int] = None,
        id_tipo_convenio: Optional[int] = None,
        nome: Optional[str] = None
    ) -> Dict:
        params = {
            "somenteAtivos": True
        }
        if id_especialidade:
            params["idEspecialidade"] = id_especialidade
        if id_tipo_convenio:
            params["idTipoConvenio"] = id_tipo_convenio
        if nome:
            params["nomeContem"] = nome
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/executor-agenda/lista",
                params=params,
                headers=self.headers
            )
            return response.json()
    
    async def get_disponibilidade_executor(
        self,
        id_executor: int,
        cod_tipo_atendimento: int,
        data_inicio: str,
        data_fim: str
    ) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/executor-agenda/disponibilidade",
                params={
                    "idExecutorAgenda": id_executor,
                    "codTipoAtendimento": cod_tipo_atendimento,
                    "data": data_inicio,
                    "dataFim": data_fim
                },
                headers=self.headers
            )
            return response.json()
    
    async def criar_agendamento(self, dados_agendamento: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/agenda/novo",
                json=dados_agendamento,
                headers=self.headers
            )
            return response.json()
    
    async def remarcar_agendamento(
        self,
        id_agenda: int,
        nova_data: str,
        novo_horario_inicial: str,
        novo_horario_final: str,
        motivo: str
    ) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/agenda/{id_agenda}/remarcar",
                json={
                    "novaData": nova_data,
                    "novoHorarioInicial": novo_horario_inicial,
                    "novoHorarioFinal": novo_horario_final,
                    "motivo": motivo
                },
                headers=self.headers
            )
            return response.json()
    
    async def alterar_status_agendamento(self, id_agenda: int, status: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/agenda/alteracao-status",
                json={
                    "idAgenda": id_agenda,
                    "status": status
                },
                headers=self.headers
            )
            return response.json() 
    
    async def get_tipo_convenios(self) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tipo-convenio/lista",
                headers=self.headers
            )
            return response.json()
    
    async def get_tipo_procedimentos(self, nome: str = "", somente_ativos: bool = True) -> Dict:
        async with httpx.AsyncClient() as client:
            params = {}
            if nome:
                params["nomeContem"] = nome
            if somente_ativos is not None:
                params["somenteAtivos"] = somente_ativos
                
            response = await client.get(
                f"{self.base_url}/tipo-procedimento/lista",
                params=params,
                headers=self.headers
            )
            return response.json()
    
    async def get_tipo_consultas(self, nome: str = "") -> Dict:
        async with httpx.AsyncClient() as client:
            params = {}
            if nome:
                params["nomeContem"] = nome
                
            response = await client.get(
                f"{self.base_url}/tipo-consulta/lista",
                params=params,
                headers=self.headers
            )
            return response.json()
    
    async def get_executor_by_id(self, id_executor: int) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/executor-agenda/{id_executor}",
                headers=self.headers
            )
            return response.json()
    
    async def get_agendamentos(self, codigo_paciente: Optional[int] = None, 
                              data_inicial: Optional[str] = None, 
                              data_final: Optional[str] = None,
                              data_por: str = "AGENDAMENTO") -> Dict:
        async with httpx.AsyncClient() as client:
            params = {"dataPor": data_por}
            
            if codigo_paciente:
                params["codigoPaciente"] = codigo_paciente
            if data_inicial:
                params["dataInicial"] = data_inicial
            if data_final:
                params["dataFinal"] = data_final
                
            response = await client.get(
                f"{self.base_url}/agenda/lista",
                params=params,
                headers=self.headers
            )
            return response.json()
    
    async def get_valores_procedimento(self, 
                                      id_tipo_procedimento: int, 
                                      id_tipo_convenio: int,
                                      data_base: str,
                                      hora_base: str) -> Dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tipo-procedimento/valores-venda",
                params={
                    "idTipoProcedimento": id_tipo_procedimento,
                    "idTipoConvenio": id_tipo_convenio,
                    "dataBase": data_base,
                    "horaBase": hora_base
                },
                headers=self.headers
            )
            return response.json()