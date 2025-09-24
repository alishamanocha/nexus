export interface NodeData {
    id: string;
    concept: { name: string};
}

export interface LinkData {
    source: string;
    target: string;
}

export interface GraphResponse {
    nodes: NodeData[];
    links: LinkData[];
}
