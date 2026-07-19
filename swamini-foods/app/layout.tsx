import type { Metadata, Viewport } from "next";
import { Cormorant_Garamond, Inter } from "next/font/google";
import "@/app/globals.css";
import "@/styles/animations.css";

const bodyFont = Inter({
  subsets: ["latin"],
  variable: "--font-body",
});

const headingFont = Cormorant_Garamond({
  subsets: ["latin"],
  variable: "--font-heading",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://swaminifoods.com"),
  title: {
    default: "Swamini Foods | Bilona Ghee",
    template: "%s | Swamini Foods",
  },
  description:
    "Swamini Foods crafts traditional bilona ghee with premium quality, authentic methods, and elevated culinary storytelling.",
  keywords: ["Swamini Foods", "Bilona Ghee", "A2 Ghee", "Traditional Ghee", "Premium Ghee"],
  openGraph: {
    title: "Swamini Foods | Bilona Ghee",
    description:
      "Traditional bilona process meets modern premium presentation for healthy and flavorful cooking.",
    type: "website",
    url: "https://swaminifoods.com",
    siteName: "Swamini Foods",
  },
  twitter: {
    card: "summary_large_image",
    title: "Swamini Foods | Bilona Ghee",
    description:
      "Discover artisanal bilona ghee from Swamini Foods with a premium, immersive web experience.",
  },
};

export const viewport: Viewport = {
  themeColor: "#0d0a08",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${bodyFont.variable} ${headingFont.variable} h-full scroll-smooth`}>
      <body className="min-h-full bg-[var(--color-background)] text-[var(--color-text)] antialiased">{children}</body>
    </html>
  );
}
