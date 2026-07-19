import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function TestimonialsSection() {
  return (
    <section id="testimonials" className={sectionPadding}>
      <SectionHeading title="Testimonials" subtitle="Placeholder carousel/grid for customer reviews." />
      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-[var(--color-text-muted)]">
        Testimonials placeholder.
      </div>
    </section>
  );
}
