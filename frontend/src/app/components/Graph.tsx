"use client";

import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";

export default function Graph() {
    const cyRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!cyRef.current) return;

        fetch("http://localhost:8000/courses/calculus1/graph")
            .then((r) => r.json())
            .then((data) => {
                const elements = [
                    ...data.nodes.map((n: any) => ({
                        data: { id: n.id, label: n.concept.name },
                    })),
                    ...data.links.map((l: any) => ({
                        data: { source: l.source, target: l.target },
                    })),
                ];

                const cy = cytoscape({
                    container: cyRef.current,
                    elements,
                    style: [
                        {
                            selector: "node",
                            style: {
                                "background-color": "#0074D9",
                                "shape": "round-rectangle",
                                "label": "data(label)",
                                "color": "white",
                                "text-valign": "center",
                                "text-halign": "center",
                                "padding": "10px",
                                "width": "label",
                                "height": "label",
                                "font-size": 16,
                                "text-wrap": "wrap",
                                "text-max-width": 120,
                            },
                        },
                        {
                            selector: "edge",
                            style: {
                                width: 2,
                                "line-color": "#aaa",
                                "target-arrow-color": "#aaa",
                                "target-arrow-shape": "triangle",
                                "curve-style": "bezier",
                            },
                        },
                    ],
                    layout: { name: "circle" },
                });

                cy.fit();
            });
    }, []);

    return (
        <div
            ref={cyRef}
            className="w-full h-200 border border-blue-500"
        />
    );
}
