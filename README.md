# MindWork: AI & IoT for Mental Health

![Technology](https://img.shields.io/badge/Tech-.NET%208%20%7C%20Python%20%7C%20Gemini-blue) ![Focus](https://img.shields.io/badge/Focus-IoT%20%26%20GenAI-purple)

O **MindWork** é uma plataforma integrada que monitora a saúde emocional de colaboradores utilizando **Visão Computacional (IoT)** e fornece suporte psicológico personalizado através de **IA Generativa (Google Gemini)**.

---

## Arquitetura da Solução

O sistema foi desenhado para demonstrar a integração real entre três pilares tecnológicos:

1. **Backend (.NET 8):** O núcleo do sistema. Uma API RESTful que gerencia autenticação, banco de dados e regras de negócio.
2. **Edge Computing / IoT (Python):** Um sensor inteligente (simulado por webcam) que usa **Deep Learning (DeepFace)** para detectar emoções em tempo real e enviá-las para a nuvem.
3. **Inteligência Artificial Generativa:** Integração com o **Google Gemini 2.5 Flash**, que atua como um "Psicólogo Virtual", cruzando dados biométricos (IoT) com autoavaliações para gerar insights personalizados.

---

## Tecnologias Utilizadas

### Backend (API)
- **Linguagem:** C# (.NET 8)
- **Framework:** ASP.NET Core Web API
- **Banco de Dados:** SQL Server (Entity Framework Core)
- **Autenticação:** JWT Bearer
- **Documentação:** Swagger UI

### IoT (Cliente)
- **Linguagem:** Python 3.10+
- **Bibliotecas:**
  - `deepface` (Análise Facial)
  - `opencv-python` (Captura de Vídeo)
  - `requests` (Comunicação HTTP)

### Inteligência Artificial
- **Modelo:** Google Gemini 2.5 Flash
- **Tipo:** LLM (Large Language Model) via REST API

---

## Configuração do Ambiente

Siga estes passos para rodar a solução completa em sua máquina.

### 1. Pré-requisitos

- [.NET SDK 8.0](https://dotnet.microsoft.com/download)
- [Python 3.10 ou superior](https://www.python.org/downloads/)
- SQL Server (Express ou Developer) rodando localmente

### 2. Configuração da API (.NET)

1.  **Clone o repositório:**
    Abra o terminal na pasta onde deseja salvar o projeto e execute:
    ```powershell
    git clone https://github.com/tcguus/MindWork-API
    cd mindwork-api/MindWork.Api
    ```

2.  **Restaure as dependências:**
    Baixe os pacotes NuGet necessários para o projeto rodar:
    ```powershell
    dotnet restore
    ```

3.  **Crie o Banco de Dados:**
    Execute as migrações para gerar as tabelas no SQL Server:
    ```powershell
    dotnet ef database update
    ```

4.  **Inicie a API:**
    Use o perfil HTTPS para garantir a segurança e a porta correta:
    ```powershell
    dotnet run --launch-profile https
    ```
    *A API estará disponível em: `https://localhost:7034`*

### 3. Configuração do IoT (Python)

1.  Acesse a pasta raiz do projeto (onde está o arquivo `iot_sensor.py`).
2.  Instale as dependências necessárias:
    ```powershell
    pip install deepface opencv-python requests tf-keras
    ```
3.  Verifique se a URL da API no script (`API_URL`) está apontando para `https://localhost:7034/api/v1`.

---

## Roteiro de Teste

Para validar a integração completa (IoT → API → IA), siga este roteiro. Ideal para apresentações e gravação de vídeos.

### FASE 1: Preparação (Swagger)

Acesse `https://localhost:7034/swagger` e utilize o endpoint **POST /api/v1/Auth/register** para criar os 3 atores do sistema:

**Dispositivo IoT (Usuário de máquina):**
- Email: `iot.device@mindwork.com`
- Senha: `Password123!`
- Role: `Collaborator`

**Gestor (Visualizador de dados):**
- Email: `maria.gestora@empresa.com`
- Senha: `Password123!`
- Role: `Manager`

**Colaborador (Usuário final):**
- Email: `joao.silva@empresa.com`
- Senha: `Password123!`
- Role: `Collaborator`

### FASE 2: Captura IoT (Visão Computacional)

1. Com a API rodando, abra um novo terminal.
2. Execute o sensor: `python iot_sensor.py`.
3. A webcam abrirá. Faça uma expressão facial (ex: Triste ou Bravo).
4. Aguarde a confirmação no terminal: `✅ --> Evento enviado: sad`.
5. Pode fechar o script.

### FASE 3: Validação de Dados (Visão do Gestor)

1. No Swagger, faça **Login** (POST /auth/login) com a Maria Gestora.
2. Copie o **Token JWT** gerado.
3. Clique no botão **Authorize** (cadeado) e cole: `Bearer SEU_TOKEN`.
4. Chame o endpoint **GET /api/v1/WellnessEvents**.
5. **Resultado:** O JSON retornará o evento `emotion_detected` com a emoção capturada. Isso prova a integração IoT.

### FASE 4: Inteligência Artificial (Visão do Colaborador)

1. **Importante:** Clique em **Logout** no botão Authorize do Swagger.
2. Faça **Login** (POST /auth/login) com o João Silva.
3. Copie o novo Token, clique em **Authorize** e cole: `Bearer TOKEN_DO_JOAO`.
4. Envie uma autoavaliação em **POST /api/v1/SelfAssessments**:

```json
{
  "mood": 2,
  "stress": 5,
  "workload": 5,
  "notes": "A câmera me viu cansado e estou com muitas entregas."
}
```

5. Chame a IA em **GET /api/v1/Ai/recommendations/me**.
6. **Resultado Final:** A API retornará recomendações geradas dinamicamente pelo Gemini 2.5 Flash, correlacionando sua autoavaliação com os dados do IoT.

---

## Solução de Problemas

**Erro 404 (Gemini Model Not Found):**  
Certifique-se de que o `AiService.cs` está configurado para usar `gemini-2.5-flash` ou `gemini-2.0-flash`, pois versões antigas (1.0/1.5) podem ser descontinuadas.

**Erro de Certificado SSL no Python:**  
O script `iot_sensor.py` já inclui `verify=False` para aceitar o certificado de desenvolvimento local. Apenas ignore os avisos de "Unverified HTTPS request".

**Erro 500 ao salvar Autoavaliação:**  
Isso ocorre se o Token JWT pertencer a um usuário que foi deletado do banco. Faça Login novamente para gerar um Token válido.

---

## Estrutura de Arquivos

```
MindWork/
├── MindWork.Api/                 # Projeto Backend Principal
│   ├── Controllers/              # API Endpoints
│   ├── Domain/                   # Regras de Negócio
│   ├── Services/AiService.cs     # Integração com Google Gemini
│   └── iot_sensor.py             # Script Cliente Python (IoT)
└── README.md                     # Documentação
```

---

## Nossos integrantes
- **Gustavo Camargo de Andrade**
- RM555562
- 2TDSPF
-------------------------------------------
- **Rodrigo Souza Mantovanello**
- RM555451
- 2TDSPF
-------------------------------------------
- **Leonardo Cesar Rodrigues Nascimento**
- RM558373
- 2TDSPF
