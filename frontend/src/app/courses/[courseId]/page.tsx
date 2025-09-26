"use client";

import Graph from "@/components/Graph";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import type { Course } from "@/types/course";

export default function CoursePage() {
    const { courseId } = useParams();
    const [course, setCourse] = useState<Course | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch(`http://localhost:8000/courses/${courseId}`)
            .then((r) => r.json())
            .then((data: Course) => {
                setCourse(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [courseId]);

    if (typeof courseId !== "string") return null;
    if (loading) return <div className="p-4">Loading courses...</div>;
    if (error)
        return (
            <div className="p-4 text-red-600">
                Failed to load course: {error}
            </div>
        );

    return (
        <main className="flex flex-col min-h-screen bg-gray-100">
            <header className="p-6 border-b bg-white shadow-sm">
                <h1 className="text-3xl font-bold text-black">
                    {course?.name}
                </h1>
                {course?.description && (
                    <p className="text-lg text-gray-700 mt-2">
                        {course.description}
                    </p>
                )}
                {course?.concepts?.length > 0 && (
                    <ul className="flex flex-wrap gap-2 mt-4">
                        {course.concepts.map((c) => (
                            <li
                                key={c.name}
                                className="px-2 py-1 text-sm bg-gray-100 border rounded text-gray-700"
                            >
                                {c.name}
                            </li>
                        ))}
                    </ul>
                )}
            </header>

            <section className="flex-1 p-6">
                <div className="w-full h-full border rounded-lg bg-white shadow">
                    <Graph courseId={decodeURIComponent(courseId)} />
                </div>
            </section>
        </main>
    );
}
