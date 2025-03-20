"use client";

import { useEffect, useRef, useState } from "react";

const P5RubiksCube = () => {
  const [loading, setLoading] = useState(true);
  const sketchRef = useRef<HTMLDivElement>(null);
  const p5InstanceRef = useRef<any>(null);

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
          p.rotateX(p.frameCount * 0.5);
          p.rotateY(p.frameCount * 0.5);

          for (let c of cubes) {
            p.push();
            p.translate(c.x, c.y, c.z);
            p.box(50);
            p.pop();
          }
        };
      };

      p5InstanceRef.current = new p5.default(sketch, sketchRef.current as HTMLDivElement);
    });

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, []);

  const handleStartClick = () => {
    setLoading(false);
    if (p5InstanceRef.current) {
      p5InstanceRef.current.remove();
      p5InstanceRef.current = null;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      {loading ? (
        <>
          <div ref={sketchRef}></div>
          <button
            onClick={handleStartClick}
            className="py-2 px-4 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
          >
            Start
          </button>
        </>
      ) : (
        <div className="text-center">
          <h1 className="text-3xl font-bold"></h1>
        </div>
      )}
    </div>
  );
};

export default P5RubiksCube;