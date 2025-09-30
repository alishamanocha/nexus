from __future__ import annotations

from uuid import uuid4

concepts = [
    {
        "id": "limits",
        "name": "Limits",
        "description": "Understanding the behavior of functions as inputs approach a value.",
        "prerequisites": [],
        "course_id": "calculus1",
        "content": "A limit tells you what a function approaches as you approach a certain input value!",
    },
    {
        "id": "continuity",
        "name": "Continuity",
        "description": "Determining whether a function has any breaks, jumps, or holes.",
        "prerequisites": ["limits"],
        "course_id": "calculus1",
        "content": "There are three conditions for continuity of f(x) at x=a: (1) f(a) is defined, (2) lim_{x->a} f(x) exists, and (3) f(a) = lim_{x->a} f(x).",
    },
    {
        "id": "derivatives",
        "name": "Derivatives",
        "description": "The instantaneous rate of change of a function at a point.",
        "prerequisites": ["limits"],
        "course_id": "calculus1",
        "content": "A derivative measures the rate of change of a function.",
    },
    {
        "id": "chain_rule",
        "name": "Chain Rule",
        "description": "Rule for differentiating compositions of functions.",
        "prerequisites": ["derivatives"],
        "course_id": "calculus1",
        "content": "The derivative of f(g(x)) is f'(g(x))*g'(x).",
    },
    {
        "id": "implicit_diff",
        "name": "Implicit Differentiation",
        "description": "Differentiating equations not explicitly solved for one variable.",
        "prerequisites": ["derivatives", "chain_rule"],
        "course_id": "calculus1",
        "content": "For example, x^2+y^2=4 -> d/dx[x^2+y^2]=d/dx[4] -> 2x+2y*dy/dx=0 -> dy/dx=-x/y.",
    },
    {
        "id": "related_rates",
        "name": "Related Rates",
        "description": "Applying derivatives to find rates of change in related quantities.",
        "prerequisites": ["derivatives", "implicit_diff"],
        "course_id": "calculus1",
        "content": "We can use implicit differentiation to determine the rate of change of the volume of a sphere based on the rate of change of the radius, for example.",
    },
    {
        "id": "integrals",
        "name": "Integrals",
        "description": "Calculating the accumulation of quantities and areas under curves.",
        "prerequisites": ["derivatives"],
        "course_id": "calculus1",
        "content": "The integral, which physically represents the area under a curve, is the inverse operation to the derivative.",
    },
    {
        "id": "fundamental_theorem",
        "name": "Fundamental Theorem of Calculus",
        "description": "Connecting derivatives and integrals as inverse processes.",
        "prerequisites": ["derivatives", "integrals"],
        "course_id": "calculus1",
        "content": "Because differentiation and integration are inverse operations, they 'undo' each other.",
    },
]

courses = [
    {
        "id": "calculus1",
        "name": "Calculus 1",
        "description": "A basic calculus 1 course.",
        "concepts": concepts,
    },
    {
        "id": "precalculus",
        "name": "Precalculus",
        "description": "A basic precalculus course.",
        "concepts": [],
    },
]

fake_users_db: list[dict[str, str | None]] = [
    {
        "id": str(uuid4()),
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
    },
]
