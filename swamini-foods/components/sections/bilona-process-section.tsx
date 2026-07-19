import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function BilonaProcessSection() {
  return (
    <section id="bilona-process" className={sectionPadding}>
      <SectionHeading title="Bilona Process" subtitle="Placeholder timeline for churning, simmering, and purity checks." />
      <div className="grid gap-4 md:grid-cols-3">
        {['Curd Formation', 'Wooden Churning', 'Slow Clarification'].map((step) => (
          <article key={step} className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5 text-[var(--color-text-muted)]">
            {step}
          </article>
        ))}
      </div>
    </section>
  );
}
