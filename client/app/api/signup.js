import { BackendAPI } from "@/shared/axios";

export default async (req, res) => {
  if (req.method === "POST") {
    const { name, email, password } = req.body;
    await BackendAPI.post(`/auth/users/`, { name, email, password })
      .then((data) => {
        res.status(201).json(data);
      })
      .catch((err) => {
        res.setHeader("Allow", ["POST"]);
        res.status(400).json(err);
      });
  } else {
    return res.status(400).json({ message: `${res.method} is not allowed` });
  }
};
