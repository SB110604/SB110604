"use client";

import { useEffect } from "react";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import gsap from "gsap";
import { useSmoothScroll } from "@/hooks/use-smooth-scroll";
import { LoadingScreen } from "@/components/ui/loading-screen";
import { HeroSection } from "@/components/sections/hero-section";
import { StorySection } from "@/components/sections/story-section";
import { BilonaProcessSection } from "@/components/sections/bilona-process-section";
import { ProductShowcaseSection } from "@/components/sections/product-showcase-section";
import { CookingExperienceSection } from "@/components/sections/cooking-experience-section";
import { BenefitsSection } from "@/components/sections/benefits-section";
import { TestimonialsSection } from "@/components/sections/testimonials-section";
import { FAQSection } from "@/components/sections/faq-section";
import { FooterSection } from "@/components/sections/footer-section";
import { PageShell } from "@/components/layout/page-shell";

export function HomePage() {
  useSmoothScroll();

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
  }, []);

  return (
    <>
      <LoadingScreen />
      <PageShell>
        <HeroSection />
        <StorySection />
        <BilonaProcessSection />
        <ProductShowcaseSection />
        <CookingExperienceSection />
        <BenefitsSection />
        <TestimonialsSection />
        <FAQSection />
        <FooterSection />
      </PageShell>
    </>
  );
}
