import "./globals.css";
export const metadata = { title: "Vibe Dashboard" };

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="ko">
            <body style={{ margin: 0, fontFamily: "ui-sans-serif, system-ui" }}>
                <div
                    style={{
                        maxWidth: 960,
                        margin: "24px auto",
                        padding: "0 16px",
                    }}
                >
                    <h1
                        style={{
                            fontSize: 24,
                            fontWeight: 700,
                            marginBottom: 16,
                        }}
                    >
                        AI Vibe Evaluator — Web Dashboard
                    </h1>
                    {children}
                </div>
            </body>
        </html>
    );
}
