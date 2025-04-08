import axios from 'axios';

const API_BASE_URL = 'https://mcp-clinica-nas-nuvens.onrender.com/api/v1';

interface Tool {
  name: string;
  description: string;
  parameters: Record<string, {
    type: string;
    required: boolean;
    description?: string;
  }>;
  execute: (params: any) => Promise<any>;
}

const tools: Tool[] = [
  {
    name: "listar_pacientes",
    description: "Lista todos os pacientes da clínica",
    parameters: {
      cnpj: {
        type: "string",
        required: true,
        description: "CNPJ da clínica"
      },
      nome: {
        type: "string",
        required: false,
        description: "Filtro por nome do paciente"
      },
      cpf: {
        type: "string",
        required: false,
        description: "Filtro por CPF do paciente"
      }
    },
    execute: async (params) => {
      const response = await axios.get(`${API_BASE_URL}/pacientes`, { params });
      return response.data;
    }
  },
  {
    name: "criar_paciente",
    description: "Cria um novo paciente na clínica",
    parameters: {
      cnpj: {
        type: "string",
        required: true,
        description: "CNPJ da clínica"
      },
      nome: {
        type: "string",
        required: true,
        description: "Nome do paciente"
      },
      cpf: {
        type: "string",
        required: true,
        description: "CPF do paciente"
      },
      data_nascimento: {
        type: "string",
        required: true,
        description: "Data de nascimento (YYYY-MM-DD)"
      },
      telefone: {
        type: "string",
        required: true,
        description: "Telefone do paciente"
      },
      email: {
        type: "string",
        required: true,
        description: "Email do paciente"
      }
    },
    execute: async (params) => {
      const response = await axios.post(`${API_BASE_URL}/pacientes`, params);
      return response.data;
    }
  },
  {
    name: "listar_executores",
    description: "Lista todos os médicos/executores disponíveis",
    parameters: {
      cnpj: {
        type: "string",
        required: true,
        description: "CNPJ da clínica"
      },
      id_especialidade: {
        type: "number",
        required: false,
        description: "ID da especialidade"
      },
      id_tipo_convenio: {
        type: "number",
        required: false,
        description: "ID do tipo de convênio"
      }
    },
    execute: async (params) => {
      const response = await axios.get(`${API_BASE_URL}/executores`, { params });
      return response.data;
    }
  }
];

// Função para listar as tools disponíveis
async function listTools() {
  return { tools: tools.map(({ name, description, parameters }) => ({ name, description, parameters })) };
}

// Função para executar uma tool
async function executeTool(toolName: string, parameters: any) {
  const tool = tools.find(t => t.name === toolName);
  if (!tool) {
    throw new Error(`Tool '${toolName}' not found`);
  }

  // Validar parâmetros obrigatórios
  for (const [key, param] of Object.entries(tool.parameters)) {
    if (param.required && !parameters[key]) {
      throw new Error(`Missing required parameter: ${key}`);
    }
  }

  return await tool.execute(parameters);
}

// Processar entrada e saída padrão
process.stdin.setEncoding('utf-8');
let inputBuffer = '';

process.stdin.on('data', async (chunk) => {
  inputBuffer += chunk;
  const lines = inputBuffer.split('\n');
  
  // Processa todas as linhas completas
  for (let i = 0; i < lines.length - 1; i++) {
    const line = lines[i];
    try {
      const request = JSON.parse(line);
      let response;

      if (request.type === 'listTools') {
        response = await listTools();
      } else if (request.type === 'executeTool') {
        response = await executeTool(request.tool, request.parameters);
      } else {
        throw new Error(`Unknown request type: ${request.type}`);
      }

      process.stdout.write(JSON.stringify({ id: request.id, result: response }) + '\n');
    } catch (error: any) {
      process.stdout.write(JSON.stringify({ id: request.id, error: error.message }) + '\n');
    }
  }

  // Mantém o resto no buffer
  inputBuffer = lines[lines.length - 1];
}); 