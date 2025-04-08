import asyncio
from services import CNNService, SupabaseService
from models import Clinica

async def main():
    # Buscar a clínica pelo CNPJ
    supabase_service = SupabaseService()
    clinica_data = await supabase_service.get_clinica_by_cnpj("30747815000108")
    
    if not clinica_data:
        print("Clínica não encontrada!")
        return
    
    # Criar instância da clínica
    clinica = Clinica(**clinica_data)
    
    # Inicializar o serviço CNN com as credenciais da clínica
    cnn_service = CNNService(clinica)
    
    # Buscar o paciente pelo CPF
    try:
        paciente_data = await cnn_service.get_paciente("06286689966")
        print("Dados do paciente:")
        print(paciente_data)
    except Exception as e:
        print(f"Erro ao buscar paciente: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
