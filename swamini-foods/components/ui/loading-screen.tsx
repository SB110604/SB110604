"use client";

import { motion } from "framer-motion";

export function LoadingScreen() {
  return (
    <motion.section
      className="flex min-h-[30vh] items-center justify-center border-b border-[var(--color-border)] bg-[var(--color-surface)]"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="text-center">
        <p className="text-xs uppercase tracking-[0.3em] text-[var(--color-accent)]">Loading Screen</p>
        <h1 className="mt-4 text-3xl font-semibold text-[var(--color-text)] md:text-5xl">Crafting Pure Bilona Goodness</h1>
      </div>
    </motion.section>
  );
}
