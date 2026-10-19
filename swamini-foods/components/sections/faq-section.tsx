import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function FAQSection() {
  return (
    <section id="faq" className={sectionPadding}>
      <SectionHeading title="FAQ" subtitle="Placeholder frequently asked questions block." />
      <div className="space-y-3">
        {['What makes bilona ghee special?', 'How should it be stored?', 'Is it lab-tested?'].map((question) => (
          <article key={question} className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4 text-[var(--color-text-muted)]">
            {question}
          </article>
        ))}
      </div>
    </section>
  );
}
