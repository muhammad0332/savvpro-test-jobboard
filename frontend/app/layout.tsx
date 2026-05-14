import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "JobBoard Pro",
  description: "Internal hiring platform assessment",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="shell">
          <nav className="nav">
            <Link href="/">
              <strong>JobBoard Pro</strong>
            </Link>
            <div className="nav-links">
              <Link href="/">Jobs</Link>
              <Link href="/dashboard">Dashboard</Link>
            </div>
          </nav>
          {children}
        </main>
      </body>
    </html>
  );
}
