const express = require("express");
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