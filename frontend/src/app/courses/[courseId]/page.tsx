"use client"

import Graph from "@/components/Graph";
import { useParams } from "next/navigation";

export default function CoursePage() {
    const { courseId } = useParams();
    if (typeof courseId !== "string") return null;

    return (
        <main className="flex min-h-screen items-center justify-center bg-gray-100">
            <Graph courseId={decodeURIComponent(courseId)} />
        </main>
    );
}
