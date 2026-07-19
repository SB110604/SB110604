import type { SectionProps } from "@/types/section";

export function SectionHeading({ title, subtitle }: Pick<SectionProps, "title" | "subtitle">) {
  return (
    <div className="mb-8 md:mb-12">
      <p className="text-xs uppercase tracking-[0.24em] text-[var(--color-accent-soft)]">Swamini Foods</p>
      <h2 className="mt-3 text-3xl font-medium text-[var(--color-text)] md:text-5xl">{title}</h2>
      {subtitle ? <p className="mt-4 max-w-2xl text-base text-[var(--color-text-muted)] md:text-lg">{subtitle}</p> : null}
    </div>
  );
}
