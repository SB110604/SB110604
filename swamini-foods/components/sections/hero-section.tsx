import { Sparkles } from "lucide-react";
import { HeroCanvas } from "@/components/three/hero-canvas";
import { SectionHeading } from "@/components/ui/section-heading";
import { sectionPadding } from "@/lib/theme";

export function HeroSection() {
  return (
    <section id="hero" className={sectionPadding}>
      <SectionHeading
        title="Hero"
        subtitle="Premium handmade bilona ghee storytelling starts here with immersive visuals and smooth interactions."
      />
      <div className="grid gap-8 md:grid-cols-2 md:items-center">
        <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <p className="flex items-center gap-2 text-sm uppercase tracking-[0.2em] text-[var(--color-accent)]">
            <Sparkles size={16} /> Signature Experience
          </p>
          <p className="mt-4 text-lg text-[var(--color-text-muted)]">
            Placeholder hero copy for brand promise, call to action, and product-first communication.
          </p>
        </div>
        <HeroCanvas />
      </div>
    </section>
  );
}
