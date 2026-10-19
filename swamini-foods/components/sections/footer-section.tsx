import { sectionPadding } from "@/lib/theme";

export function FooterSection() {
  return (
    <footer id="footer" className={`${sectionPadding} border-t border-[var(--color-border)]`}>
      <p className="text-sm uppercase tracking-[0.2em] text-[var(--color-accent)]">Footer</p>
      <p className="mt-3 text-[var(--color-text-muted)]">Placeholder footer for contact, social links, and policies.</p>
    </footer>
  );
}
