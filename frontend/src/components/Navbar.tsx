import Link from "next/link";
import LogoutButton from "@/components/LogoutButton";

export default function Navbar() {
    return (
        <nav className="fixed top-0 left-0 right-0 bg-blue-500 text-white px-6 py-3 shadow-md">
            <div className="mx-auto flex items-center justify-between">
                <Link
                    href="/"
                    className="text-xl font-bold hover:text-gray-200"
                >
                    Nexus
                </Link>
                <div className="flex gap-4">
                    <Link href="/courses" className="hover:text-gray-200">
                        Courses
                    </Link>
                    <Link href="/profile" className="hover:text-gray-200">
                        Profile
                    </Link>
                    <LogoutButton />
                </div>
            </div>
        </nav>
    );
}
