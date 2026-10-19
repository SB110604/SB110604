"use client";

import { OrbitControls, Float } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";

function GheeOrb() {
  return (
    <Float speed={1.8} floatIntensity={1.2}>
      <mesh>
        <icosahedronGeometry args={[1, 1]} />
        <meshStandardMaterial color="#d9a466" metalness={0.35} roughness={0.25} />
      </mesh>
    </Float>
  );
}

export function HeroCanvas() {
  return (
    <div className="h-[280px] w-full overflow-hidden rounded-2xl border border-[var(--color-border)] md:h-[360px]">
      <Canvas camera={{ position: [0, 0, 3.5], fov: 45 }}>
        <ambientLight intensity={1.2} />
        <directionalLight position={[3, 3, 2]} intensity={1.6} />
        <GheeOrb />
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.9} />
      </Canvas>
    </div>
  );
}
