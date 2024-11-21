
import os

# Estrutura de pastas e arquivos com o código correspondente
project_structure = {
    ".env": """JWT_SECRET="(@43147109)"
PORT=3000""",


    "package.json": """{
  "name": "project",
  "version": "1.0.0",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon ./src/server.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "bcrypt": "^5.0.1",
    "jsonwebtoken": "^8.5.1",
    "@prisma/client": "^4.0.0"
  },
  "devDependencies": {
    "nodemon": "^2.0.15"
  }
}""",



    "src": {
        "Controllers": {
            "userController.js": """const userService = require('../Services/userService');

const createUser = async (req, res) => {
  try {
    const user = await userService.createUser(req.body);
    res.status(201).json(user); 
  } catch (error) {
    res.status(400).json({ error: error.message }); 
  }
};

const getAllUsers = async (req, res) => {
  try {
    const users = await userService.getAllUsers();
    if (users && users.length > 0) {
      res.status(200).json(users); 
    } else {
      res.status(404).json({ message: 'Usuarios não encontrados' }); 
    }
  } catch (error) {
    res.status(500).json({ error: error.message }); 
  }
};

const getUserById = async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'Usuario não encontrado' }); 
    }
    res.status(200).json(user); 
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

const updateUser = async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'Usuario não encontrado' }); 
    }
    const updatedUser = await userService.updateUser(req.params.id, req.body);
    res.status(200).json(updatedUser); 
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

const deleteUser = async (req, res) => {
  try {
    const user = await userService.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ message: 'Usuario não encontrado' }); 
    }
    await userService.deleteUser(req.params.id);
    res.status(204).json({ message: 'Usuario deletado com sucesso' }); 
  } catch (error) {
    res.status(500).json({ error: error.message }); 
  }
};

module.exports = {
  createUser,
  getAllUsers,
  getUserById,
  updateUser,
  deleteUser,
};
"""
        },
        "Middleware": {
            "Auth.js": """const userService = require('../Services/userService');
const bcrypt = require('bcrypt');

const authenticateUser = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    // Verifica se o email e senha foram fornecidos
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    // Busca o usuário pelo email
    const user = await userService.getUSerByEmail(email);
    if (!user) {
      return res.status(401).json({ message: 'E-mail Ou senha Validos' });
    }

    // Verifica a senha
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'E-mail Ou senha Validos' });
    }

    // Armazena o usuário no request para uso posterior
    req.user = user;

    next(); // Continua para o próximo middleware ou controller
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = authenticateUser;
""",
            "checkDuplicateUser.js": """const userService = require('../Services/userService');

const checkDuplicateUser = async (req, res, next) => {
  try {
    const { name, email } = req.body;

    const existingUser = await userService.findUserByNameOrEmail(name) || 
                         await userService.findUserByNameOrEmail(email);

    if (existingUser) {
      return res.status(400).json({ message: 'User already exists with the given email or name.' });
    }

    next();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = checkDuplicateUser;
""",
            "ChekUSerId.js": """const userService = require('../Services/userService');

const checkUserId = async (req, res, next) => {
  try {
    const { id } = req.params;

    const user = await userService.getUserById(id);
    if (!user) {
      return res.status(404).json({ message: 'No user found with this ID' });
    }

    next();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = checkUserId;
"""
        },
        "Routes": {
            "authRoutes.js": """const express = require('express');
const jwt = require('jsonwebtoken');
const authenticateUser = require('../Middleware/Auth');

const router = express.Router();

router.post('/Login', authenticateUser, (req, res) => {
  const user = req.user;

  const payload = {
    id: user.id,
    email: user.email,
    name: user.name,
  };

  const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '1h' });

  res.status(200).json({
    message: 'Login successful',
    token,
  });
});

module.exports = router;
""",
            "userRouter.js": """const express = require("express");
const userController = require("../Controllers/userController");
const checkDuplicateUser = require("../Middleware/checkDuplicateUser");
const checkUserId = require("../Middleware/ChekUSerId");

const router = express.Router();

router.post("/CreateUser", checkDuplicateUser, userController.createUser);
router.get("/GetAllUsers", userController.getAllUsers);
router.get("/:id", checkUserId, userController.getUserById);
router.put("/:id", checkUserId, userController.updateUser);
router.delete("/:id", checkUserId, userController.deleteUser);

module.exports = router;
"""
        },
        "Services": {
            "userService.js": """const prisma = require("../Model/PrismaClient");
const bcrypt = require("bcrypt");

const createUser = async (data) => {
  const hashedPassword = await bcrypt.hash(data.password, 10);
  data.password = hashedPassword;
  return prisma.user.create({ data });
};

const getAllUsers = async () => {
  return prisma.user.findMany();
};

const getUserById = async (id) => {
  return prisma.user.findUnique({ where: { id } });
};

const updateUser = async (id, data) => {
  return prisma.user.update({
    where: { id },
    data,
  });
};

const deleteUser = async (id) => {
  return prisma.user.delete({ where: { id } });
};

const findUserByNameOrEmail = async (identifier) => {
  const user = await prisma.user.findFirst({
    where: {
      OR: [{ name: identifier }, { email: identifier }],
    },
  });

  return user;
};

const getUSerByEmail = async (email) => {
  return prisma.user.findUnique({ where: { email } });
};

module.exports = {
  createUser,
  getAllUsers,
  getUserById,
  updateUser,
  deleteUser,
  findUserByNameOrEmail,
  getUSerByEmail,
};
"""},
        
          "Model" : {
             "PrismaClient.js" : """const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

module.exports = prisma;
"""
          },
        
        "app.js": """const express = require("express");
const userRoutes = require("./Routes/userRouter");

const app = express();

app.use(express.json());
app.use("/users", userRoutes);

module.exports = app;
""",
        "server.js": """require('dotenv').config();
const app = require('./app');

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
"""
    }
}

def create_project_structure(base_path, structure):
    for folder, content in structure.items():
        folder_path = os.path.join(base_path, folder)
        if isinstance(content, dict):
            os.makedirs(folder_path, exist_ok=True)
            create_project_structure(folder_path, content)
        else:
            with open(folder_path, "w", encoding="utf-8") as file:
                file.write(content.strip())

# Caminho base do projeto
base_path = "Server"

# Criar a estrutura
create_project_structure(base_path, project_structure)

print(f"Estrutura do projeto criada dentro da pasta 'src'.")
