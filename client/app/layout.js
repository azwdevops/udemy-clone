import { Navbar } from "@/components";
import "./globals.css";
import AuthContextProvider from "@/context/AuthContext";
import { ToastContainer } from "react-toastify";
import CartContextProvider from "@/context/CartContext";
import Footer from "@/components/Footer";
// import "react-toastify/dist/ReactToastify.css";

export const metadata = {
  title: "Udemy Clone",
  description: "udemy clone created with django and nextjs",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="font-primary">
        <AuthContextProvider>
          <CartContextProvider>
            {/* Navbar goes here */}
            <Navbar />
            {children}
            {/* footer goes here */}
            <Footer />
          </CartContextProvider>
        </AuthContextProvider>
      </body>
    </html>
  );
}
