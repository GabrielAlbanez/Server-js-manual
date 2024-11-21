const userService = require('../Services/userService');

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