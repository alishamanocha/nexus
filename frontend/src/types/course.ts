export interface Concept {
    id: string;
    name: string;
    description: string;
    course_id: string;
    prerequisites: string[];
}

export interface Course {
    id: string;
    name: string;
    description: string;
    concepts: Concept[];
}
