"use client";

import { ReactNode } from "react";

export default function PageLayout({
    title,
    description,
    children,
}: {
    title: string;
    description?: string;
    children: ReactNode;
}) {
    return (
        <main className="flex flex-col min-h-screen bg-gray-100">
            <header className="p-6 border-b bg-white shadow-sm">
                <h1 className="text-2xl font-bold text-black">{title}</h1>
                {description && (
                    <p className="text-gray-700 mt-2">{description}</p>
                )}
            </header>

            <section className="flex-1 p-6">{children}</section>
        </main>
    );
}
