import cookie from "cookie";

export default async (req, res) => {
  // remove auth tokens

  if (req.method === "POST") {
    res.setHeader("Set-Cookie", [
      cookie.serialize("refresh_token", "", {
        httpOnly: true,
        secure: process.env.NODE_ENV !== "development",
        maxAge: new Date(0),
        sameSite: "strict",
        path: "/",
      }),
      cookie.serialize("access_token", "", {
        httpOnly: true,
        secure: process.env.NODE_ENV !== "development",
        maxAge: new Date(0),
        sameSite: "strict",
        path: "/",
      }),
    ]);
    res.status(204).json({});
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(403).json({ message: `Method ${req.method} is not allowed` });
  }
};
