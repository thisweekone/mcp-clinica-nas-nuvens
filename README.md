# MCP Clínica nas Nuvens - Atendimento Automatizado

Sistema de atendimento automatizado para clínicas médicas via WhatsApp, utilizando processamento de linguagem natural para oferecer uma experiência humanizada.

## Funcionalidades

- Agendamento de consultas e exames
- Remarcação de compromissos existentes
- Cancelamento de consultas
- Confirmação de presença
- Consulta de horários disponíveis
- Esclarecimento de dúvidas comuns
- Integração com sistema Clínica nas Nuvens

## Requisitos

- Python 3.8+
- FastAPI
- Supabase
- Evolution API
- MCP Server

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/mcp-clinica-nas-nuvens.git
cd mcp-clinica-nas-nuvens
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

5. Configure as variáveis de ambiente no arquivo `.env` com suas credenciais.

## Executando o Servidor

Para iniciar o servidor em modo de desenvolvimento:

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

## Documentação da API

A documentação da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do Projeto

```
mcp-clinica-nas-nuvens/
├── main.py              # Ponto de entrada da aplicação
├── config.py            # Configurações do sistema
├── models.py            # Modelos de dados
├── routes.py            # Rotas da API
├── services/            # Serviços de integração
│   ├── cnn_api.py       # Integração com Clínica nas Nuvens
│   ├── evolution_service.py  # Integração com Evolution API
│   ├── mcp_service.py   # Integração com MCP Server
│   └── supabase_service.py  # Integração com Supabase
├── requirements.txt     # Dependências do projeto
└── .env                 # Variáveis de ambiente
```

## Configuração do Webhook

1. Configure o webhook do Evolution API para apontar para:
```
http://seu-servidor/api/v1/webhook/whatsapp
```

2. Certifique-se de que o servidor está acessível publicamente.

## Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 