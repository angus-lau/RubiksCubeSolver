"use client";

import { useEffect, useRef, useState } from "react";
import SolvingCube from './SolvingCube'

const P5RubiksCube = () => {
  const [stage, setStage] = useState<"intro" | "solve">("intro");
  const [fadeOut, setFadeOut] = useState(false);
  const sketchRef = useRef<HTMLDivElement>(null);
  const p5InstanceRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window === "undefined" || stage !== "intro") return;

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
  }, [stage]);

  const handleStartClick = () => {
    setFadeOut(true);
    setTimeout(() => {
      setStage("solve");
    }, 1000);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      {stage === "intro" && (
        <div
          className={`flex flex-col items-center justify-center transition-opacity duration-1000 ${
            fadeOut ? "opacity-0 pointer-events-none" : "opacity-100"
          }`}
        >
          <div ref={sketchRef} />
          <button
            onClick={handleStartClick}
            className="py-2 px-4 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75 mt-4"
          >
            Start
          </button>
        </div>
      )}
      {stage === "solve" && <SolvingCube />}
    </div>
  );
};

export default P5RubiksCube;