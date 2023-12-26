"use client";

import { createContext, useContext, useMemo, useState } from "react";
import { FrontendAPI } from "@/shared/axios";

const AuthContext = createContext();

const AuthContextProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authError, setAuthError] = useState(null);
  const [authReady, setAuthReady] = useState(true);

  //sign up
  const signup = async (email, password, name) => {
    await FrontendAPI.post("/signup/", { email, password, name })
      .then((res) => {
        login(email, password);
      })
      .catch((err) => {
        if (err.name) {
          setAuthError(err.name[0]);
        } else if (err.email) {
          setAuthError(err.email[0]);
        } else if (err.password) {
          setAuthError(err.password[0]);
        }
      });
  };

  //login
  const login = async (email, password) => {
    await FrontendAPI.post("/login", { email, password })
      .then((res) => {
        checkUserLoggedIn();
      })
      .catch((err) => {
        setAuthError(err.detail);
      });
  };
  // logout
  const logout = async () => {
    await FrontendAPI.get("/logout/").then((res) => {
      setUser(null);

      //remove user from redux
    });
  };

  //clear user
  const checkUserLoggedIn = async () => {
    await FrontendAPI.get("/user/")
      .then((res) => {
        setUser(res.user);
        //set user to redux
      })
      .catch((err) => {
        // set user to null in redux
        setUser(null);
      });
  };

  const clearUser = () => {
    // clear user form redux
    setUser(null);
  };
  const value = useMemo(() => {
    return { user, authError, login, signup, clearUser, logout };
  });

  return (
    <AuthContext.Provider value={value}>
      {authReady && children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;

export const useAuth = () => useContext(AuthContext);
