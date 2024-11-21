
# Bem-vindo ao Guia de Configuração do Projeto!

Olá! Este é um guia passo a passo para configurar seu projeto Node.js com Prisma, SQLite e Express. Ao final, você terá um ambiente completo com estrutura de rotas, banco de dados, seed e testes.

# Passo 1: Configuração do Projeto

1. Crie uma pasta para o projeto e acesse-a.
   ```bash
   mkdir meu-projeto && cd meu-projeto
   ```
2. Inicialize o Node.js no projeto:
   ```bash
   npm init -y
   ```

---

# Passo 2: Instalação de Dependências

1. Instale as dependências principais:
   ```bash
   npm install express dotenv bcrypt jsonwebtoken @prisma/client sqlite3
   ```
2. Instale as dependências de desenvolvimento:
   ```bash
   npm install --save-dev nodemon prisma
   ```

---

# Passo 3: Configuração do Prisma

1. Inicialize o Prisma no projeto:
   ```bash
   npx prisma init
   ```

2. Configure o arquivo `schema.prisma` com o seguinte código:
   ```prisma
   generator client {
     provider = "prisma-client-js"
   }

   datasource db {
     provider = "sqlite"
     url      = "file:./dev.db"
   }

   model User {
     id        String   @id @default(uuid()) // Gera um UUID automaticamente
     name      String
     email     String   @unique
     password  String
     createdAt DateTime @default(now())
   }
   ```

3. No arquivo `.env`, adicione:
   ```env
   DATABASE_URL="file:./dev.db"
   ```

4. Execute o seguinte comando para criar as tabelas no banco:
   ```bash
   npx prisma db push
   ```

---

# Passo 4: Criação da Estrutura do Projeto

1. Crie as pastas e arquivos necessários usando os comandos abaixo:
   ```bash
   mkdir src
   mkdir src\Controllers src\Middleware src\Model src\Routes src\Services
   echo. > src\Controllers\userController.js
   echo. > src\Middleware\Auth.js
   echo. > src\Middleware\checkDuplicateUser.js
   echo. > src\Middleware\ChekUSerId.js
   echo. > src\Model\PrismaClient.js
   echo. > src\Routes\authRoutes.js
   echo. > src\Routes\userRouter.js
   echo. > src\Services\userService.js
   echo. > src\app.js
   echo. > src\server.js
   ```

2. **Rode o script Python** para popular os arquivos com código automaticamente.

---



# Arquivo Python para Configuração Automática

O arquivo Python anexo cria toda a estrutura do projeto, incluindo o `seed.js`, as rotas e o teste automático.

[Baixar Script Python](create_full_project_structure_with_updates.py)

---

**Dica:** Após seguir todos os passos, seu projeto estará configurado e pronto para uso. Divirta-se programando!

