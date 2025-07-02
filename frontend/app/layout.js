import "./globals.css";

export const metadata = {
  title: "RAG Demo",
  description: "RAG Demo with Next.js, FastAPI, and Qdrant",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
