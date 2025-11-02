"use client";

export default function ScoreSummary(props: {
    reviewId: string;
    globalScore: number;
    modelScore: number;
    summary: string;
}) {
    const { reviewId, globalScore, modelScore, summary } = props;

    const card: React.CSSProperties = {
        border: "1px solid #eee",
        borderRadius: 12,
        padding: 16,
    };
    const badge: React.CSSProperties = {
        display: "inline-block",
        padding: "2px 8px",
        borderRadius: 999,
        border: "1px solid #ddd",
        fontSize: 12,
    };

    return (
        <div style={card}>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: 8,
                }}
            >
                <span style={badge}>Review ID</span>
                <code style={{ fontSize: 12, color: "#555" }}>{reviewId}</code>
            </div>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 12,
                }}
            >
                <div
                    style={{
                        padding: 12,
                        border: "1px solid #f0f0f0",
                        borderRadius: 8,
                    }}
                >
                    <div style={{ fontSize: 12, color: "#666" }}>
                        Global Score
                    </div>
                    <div style={{ fontSize: 28, fontWeight: 700 }}>
                        {globalScore}
                    </div>
                </div>
                <div
                    style={{
                        padding: 12,
                        border: "1px solid #f0f0f0",
                        borderRadius: 8,
                    }}
                >
                    <div style={{ fontSize: 12, color: "#666" }}>
                        Model Score
                    </div>
                    <div style={{ fontSize: 28, fontWeight: 700 }}>
                        {modelScore}
                    </div>
                </div>
            </div>

            <div style={{ marginTop: 12, fontSize: 14, color: "#333" }}>
                <b>요약:</b> {summary}
            </div>
        </div>
    );
}
