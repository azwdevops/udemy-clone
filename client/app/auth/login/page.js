"use client";

import React, { useContext, useEffect, useState } from "react";

import Link from "next/link";
import { useAuth } from "../../../context/AuthContext";
import { toast } from "react-toastify";
import cookie from "cookie";
import FormInput from "@/components/auth/FormInput";
import AuthBtn from "@/components/auth/AuthBtn";
import { useRouter } from "next/navigation";

const login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authReady, setAuthReady] = useState(false);

  const { login, authError, clearUser } = useAuth();
  const router = useRouter();

  useEffect(() => clearUser(), []);

  useEffect(() => {
    const checkCookies = async () => {
      const res = await fetch("/api/refreshToken"); // Replace with your API route or endpoint
      if (res.ok) {
        const cookies = await res.json();
        if (cookies && cookies.refresh_token) {
          router.push("/"); // Redirect if refresh_token exists
        }
      }
    };

    checkCookies();
  }, [router]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setAuthReady(true);
    await login({ email, password });
    setAuthReady(false);
  };

  useEffect(() => {
    authError && toast.error(authError);
  }, [authError]);

  return (
    <section className="flex justify-center pt-20 min-h-screen">
      <div className="w-10/12 md:w-7/12 lg:w-4/12">
        <h2 className="text-xl md:text-2xl font-medium py-3 border-b pl-5">
          Log In and Start Learning!
        </h2>

        <form action="" onSubmit={handleSubmit} className="w-full py-4">
          <FormInput
            inputVal={email}
            setInput={setEmail}
            type="email"
            iconName="mail"
            placeholder="Email"
            name="email"
          />
          <FormInput
            inputVal={password}
            setInput={setPassword}
            type="password"
            iconName="lock-closed"
            placeholder="Password"
            name="password"
          />

          <AuthBtn
            disabled={authReady}
            action={!authReady ? "Log In" : "Please wait..."}
          />

          <p className="md:text-lg my-2 text-center ">
            Do not have an account?{" "}
            <span className="text-blue-600 font-medium">
              <Link href="/auth/signup">Sign Up</Link>
            </span>
          </p>
        </form>
      </div>
    </section>
  );
};

// export const getServerSideProps = async ({ req, res }) => {
//   if (req.headers.cookie) {
//     let cookies = cookie.parse(req.headers.cookie);

//     if (cookies && cookies.refresh_token) {
//       return {
//         redirect: {
//           destination: "/",
//           permanent: false,
//         },
//       };
//     }
//   }

//   return {
//     props: {},
//   };
// };

export default login;
