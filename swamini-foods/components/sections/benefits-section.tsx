import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function BenefitsSection() {
  return (
    <section id="benefits" className={sectionPadding}>
      <SectionHeading title="Benefits" subtitle="Placeholder list of health, purity, and taste benefits." />
      <ul className="grid gap-3 md:grid-cols-3">
        {['A2-rich nutrition', 'Traditional authenticity', 'Premium taste profile'].map((item) => (
          <li key={item} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-[var(--color-text-muted)]">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
