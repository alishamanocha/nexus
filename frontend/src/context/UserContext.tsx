"use client";
import { createContext, useContext, useState, useEffect } from "react";
import type { User } from "@/types/user";

const UserContext = createContext<{
    user: User | null;
    setUser: (u: User | null) => void;
    refreshUser: () => Promise<void>;
}>({
    user: null,
    setUser: () => {},
    refreshUser: async () => {},
});

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User>(null);

    const refreshUser = async () => {
        try {
            const res = await fetch("http://localhost:8000/me", {
                credentials: "include",
            });
            if (res.ok) {
                const data = await res.json();
                setUser(data);
            } else {
                setUser(null);
            }
        } catch {
            setUser(null);
        }
    };

    useEffect(() => {
        refreshUser();
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser, refreshUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useCurrentUser = () => useContext(UserContext);
