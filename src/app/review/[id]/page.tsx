type Category = { name: string; score: number };
type ReviewResponse = {
    review_id: string;
    global_score: number;
    model_score: number;
    categories: Category[];
    summary: string;
};

async function getReview(id: string): Promise<ReviewResponse> {
    // Fallback 넣어서 .env 못 읽어도 안전하게
    const base = process.env.API_BASE || "http://localhost:8000";
    const url = new URL(`/review/${id}`, base).toString();

    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok)
        throw new Error(
            `Failed to fetch review: ${res.status} ${res.statusText}`
        );
    return res.json();
}

import ScoreSummary from "@/components/ScoreSummary";
import CategoryBarChart from "@/components/CategoryBarChart";

// ✅ Next 16: params는 Promise입니다. 먼저 await 해서 꺼내세요.
export default async function ReviewPage({
    params,
}: {
    params: Promise<{ id: string }>;
}) {
    const { id } = await params;
    const data = await getReview(id);

    return (
        <main>
            <section
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 16,
                }}
            >
                <ScoreSummary
                    reviewId={data.review_id}
                    globalScore={data.global_score}
                    modelScore={data.model_score}
                    summary={data.summary}
                />
                <div
                    style={{
                        border: "1px solid #eee",
                        borderRadius: 12,
                        padding: 16,
                    }}
                >
                    <h3 style={{ margin: "0 0 12px 0" }}>카테고리 점수</h3>
                    <CategoryBarChart categories={data.categories} />
                </div>
            </section>

            <section style={{ marginTop: 24 }}>
                <div
                    style={{
                        border: "1px solid #eee",
                        borderRadius: 12,
                        padding: 16,
                    }}
                >
                    <h3 style={{ margin: "0 0 12px 0" }}>원본 JSON</h3>
                    <pre
                        style={{
                            margin: 0,
                            whiteSpace: "pre-wrap",
                            wordBreak: "break-word",
                        }}
                    >
                        {JSON.stringify(data, null, 2)}
                    </pre>
                </div>
            </section>
        </main>
    );
}
