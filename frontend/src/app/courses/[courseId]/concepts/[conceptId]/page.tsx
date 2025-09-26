"use client"

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { Concept } from "@/types/course";

export default function ConceptPage() {
    const { conceptId } = useParams();
    const [concept, setConcept] = useState<Concept | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch(`http://localhost:8000/concepts/${conceptId}`)
            .then((r) => r.json())
            .then((data: Concept) => {
                setConcept(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [conceptId]);

    if (typeof conceptId !== "string") return null;
    if (loading) return <div className="p-4">Loading concept...</div>
    if (error) return (
        <div className="p-4 text-red-600">
            Failed to load concept: {error}
        </div>
    )

    return (
        <main className="flex flex-col min-h-screen bg-gray-100">
            <header className="p-6 border-b bg-white shadow-sm">
                <h1 className="text-3xl font-bold text-black">{concept?.name}</h1>
                {concept?.description && (
                    <p className="text-lg text-gray-700 mt-2">{concept.description}</p>
                )}
                {concept?.content && (
                    <p className="text-lg text-gray-700 mt-2">{concept.content}</p>
                )}
            </header>
        </main>
    );
}
