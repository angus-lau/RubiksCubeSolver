"use client";

import { useEffect, useRef } from "react";

const P5RubiksCube = () => {
  const sketchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;

    import("p5").then((p5) => {
      let cubes: { x: number; y: number; z: number }[] = [];

      const sketch = (p: typeof p5.prototype) => {
        p.setup = () => {
          p.createCanvas(710, 400, p.WEBGL);
          p.angleMode(p.DEGREES);
          p.normalMaterial();

          let size = 50; 
          let spacing = 55;

          for (let x = -1; x <= 1; x++) {
            for (let y = -1; y <= 1; y++) {
              for (let z = -1; z <= 1; z++) {
                cubes.push({ x: x * spacing, y: y * spacing, z: z * spacing });
              }
            }
          }
        };

        p.draw = () => {
         p.clear();
          p.rotateX(30);
          p.rotateY(p.frameCount * 0.5); // Rotate entire cube

          for (let c of cubes) {
            p.push();
            p.translate(c.x, c.y, c.z);
            p.box(50);
            p.pop();
          }
        };
      };

      const p5Instance = new p5.default(sketch, sketchRef.current as HTMLDivElement);

      return () => {
        p5Instance.remove();
      };
    });
  }, []);

  return <div ref={sketchRef}></div>;
};

export default P5RubiksCube;