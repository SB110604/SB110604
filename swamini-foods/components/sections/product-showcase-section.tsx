import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function ProductShowcaseSection() {
  return (
    <section id="product-showcase" className={sectionPadding}>
      <SectionHeading title="Product Showcase" subtitle="Placeholder product cards for ghee variants and pack sizes." />
      <div className="rounded-2xl border border-dashed border-[var(--color-border)] p-8 text-[var(--color-text-muted)]">
        Product cards placeholder.
      </div>
    </section>
  );
}
