const prisma = require("../Model/PrismaClient");
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