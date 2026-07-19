import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function StorySection() {
  return (
    <section id="story" className={sectionPadding}>
      <SectionHeading title="Story" subtitle="Placeholder section for origin, values, and farm-to-table narrative." />
      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-[var(--color-text-muted)]">
        Story content placeholder.
      </div>
    </section>
  );
}
