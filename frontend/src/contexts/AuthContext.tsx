import React, { createContext, useContext, useState } from 'react';

interface User {
  id: string;
  email: string;
  area: string;
  role: 'admin' | 'officer';
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, area: string, role: 'admin' | 'officer') => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock user storage
const users: { [key: string]: { password: string; user: User } } = {
  'admin@example.com': {
    password: 'admin123',
    user: {
      id: '1',
      email: 'admin@example.com',
      area: 'Mumbai',
      role: 'admin'
    }
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const signUp = async (email: string, password: string, area: string, role: 'admin' | 'officer') => {
    setLoading(true);
    try {
      if (users[email]) {
        throw new Error('User already exists');
      }

      const newUser: User = {
        id: Math.random().toString(36).substr(2, 9),
        email,
        area,
        role
      };

      users[email] = {
        password,
        user: newUser
      };
    } finally {
      setLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      const userRecord = users[email];
      if (!userRecord || userRecord.password !== password) {
        throw new Error('Invalid email or password');
      }
      setUser(userRecord.user);
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
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
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};