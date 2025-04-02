"use client";

import { useEffect, useRef } from "react";

type Face = "front" | "back" | "left" | "right" | "top" | "bottom";

type Cubelet = {
  x: number;
  y: number;
  z: number;
  color: Partial<Record<Face, string>>;
};

// Initializes the 3D Rubik's Cube with color assignments based on position
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

  const globalRotation = useRef<{
    angle: number;
    rotating: boolean;
    layer: number | null;
    axis: "x" | "y" | "z" | null;
    direction: 'clockwise' | 'counter';
  }>({
    angle: 0,
    rotating: false,
    layer: null,
    axis: null,
    direction: 'clockwise',
  });

  function rotateFace(axis: "x" | "y" | "z", layerValue: number, direction: "clockwise" | "counter") {
    const spacing = 55;

    const rotate90 = (x: number, y: number, clockwise: boolean): [number, number] =>
      clockwise ? [-y, x] : [y, -x];

    const newCubes = cubesRef.current.map((c) => {
      const gx = Math.round(c.x / spacing);
      const gy = Math.round(c.y / spacing);
      const gz = Math.round(c.z / spacing);

      const matchLayer =
        (axis === "x" && gx === layerValue) ||
        (axis === "y" && gy === layerValue) ||
        (axis === "z" && gz === layerValue);

      if (!matchLayer) return c;

      let [nx, ny, nz] = [gx, gy, gz];
      let newColor = { ...c.color };

      if (axis === "x") {
        [ny, nz] = rotate90(gy, gz, direction === "clockwise");
        newColor = {
          ...c.color,
          top: direction === "clockwise" ? c.color.front : c.color.back,
          bottom: direction === "clockwise" ? c.color.back : c.color.front,
          front: direction === "clockwise" ? c.color.bottom : c.color.top,
          back: direction === "clockwise" ? c.color.top : c.color.bottom,
        };
      }

      if (axis === "y") {
        [nz, nx] = rotate90(gz, gx, direction === "clockwise");
        newColor = {
          ...c.color,
          front: direction === "clockwise" ? c.color.left : c.color.right,
          back: direction === "clockwise" ? c.color.right : c.color.left,
          left: direction === "clockwise" ? c.color.back : c.color.front,
          right: direction === "clockwise" ? c.color.front : c.color.back,
        };
      }

      if (axis === "z") {
        [nx, ny] = rotate90(gx, gy, direction === "clockwise");
        newColor = {
          ...c.color,
          top: direction === "clockwise" ? c.color.left : c.color.right,
          bottom: direction === "clockwise" ? c.color.right : c.color.left,
          left: direction === "clockwise" ? c.color.bottom : c.color.top,
          right: direction === "clockwise" ? c.color.top : c.color.bottom,
        };
      }

      return {
        ...c,
        x: nx * spacing,
        y: ny * spacing,
        z: nz * spacing,
        color: newColor,
      };
    });

    cubesRef.current = newCubes;
  }

  function startRotation(axis: "x" | "y" | "z", layer: number) {
    globalRotation.current.rotating = true;
    globalRotation.current.layer = layer;
    globalRotation.current.axis = axis;
    globalRotation.current.direction = 'clockwise';

    setTimeout(() => {
      globalRotation.current.rotating = false;
      globalRotation.current.layer = null;
      globalRotation.current.axis = null;
      rotateFace(axis, layer, "clockwise");
      globalRotation.current.angle = 0;
    }, 2000);
  }

  function startCounterRotation(axis: "x" | "y" | "z", layer: number) {
    globalRotation.current.rotating = true;
    globalRotation.current.layer = layer;
    globalRotation.current.axis = axis;
    globalRotation.current.direction = 'counter';
  
    setTimeout(() => {
      globalRotation.current.rotating = false;
      globalRotation.current.layer = null;
      globalRotation.current.axis = null;
      rotateFace(axis, layer, "counter");
      globalRotation.current.angle = 0;
    }, 2000);
  }

  useEffect(() => {
    // p5.js canvas setup and draw loop behavior
    if (typeof window === "undefined" || !sketchRef.current) return;

    import("p5").then((p5) => {
      const sketch = (p: typeof p5.prototype) => {
        p.setup = () => {
          p.createCanvas(710, 400, p.WEBGL); // Setup canvas
          p.angleMode(p.DEGREES);
        };

        p.draw = () => {
          p.clear(); // Clear the canvas
          if (globalRotation.current.rotating) {
            const delta = globalRotation.current.direction === "clockwise" ? 50 : -50;
            globalRotation.current.angle += delta;
          }
        
          p.orbitControl();

          for (let c of cubesRef.current) {
            p.push();

            const spacing = 55;
            const normalized = {
              x: Math.round(c.x / spacing),
              y: Math.round(c.y / spacing),
              z: Math.round(c.z / spacing),
            };

            if (
              globalRotation.current.rotating &&
              globalRotation.current.layer !== null &&
              globalRotation.current.axis !== null &&
              normalized[globalRotation.current.axis] === globalRotation.current.layer
            ) {
              const angle = p.radians(globalRotation.current.angle);
              if (globalRotation.current.axis === "x") p.rotateX(angle);
              else if (globalRotation.current.axis === "y") p.rotateY(angle);
              else if (globalRotation.current.axis === "z") p.rotateZ(angle);
            }

            p.translate(c.x, c.y, c.z); // Position the cubelet
            p.fill(50);
            p.box(50); // Draw the cubelet

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
      <div ref={sketchRef}/>
      <button
        onClick={() => startRotation('y', -1)}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Rotate Top Face
      </button>
      <button
        onClick={() => startCounterRotation('y', -1)}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Rotate Top Face Counterclockwise
      </button>
      <button
        onClick={() => startRotation('y', 0)}
        className="mt-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Rotate Middle Layer
      </button>
      <button
        onClick={() => startCounterRotation('y', 0)}
        className="mt-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Rotate Middle Layer Counterclockwise
      </button>
      <button
        onClick={() => startRotation('y', 1)}
        className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Rotate Bottom Face
      </button>
      <button
        onClick={() => startCounterRotation('x',-1)}
        className="mt-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
      >
        Rotate Left Column
      </button>
      <button
        onClick={() => startRotation('x',-1)}
        className="mt-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
      >
        Rotate Left Column Counterclockwise
      </button>
      <button
        onClick={() => startRotation('x',0)}
        className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        Rotate Middle Column
      </button>
      <button
        onClick={() => startCounterRotation('x',0)}
        className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        Rotate Middle Column Counterclockwise
      </button>
      <button
        onClick={() => startRotation('x',1)}
        className="mt-2 px-4 py-2 bg-pink-600 text-white rounded hover:bg-pink-700"
      >
        Rotate Right Column
      </button>
      <button
        onClick={() => startCounterRotation('x',1)}
        className="mt-2 px-4 py-2 bg-pink-600 text-white rounded hover:bg-pink-700"
      >
        Rotate Right Column Counterclockwise
      </button>
      <button
        onClick={() => startRotation('z', 1)}
        className="mt-2 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700"
      >
        Rotate Front Face
      </button>
      <button
        onClick={() => startCounterRotation('z', 1)}
        className="mt-2 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700"
      >
        Rotate Front Face Counterclockwise
      </button>
      <button
        onClick={() => startCounterRotation('z', -1)}
        className="mt-2 px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700"
      >
        Rotate Back Face
      </button>
      <button
        onClick={() => startRotation('z', -1)}
        className="mt-2 px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700"
      >
        Rotate Back Face Counterclockwise
      </button>
    </div>
  );
};

export default SolvingCube;