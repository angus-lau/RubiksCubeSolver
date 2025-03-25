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
        if (y === 1) color.bottom = colors.bottom;

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
  const cubesRef = useRef<Cubelet[]>(createCubelets());

  const rotationAnimation = useRef<{
    axis: "x" | "y" | "z" | null;
    layerValue: number;
    direction: "clockwise" | "counter";
    angle: number;
    speed: number;
    isAnimating: boolean;
  }>({
    axis: null,
    layerValue: 0,
    direction: "clockwise",
    angle: 0,
    speed: 3,
    isAnimating: false,
  });

  function rotateFace(axis: "x" | "y" | "z", layerValue: number, direction: "clockwise" | "counter") {
    const spacing = 55;
    const newCubes = cubesRef.current.map((c) => {
      const norm = {
        x: Math.round(c.x / spacing),
        y: Math.round(c.y / spacing),
        z: Math.round(c.z / spacing),
      };

      if (norm[axis] !== layerValue) return c;

      let { x, y, z, color } = c;
      let newX = x,
        newY = y,
        newZ = z;
      let newColor = { ...color };

      if (axis === "x") {
        newY = direction === "clockwise" ? -z : z;
        newZ = direction === "clockwise" ? y : -y;

        newColor = {
          ...color,
          top: direction === "clockwise" ? color.front : color.back,
          bottom: direction === "clockwise" ? color.back : color.front,
          front: direction === "clockwise" ? color.bottom : color.top,
          back: direction === "clockwise" ? color.top : color.bottom,
        };
      }

      if (axis === "y") {
        newX = direction === "clockwise" ? z : -z;
        newZ = direction === "clockwise" ? -x : x;

        newColor = {
          ...color,
          front: direction === "clockwise" ? color.left : color.right,
          back: direction === "clockwise" ? color.right : color.left,
          left: direction === "clockwise" ? color.back : color.front,
          right: direction === "clockwise" ? color.front : color.back,
        };
      }

      if (axis === "z") {
        newX = direction === "clockwise" ? -y : y;
        newY = direction === "clockwise" ? x : -x;

        newColor = {
          ...color,
          top: direction === "clockwise" ? color.left : color.right,
          bottom: direction === "clockwise" ? color.right : color.left,
          left: direction === "clockwise" ? color.bottom : color.top,
          right: direction === "clockwise" ? color.top : color.bottom,
        };
      }

      return {
        ...c,
        x: newX,
        y: newY,
        z: newZ,
        color: newColor,
      };
    });

    cubesRef.current = newCubes;
  }

  function startRotation(axis: "x" | "y" | "z", layerValue: number, direction: "clockwise" | "counter") {
    if (rotationAnimation.current.isAnimating) return;

    rotationAnimation.current = {
      axis,
      layerValue,
      direction,
      angle: 50,
      speed: 3,
      isAnimating: true,
    };
  }

  useEffect(() => {
    if (typeof window === "undefined" || !sketchRef.current) return;

    import("p5").then((p5) => {
      const sketch = (p: typeof p5.prototype) => {
        p.setup = () => {
          p.createCanvas(710, 400, p.WEBGL);
          p.angleMode(p.DEGREES);
        };

        p.draw = () => {
          p.clear();
          p.rotateX(p.radians(15));
          p.rotateY(p.radians(30));
          p.orbitControl();

          const anim = rotationAnimation.current;

          for (let c of cubesRef.current) {
            p.push();

            const spacing = 55;
            const normalized = {
              x: Math.round(c.x / spacing),
              y: Math.round(c.y / spacing),
              z: Math.round(c.z / spacing),
            };

            if (anim.isAnimating && normalized[anim.axis!] === anim.layerValue) {
              const theta = anim.direction === "clockwise" ? anim.angle : -anim.angle;

              if (anim.axis === "x") p.rotateX(p.radians(theta));
              if (anim.axis === "y") p.rotateY(p.radians(theta));
              if (anim.axis === "z") p.rotateZ(p.radians(theta));
            }

            p.translate(c.x, c.y, c.z);
            p.fill(50);
            p.box(50);

            const s = 23;
            const offset = 26;

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

          // update angle
          if (anim.isAnimating) {
            anim.angle += anim.speed;

            if (anim.angle >= 90) {
              anim.angle = 90;
              anim.isAnimating = false;

              // Wait one full frame, then rotate the face
              setTimeout(() => {
                rotateFace(anim.axis!, anim.layerValue, anim.direction);
                anim.angle = 0;
              }, 0);
            }
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
  }, []);

  return (
    <div className="flex flex-col items-center">
      <div ref={sketchRef} />
      <button
        onClick={() => startRotation("y", -1, "clockwise")}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Rotate Top Face
      </button>
    </div>
  );
};

export default SolvingCube;