const userService = require('../Services/userService');
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