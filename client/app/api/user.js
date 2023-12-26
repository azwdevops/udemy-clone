import { BackendAPI } from "@/shared/axios";
import cookie from "cookie";
import refreshToken from "./refreshToken";

export default async (req, res) => {
  if (req.method === "GET") {
    if (!req.headers.cookie) {
      res.status(401).json({ message: "Not authorized" });
      return;
    }
    let { refresh_token, access_token } = cookie.parse(req.headers.cookie);
    if (!refresh_token) {
      res.status(401).json({ message: "Not authorized" });
      return;
    }
    if (!access_token) {
      // refresh the access token
      await refreshToken(req, res)
        .then((data) => {
          access_token = data;
        })
        .catch((err) => {
          res.status(401).json({ message: `Not authorized` });
        });
    }
    await BackendAPI.get(`auth/users/me/`, {
      headers: { Authorization: `Token ${access_token_token}` },
    })
      .then((data) => {
        res.status(200).json({ data });
        return data;
      })
      .catch((err) => {
        res.status(401).json({ err });
      });
  } else {
    res.setHeader("Allow", ["GET"]);
    res.status(403).json({ message: `Method ${req.method} is not allowed` });
  }
};
