concepts = [
    {
        "id": "limits",
        "name": "Limits",
        "description": "Understanding the behavior of functions as inputs approach a value.",
        "prerequisites": [],
        "course_id": "calculus1",
    },
    {
        "id": "continuity",
        "name": "Continuity",
        "description": "Determining whether a function has any breaks, jumps, or holes.",
        "prerequisites": ["limits"],
        "course_id": "calculus1",
    },
    {
        "id": "derivatives",
        "name": "Derivatives",
        "description": "The instantaneous rate of change of a function at a point.",
        "prerequisites": ["limits"],
        "course_id": "calculus1",
    },
    {
        "id": "chain_rule",
        "name": "Chain Rule",
        "description": "Rule for differentiating compositions of functions.",
        "prerequisites": ["derivatives"],
        "course_id": "calculus1",
    },
    {
        "id": "implicit_diff",
        "name": "Implicit Differentiation",
        "description": "Differentiating equations not explicitly solved for one variable.",
        "prerequisites": ["derivatives", "chain_rule"],
        "course_id": "calculus1",
    },
    {
        "id": "related_rates",
        "name": "Related Rates",
        "description": "Applying derivatives to find rates of change in related quantities.",
        "prerequisites": ["derivatives", "implicit_diff"],
        "course_id": "calculus1",
    },
    {
        "id": "integrals",
        "name": "Integrals",
        "description": "Calculating the accumulation of quantities and areas under curves.",
        "prerequisites": ["derivatives"],
        "course_id": "calculus1",
    },
    {
        "id": "fundamental_theorem",
        "name": "Fundamental Theorem of Calculus",
        "description": "Connecting derivatives and integrals as inverse processes.",
        "prerequisites": ["derivatives", "integrals"],
        "course_id": "calculus1",
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
