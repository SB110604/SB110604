import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function CookingExperienceSection() {
  return (
    <section id="cooking-experience" className={sectionPadding}>
      <SectionHeading
        title="Cooking Experience"
        subtitle="Placeholder section for recipe interactions, aroma cues, and kitchen storytelling."
      />
      <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 text-[var(--color-text-muted)]">
        Cooking experience placeholder.
      </div>
    </section>
  );
}
