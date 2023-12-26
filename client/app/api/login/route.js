import { BackendAPI } from "@/shared/axios";
import cookie from "cookie";
import { NextResponse } from "next/server";

export async function POST(req) {
  if (req.method === "POST") {
    const { email, password } = req.body;
    await BackendAPI.post(`/auth/jwt/create/`, { email, password })
      .then((response) => {
        //set server side token
        NextResponse.setHeader("Set-Cookie", [
          cookie.serialize("refresh_token", response.refresh, {
            httpOnly: true,
            secure: process.env.NODE_ENV !== "development",
            maxAge: 60 * 60 * 24,
            sameSite: "strict",
            path: "/",
          }),
          cookie.serialize("access_token", response.access, {
            httpOnly: true,
            secure: process.env.NODE_ENV !== "development",
            maxAge: 60,
            sameSite: "strict",
            path: "/",
          }),
        ]);

        return NextResponse.json({}, { status: 200 });
      })
      .catch((err) => {
        return NextResponse.json({ err }, { status: 401 });
      });
  } else {
    // NextResponse.setHeader("Allow", ["POST"]);
    return NextResponse.json(
      { message: `${req.method} is not allowed` },
      { status: 400 }
    );
  }
}
