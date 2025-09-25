import Link from "next/link";
import type { Course } from "@/types/course";

export default function CoursesList({ courses }: { courses: Course[] }) {
    if (courses.length === 0) {
        return <div className="text-gray-600">No courses available.</div>;
    }

    return (
        <ul className="space-y-3">
            {courses.map((course) => (
                <li
                    key={course.id}
                    className="p-4 border border-gray-200 rounded-lg bg-white shadow hover:shadow-md transition"
                >
                    <Link href={`/courses/${course.id}`}>
                        <h2 className="text-lg font-semibold text-black">{course.name}</h2>
                        {course.description && (
                            <p className="text-sm text-gray-700">{course.description}</p>
                        )}
                    </Link>
                </li>
            ))}
        </ul>
    );
}
