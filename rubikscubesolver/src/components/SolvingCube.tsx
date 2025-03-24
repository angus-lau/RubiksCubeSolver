"use client";
import { useEffect, useRef } from "react";

type Face = "front" | "back" | "left" | "right" | "top" | "bottom";

type Cubelet = {
  x: number;
  y: number;
  z: number;
  color: Partial<Record<Face, string>>;
};

const createCubelets = (): Cubelet[] => {
  const colors = {
    front: "green",
    back: "blue",
    left: "orange",
    right: "red",
    top: "white",
    bottom: "yellow",
  };

  const cubelets: Cubelet[] = [];
  const spacing = 55;

  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const color: Partial<Record<Face, string>> = {};
        if (z === 1) color.front = colors.front;
        if (z === -1) color.back = colors.back;
        if (x === -1) color.left = colors.left;
        if (x === 1) color.right = colors.right;
        if (y === -1) color.top = colors.top;
        if (y === 1)  color.bottom = colors.bottom; 

        cubelets.push({
          x: x * spacing,
          y: y * spacing,
          z: z * spacing,
          color,
        });
      }
    }
  }

  return cubelets;
};

const SolvingCube = () => {
  const p5InstanceRef = useRef<any>(null);
  const sketchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window === "undefined" || !sketchRef.current) return;

    import("p5").then((p5) => {
      let cubes: Cubelet[] = createCubelets();

      const sketch = (p: typeof p5.prototype) => {
        p.setup = () => {
          p.createCanvas(710, 400, p.WEBGL);
          p.angleMode(p.DEGREES);

          let size = 50;
          let spacing = 55;
        };

        p.draw = () => {
          p.clear();
          p.rotateX(p.degrees(15));
          p.rotateY(p.degrees(30));
          p.orbitControl();

          for (let c of cubes) {
            p.push();
            p.translate(c.x, c.y, c.z);

            // draw inner cube
            p.fill(50);
            p.box(50);


            const s = 23; // slightly smaller than half cube size
            const offset = 26; // how far to push stickers outward


            if (c.color.front) {
              p.fill(c.color.front);
              p.beginShape();
              p.vertex(-s, -s, offset);
              p.vertex(s, -s, offset);
              p.vertex(s, s, offset);
              p.vertex(-s, s, offset);
              p.endShape(p.CLOSE);
            }

            if (c.color.back) {
              p.fill(c.color.back);
              p.beginShape();
              p.vertex(s, -s, -offset);
              p.vertex(-s, -s, -offset);
              p.vertex(-s, s, -offset);
              p.vertex(s, s, -offset);
              p.endShape(p.CLOSE);
            }

            if (c.color.left) {
              p.fill(c.color.left);
              p.beginShape();
              p.vertex(-offset, -s, -s);
              p.vertex(-offset, -s, s);
              p.vertex(-offset, s, s);
              p.vertex(-offset, s, -s);
              p.endShape(p.CLOSE);
            }

            if (c.color.right) {
              p.fill(c.color.right);
              p.beginShape();
              p.vertex(offset, -s, s);
              p.vertex(offset, -s, -s);
              p.vertex(offset, s, -s);
              p.vertex(offset, s, s);
              p.endShape(p.CLOSE);
            }

            if (c.color.top) {
              p.fill(c.color.top);
              p.beginShape();
              p.vertex(-s, -offset, -s);
              p.vertex(s, -offset, -s);
              p.vertex(s, -offset, s);
              p.vertex(-s, -offset, s);
              p.endShape(p.CLOSE);
            }

            if (c.color.bottom) {
              p.fill(c.color.bottom);
              p.beginShape();
              p.vertex(-s, offset, s);
              p.vertex(s, offset, s);
              p.vertex(s, offset, -s);
              p.vertex(-s, offset, -s);
              p.endShape(p.CLOSE);
            }

            p.pop();
          }
        };
      };

      if (!p5InstanceRef.current) {
        p5InstanceRef.current = new p5.default(sketch, sketchRef.current as HTMLDivElement);
      }
    });

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  });

  return <div ref={sketchRef} />;
};

export default SolvingCube;