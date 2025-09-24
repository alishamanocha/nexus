"use client";

import { useEffect, useRef, useState } from "react";
import cytoscape from "cytoscape";
import type { GraphResponse, NodeData, LinkData } from "@/types/graph";

export default function Graph({ courseId }: { courseId: string }) {
    const cyRef = useRef<HTMLDivElement>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!cyRef.current) return;
        let cy: cytoscape.Core | undefined;

        fetch(`http://localhost:8000/courses/${courseId}/graph`)
            .then(async (r) => {
                if (!r.ok) {
                    let errMsg = `${r.status} - ${r.statusText}`;
                    try {
                        const errData = await r.json();
                        if (errData?.detail) {
                            errMsg = errData.detail;
                        }
                    } catch {}
                    throw new Error(errMsg);
                }
                return r.json();
            })
            .then((data: GraphResponse) => {
                const elements = [
                    ...data.nodes.map((n: NodeData) => ({
                        data: { id: n.id, label: n.concept.name },
                    })),
                    ...data.links.map((l: LinkData) => ({
                        data: { source: l.source, target: l.target },
                    })),
                ];

                cy = cytoscape({
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
                    layout: { name: "breadthfirst", directed: true, padding: 10 },
                });

                cy.fit();
            })
            .catch((err) => {
                setError(err.message);
            });

        return () => {
            cy?.destroy();
        };
    }, [courseId]);

    if (error) {
        return (
            <div className="p-4 text-red-600 border border-red-400 bg-red-50 rounded">
                {error}
            </div>
        );
    }

    return (
        <div
            ref={cyRef}
            className="w-full h-200 border border-blue-500"
        />
    );
}
