# Guia de Uso da API - Clínica nas Nuvens

Este guia fornece instruções detalhadas sobre como utilizar a API de integração com o sistema Clínica nas Nuvens. Ele abrange os principais endpoints, parâmetros necessários e exemplos de requisições.

## Índice

1. [Autenticação](#autenticação)
2. [Pacientes](#pacientes)
   - [Listar Pacientes](#listar-pacientes)
   - [Criar Paciente](#criar-paciente)
   - [Associar Convênio ao Paciente](#associar-convênio-ao-paciente)
3. [Convênios](#convênios)
   - [Listar Tipos de Convênios](#listar-tipos-de-convênios)
4. [Médicos (Executores)](#médicos-executores)
   - [Listar Executores](#listar-executores)
5. [Disponibilidade](#disponibilidade)
   - [Verificar Disponibilidade](#verificar-disponibilidade)
6. [Agendamentos](#agendamentos)
   - [Criar Agendamento](#criar-agendamento)
   - [Listar Agendamentos](#listar-agendamentos)

## Autenticação

Todas as requisições à API são autenticadas automaticamente pelo sistema. Não é necessário incluir tokens de autenticação nas requisições.

## Pacientes

### Listar Pacientes

Retorna uma lista de pacientes com base nos filtros fornecidos.

**Endpoint:** `GET /api/v1/pacientes`

**Parâmetros de consulta:**
- `nome` (opcional): Filtra pacientes pelo nome
- `cpf` (opcional): Filtra pacientes pelo CPF

**Exemplo de requisição:**
```
GET /api/v1/pacientes?nome=João
```

**Exemplo de resposta:**
```json
{
  "pagina": 0,
  "totalPaginas": 1,
  "lista": [
    {
      "id": 1398881,
      "nome": "João Silva",
      "cpfcnpj": "12345678901",
      "dataNascimento": "1980-01-01",
      "contato": {
        "telefoneCelular": "47999999999"
      },
      "ativo": true
    }
  ]
}
```

### Criar Paciente

Cria um novo paciente no sistema.

**Endpoint:** `POST /api/v1/pacientes`

**Corpo da requisição:**
```json
{
  "nome": "Marcos Silva",
  "cpfcnpj": "13873588048",
  "dataNascimento": "1988-01-13",
  "idOrigem": 69210,
  "contato": {
    "telefoneCelular": "47991425151"
  }
}
```

**Campos obrigatórios:**
- `nome`: Nome completo do paciente
- `cpfcnpj`: CPF ou CNPJ do paciente (apenas números)
- `dataNascimento`: Data de nascimento no formato YYYY-MM-DD
- `idOrigem`: ID da origem do paciente (use 69210)
- `contato.telefoneCelular`: Número de telefone celular

**Observação:** Após criar um paciente, é necessário associar pelo menos um convênio a ele.

### Associar Convênio ao Paciente

Associa um convênio a um paciente existente.

**Endpoint:** `POST /api/v1/pacientes/{id_paciente}/convenios`

**Corpo da requisição:**
```json
{
  "idPaciente": 19839542,
  "idTipoConvenio": 12642
}
```

**Campos obrigatórios:**
- `idPaciente`: ID do paciente
- `idTipoConvenio`: ID do tipo de convênio

## Convênios

### Listar Tipos de Convênios

Retorna uma lista de todos os tipos de convênios disponíveis.

**Endpoint:** `GET /api/v1/tipos-convenios`

**Exemplo de resposta:**
```json
{
  "pagina": 0,
  "totalPaginas": 1,
  "lista": [
    {
      "id": 12642,
      "nome": "Particular",
      "particular": true,
      "ativo": true
    },
    {
      "id": 19719,
      "nome": "Convenio Teste",
      "particular": false,
      "ativo": true
    }
  ]
}
```

## Médicos (Executores)

### Listar Executores

Retorna uma lista de médicos (executores) com base nos filtros fornecidos.

**Endpoint:** `GET /api/v1/executores`

**Parâmetros de consulta:**
- `id_especialidade` (opcional): ID da especialidade médica
- `id_tipo_convenio` (opcional): ID do tipo de convênio
- `nome` (opcional): Nome do médico

**Exemplo de requisição:**
```
GET /api/v1/executores?nome=Valmira
```

**Exemplo de resposta:**
```json
{
  "pagina": 0,
  "totalPaginas": 1,
  "lista": [
    {
      "id": 9931,
      "idPessoa": 1405079,
      "nome": "VALMIRA KOHLS BUTWILOWICZ",
      "especialidades": [
        {
          "id": 1616148,
          "nome": "CLINICA MEDICA"
        }
      ]
    }
  ]
}
```

## Disponibilidade

### Verificar Disponibilidade

Verifica a disponibilidade de horários para um médico específico.

**Endpoint:** `GET /api/v1/disponibilidade`

**Parâmetros de consulta:**
- `id_executor` (obrigatório): ID do executor (médico)
- `cod_tipo_atendimento` (obrigatório): Código do tipo de atendimento
- `data_inicio` (obrigatório): Data inicial no formato YYYY-MM-DD
- `data_fim` (obrigatório): Data final no formato YYYY-MM-DD

**Exemplo de requisição:**
```
GET /api/v1/disponibilidade?id_executor=9931&cod_tipo_atendimento=133964&data_inicio=2025-05-01&data_fim=2025-05-10
```

**Exemplo de resposta:**
```json
[
  {
    "data": "2025-05-01",
    "horaInicio": "08:00:00",
    "horaFim": "08:15:00"
  },
  {
    "data": "2025-05-01",
    "horaInicio": "08:15:00",
    "horaFim": "08:30:00"
  }
]
```

## Agendamentos

### Criar Agendamento

Cria um novo agendamento para um paciente.

**Endpoint:** `POST /api/v1/agendamentos`

**Corpo da requisição:**
```json
{
  "data": "2025-05-01",
  "encaminhamento": "Atendimento gerado via API",
  "horaFim": "09:15:00",
  "horaInicio": "09:00:00",
  "idLocalAgenda": 10919,
  "idOrigemPaciente": 69210,
  "idPaciente": 1398881,
  "idPacienteConvenio": 1656570,
  "idPessoaExecutor": 1405079,
  "idRotulo": 68780,
  "idTipoConsulta": 46272,
  "notificarEmailPaciente": true,
  "notificarEmailProfissional": true,
  "notificarSMSPaciente": true,
  "notificarSMSProfissional": true,
  "notificarWhatsappPaciente": true,
  "observacoes": "Consulta de rotina",
  "procedimentos": [
    {
      "idEspecialidade": 1616148,
      "idTipoProcedimento": 133964,
      "quantidade": 1
    }
  ],
  "salaEspera": "CRIAR",
  "status": "AGENDADO",
  "telefoneCelularPaciente": "(47) 99999-9999"
}
```

**Campos obrigatórios:**
- `data`: Data do agendamento no formato YYYY-MM-DD
- `horaInicio`: Hora de início no formato HH:MM:SS
- `horaFim`: Hora de término no formato HH:MM:SS
- `idLocalAgenda`: ID do local da agenda (use 10919)
- `idOrigemPaciente`: ID da origem do paciente (use 69210)
- `idPaciente`: ID do paciente
- `idPacienteConvenio`: ID do convênio do paciente
- `idPessoaExecutor`: ID da pessoa do executor (médico)
- `idRotulo`: ID do rótulo (use 68780)
- `idTipoConsulta`: ID do tipo de consulta (use 46272)
- `procedimentos`: Lista de procedimentos
  - `idEspecialidade`: ID da especialidade
  - `idTipoProcedimento`: ID do tipo de procedimento
  - `quantidade`: Quantidade (use 1)

### Listar Agendamentos

Retorna uma lista de agendamentos para um paciente específico.

**Endpoint:** `GET /api/v1/agendamentos`

**Parâmetros de consulta:**
- `codigo_paciente` (obrigatório): ID do paciente
- `data_inicial` (obrigatório): Data inicial no formato YYYY-MM-DD
- `data_final` (obrigatório): Data final no formato YYYY-MM-DD

**Exemplo de requisição:**
```
GET /api/v1/agendamentos?codigo_paciente=1398881&data_inicial=2025-04-01&data_final=2025-06-01
```

**Exemplo de resposta:**
```json
{
  "pagina": 0,
  "totalPaginas": 1,
  "lista": [
    {
      "id": 89706156,
      "idPessoaExecutor": 1405079,
      "idPaciente": 1398881,
      "idOrigemPaciente": 69210,
      "idTipoConvenio": 12642,
      "idTipoConsulta": 46272,
      "idLocalAgenda": 10919,
      "status": "AGENDADO",
      "data": "2025-04-08",
      "horaInicio": "09:00:00",
      "horaFim": "09:15:00",
      "observacoes": "Consulta de rotina",
      "telefoneCelularPaciente": "(47) 99999-9999",
      "encaminhamento": "Atendimento gerado via API",
      "idRotulo": 68780,
      "procedimentos": [
        {
          "idTipoProcedimento": 133964,
          "idEspecialidade": 1616148,
          "quantidade": 1,
          "id": 78624640,
          "nome": "Consulta"
        }
      ]
    }
  ]
}
```

## Fluxo Completo de Agendamento

Para realizar um agendamento completo, siga estes passos:

1. **Verificar se o paciente existe**
   - Use o endpoint `GET /api/v1/pacientes` com filtros de nome ou CPF
   - Se o paciente não existir, crie-o com `POST /api/v1/pacientes`

2. **Associar convênio ao paciente (se for um paciente novo)**
   - Use o endpoint `POST /api/v1/pacientes/{id_paciente}/convenios`
   - Se o paciente não informar um convênio, use o convênio Particular (ID: 12642)

3. **Buscar médicos disponíveis**
   - Use o endpoint `GET /api/v1/executores` com filtros opcionais

4. **Verificar disponibilidade de horários**
   - Use o endpoint `GET /api/v1/disponibilidade` com o ID do médico escolhido

5. **Criar o agendamento**
   - Use o endpoint `POST /api/v1/agendamentos` com todos os dados necessários

6. **Confirmar o agendamento**
   - Use o endpoint `GET /api/v1/agendamentos` para verificar se o agendamento foi criado com sucesso
