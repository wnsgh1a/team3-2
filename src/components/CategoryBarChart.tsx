"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
} from "recharts";

type Category = { name: string; score: number };

export default function CategoryBarChart({
    categories,
}: {
    categories: Category[];
}) {
    const data =
        categories?.map((c) => ({ name: c.name, score: c.score })) ?? [];
    return (
        <div style={{ width: "100%", height: 280 }}>
            <ResponsiveContainer>
                <BarChart
                    data={data}
                    margin={{ top: 8, right: 8, left: 0, bottom: 8 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="score" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
