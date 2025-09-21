concepts = [
    {
        "id": "limits",
        "name": "Limits",
        "description": "Understanding the behavior of functions as inputs approach a value.",
        "prerequisites": [],
    },
    {
        "id": "continuity",
        "name": "Continuity",
        "description": "Determining whether a function has any breaks, jumps, or holes.",
        "prerequisites": ["limits"],
    },
    {
        "id": "derivatives",
        "name": "Derivatives",
        "description": "The instantaneous rate of change of a function at a point.",
        "prerequisites": ["limits"],
    },
    {
        "id": "chain_rule",
        "name": "Chain Rule",
        "description": "Rule for differentiating compositions of functions.",
        "prerequisites": ["derivatives"],
    },
    {
        "id": "implicit_diff",
        "name": "Implicit Differentiation",
        "description": "Differentiating equations not explicitly solved for one variable.",
        "prerequisites": ["derivatives", "chain_rule"],
    },
    {
        "id": "related_rates",
        "name": "Related Rates",
        "description": "Applying derivatives to find rates of change in related quantities.",
        "prerequisites": ["derivatives", "implicit_diff"],
    },
    {
        "id": "integrals",
        "name": "Integrals",
        "description": "Calculating the accumulation of quantities and areas under curves.",
        "prerequisites": ["derivatives"],
    },
    {
        "id": "fundamental_theorem",
        "name": "Fundamental Theorem of Calculus",
        "description": "Connecting derivatives and integrals as inverse processes.",
        "prerequisites": ["derivatives", "integrals"],
    },
]

course = {
    "id": "calculus",
    "name": "Calculus",
    "description": "A basic calculus 1 course.",
    "concepts": concepts,
}
