"use client";

import { useRouter } from "next/navigation";
import { useCurrentUser } from "@/context/UserContext";

export default function LogoutButton() {
    const router = useRouter();
    const { setUser } = useCurrentUser();

    const handleLogout = async () => {
        try {
            const res = await fetch("http://localhost:8000/logout", {
                method: "POST",
                credentials: "include",
            });

            if (res.ok) {
                setUser(null);
                router.push("/login");
            } else {
                console.error("Logout failed");
            }
        } catch (err) {
            console.error("Logout failed:", err);
        }
    };

    return (
        <button
            onClick={handleLogout}
            className="text-white hover:text-gray-200 cursor-pointer"
        >
            Logout
        </button>
    );
}
