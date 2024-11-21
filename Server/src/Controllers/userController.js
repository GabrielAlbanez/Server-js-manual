const userService = require('../Services/userService');

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