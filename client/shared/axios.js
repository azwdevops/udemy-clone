import axios from "axios";

const FrontendAPI = axios.create({ baseURL: "http://localhost:3000/api" });
FrontendAPI.interceptors.request.use((req) => {
  req.headers.Accept = "application/json";
  return req;
});

const BackendAPI = axios.create({ baseURL: "http://localhost:8000/api/v1" });
BackendAPI.interceptors.request.use((req) => {
  req.headers.Accept = "application/json";
  return req;
});

export { FrontendAPI, BackendAPI };
