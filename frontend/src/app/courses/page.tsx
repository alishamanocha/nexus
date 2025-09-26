"use client";

import { useEffect, useState } from "react";
import CoursesList from "@/components/CoursesList";
import type { Course } from "@/types/course";
import PageLayout from "@/components/PageLayout";

export default function CoursesPage() {
    const [courses, setCourses] = useState<Course[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/courses")
            .then((r) => {
                if (!r.ok) throw new Error(`${r.status} - ${r.statusText}`);
                return r.json();
            })
            .then((data: Course[]) => {
                setCourses(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="p-4">Loading courses...</div>;
    if (error)
        return (
            <div className="p-4 text-red-600">
                Failed to load courses: {error}
            </div>
        );

    return (
        <PageLayout title="Courses">
            <CoursesList courses={courses} />
        </PageLayout>
    );
}
