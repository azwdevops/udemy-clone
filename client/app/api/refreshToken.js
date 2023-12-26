import { BackendAPI } from "@/shared/axios";
import cookie from "cookie";

export default async (req, res) => {
  if (
    req.method === "GET" ||
    req.url === "/api/payments/" ||
    req.url === "/api/addComment/"
  ) {
    if (!req.headers.cookie) return;
    const { refresh_token } = cookie.parse(req.headers.cookie);
    if (!refresh_token) return;
    await BackendAPI.post(`/auth/jwt/refresh/`, { refresh: refresh_token })
      .then((data) => {
        res.setHeader(
          "Set-Cookie",
          cookie.serialize("access_token", data.access, {
            httpOnly: true,
            secure: process.env.NODE_ENV !== "development",
            maxAge: 60 * 60 * 24,
            sameSite: "strict",
            path: "/",
          })
        );
        return data.access;
      })
      .catch((err) => {
        return;
      });
  } else {
    return;
  }
};
