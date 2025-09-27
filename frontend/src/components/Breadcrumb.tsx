import Link from "next/link";

interface Crumb {
    href?: string;
    label: string;
}

export default function Breadcrumb({ items }: { items: Crumb[] }) {
    return (
        <nav className="mb-4 text-sm text-gray-600">
            {items.map((item, idx) => (
                <span key={idx}>
                    {item.href ? (
                        <Link href={item.href} className="hover:underline">
                            {item.label}
                        </Link>
                    ) : (
                        <span className="text-gray-800 font-medium">
                            {item.label}
                        </span>
                    )}
                    {idx < items.length - 1 && <span className="mx-2">/</span>}
                </span>
            ))}
        </nav>
    );
}
