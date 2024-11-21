const express = require("express");
const userRoutes = require("./Routes/userRouter");

const app = express();

app.use(express.json());
app.use("/users", userRoutes);

module.exports = app;