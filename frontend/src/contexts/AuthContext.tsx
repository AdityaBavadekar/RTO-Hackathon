// import { ca } from "date-fns/locale";
import React, { createContext, useContext, useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";

interface User {
  id: string;
  email: string;
  area: string;
  role: "admin" | "officer";
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<Boolean>;
  signUp: (
    email: string,
    password: string,
    area: string,
    role: "admin" | "officer"
  ) => Promise<void>;
  signOut: () => Promise<void>;
}
// const navigate = useNavigate();
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock user storage
// const users: { [key: string]: { password: string; user: User } } = {
//   "admin@example.com": {
//     password: "admin123",
//     user: {
//       id: "1",
//       email: "admin@example.com",
//       area: "Mumbai",
//       role: "admin",
//     },
//   },
// };

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const id = localStorage.getItem("rto_id");
    const username = localStorage.getItem("rto_username");
    if (id && username) {
      const rtoCenter = JSON.parse(localStorage.getItem("rto_center") || "{}");
      setUser({
        id,
        ...rtoCenter,
        email: username,
        area: rtoCenter.rto_address,
        role: "admin",
      });
    }
  }, []);

  const signUp = async (
    email: string,
    password: string,
    area: string
    // role: "admin" | "officer"
  ) => {
    setLoading(true);
    try {
      fetch("http://192.168.58.4:8000/api/rto/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password: password,
          rto_name: "RTO Center @[id]@", // Dynamic name
          rto_address: area,
          rto_lat: 24.824907,
          rto_long: -1.909589,
          rto_website: "https://rto-center-web.com",
          rto_main_email: email.endsWith("@example.com")
            ? email
            : "rto_test@gmail.com",
          rto_contact_number: "+916652063284",
          rto_office_hours: "10:00 AM - 5:00 PM",
          rto_report_to_mails: [
            "nikhil.joshi@gmail.com",
            "anay.rtol1@gmail.com",
          ],
          rto_metadata: {
            office_type: "Regional",
            established_year: 2024,
            services: ["Vehicle Registration", "Road Tax Collection"],
          },
        }),
      }).then(async (response) => {
        const data = await response.json();
        if (response.status == 200) {
          setUser(data.rto_center);
          localStorage.setItem("rto_id", data.rto_id);
          localStorage.setItem("rto_username", data.rto_username);
          localStorage.setItem("rto_center", JSON.stringify(data.rto_center));
        }
        throw new Error(data.message);
      });
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await fetch(
        "http://192.168.58.4:8000/api/rto/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username: email, password }),
        }
      );
      const data = await response.json();
      if (response.status == 200) {
        setUser(data.rto_center);
        localStorage.setItem("rto_id", data.rto_id);
        localStorage.setItem("rto_username", data.rto_username);
        setLoading(false);
        return true;
      }
      throw new Error(data.message);
    } catch (e) {
      setLoading(false);
      return false;
    }
  };

  const signOut = async () => {
    localStorage.removeItem("rto_id");
    localStorage.removeItem("rto_username");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
