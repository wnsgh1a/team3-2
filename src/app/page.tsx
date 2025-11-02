export default function Home() {
    const sampleId = "123e4567-e89b-12d3-a456-426614174000";
    return (
        <main style={{ padding: 16 }}>
            <h2 style={{ marginTop: 0 }}>시작하기</h2>
            <p>
                샘플 리뷰 보기 →{" "}
                <a
                    href={`/review/${sampleId}`}
                    style={{ textDecoration: "underline" }}
                >
                    /review/{sampleId}
                </a>
            </p>
        </main>
    );
}
