"use client";

import { useState, useEffect, useRef } from "react";

type Face = "front" | "back" | "left" | "right" | "top" | "bottom";

type Cubelet = {
  x: number;
  y: number;
  z: number;
  color: Partial<Record<Face, string>>;
};

// Initializes the 3D Rubik's Cube with color assignments based on position
const createCubeletsFromCubeString = (cubeString: string): Cubelet[] => {
  const colorCharToHex: Record<string, string> = {
    U: "white",
    D: "yellow",
    F: "green",
    B: "blue",
    R: "red",
    L: "orange",
  };

  const faces: Record<string, string[][]> = {
    U: [],
    R: [],
    F: [],
    D: [],
    L: [],
    B: [],
  };

  let idx = 0;
  for (const face of ["U", "R", "F", "D", "L", "B"]) {
    faces[face] = [];
    for (let i = 0; i < 3; i++) {
      faces[face].push([]);
      for (let j = 0; j < 3; j++) {
        faces[face][i].push(cubeString[idx++]);
      }
    }
  }

  const spacing = 55;
  const cubelets: Cubelet[] = [];

  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const color: Partial<Record<Face, string>> = {};

        const i = -(y - 1);
        const j = x + 1;

        if (y === -1) color.top = colorCharToHex[faces["U"][i][j]];
        if (y === 1) color.bottom = colorCharToHex[faces["D"][i][j]];
        if (z === 1) color.front = colorCharToHex[faces["F"][i][j]];
        if (z === -1) color.back = colorCharToHex[faces["B"][i][j]];
        if (x === -1) color.left = colorCharToHex[faces["L"][i][j]];
        if (x === 1) color.right = colorCharToHex[faces["R"][i][j]];

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
  const [cubeString, setCubeString] = useState<string>("");
  const [selectedLabel, setSelectedLabel] = useState<string>("Red");
  const colorOptions = ["Red", "Green", "Blue", "Yellow", "White", "Orange"];
  const p5InstanceRef = useRef<any>(null);
  const sketchRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const defaultCube = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB";
  const cubesRef = useRef<Cubelet[]>(createCubeletsFromCubeString(defaultCube));

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

  const handleCaptureFrame = async () => {
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx || !videoRef.current || !canvasRef.current) return;
  
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  
    // Capture frame from video for backend processing
    ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    const imageData = canvasRef.current.toDataURL("image/png");
    const base64Image = imageData.replace(/^data:image\/png;base64,/, "");
  
    // Clear again so we can just draw overlay
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  
    // === DRAW ROI same as backend ===
    const ROI_WIDTH = 200;
    const ROI_HEIGHT = 200;
    const NUM_ROWS = 3;
    const NUM_COLS = 3;
    const CELL_WIDTH = ROI_WIDTH / NUM_COLS;
    const CELL_HEIGHT = ROI_HEIGHT / NUM_ROWS;
  
    const x_center = canvasRef.current.width / 2;
    const y_center = canvasRef.current.height / 2;
    const x1 = x_center - ROI_WIDTH / 2;
    const y1 = y_center - ROI_HEIGHT / 2;
  
    ctx.strokeStyle = "red";
    ctx.lineWidth = 1;
  
    // Draw grid lines
    for (let i = 0; i <= NUM_ROWS; i++) {
      const y = y1 + i * CELL_HEIGHT;
      ctx.beginPath();
      ctx.moveTo(x1, y);
      ctx.lineTo(x1 + ROI_WIDTH, y);
      ctx.stroke();
    }
  
    for (let i = 0; i <= NUM_COLS; i++) {
      const x = x1 + i * CELL_WIDTH;
      ctx.beginPath();
      ctx.moveTo(x, y1);
      ctx.lineTo(x, y1 + ROI_HEIGHT);
      ctx.stroke();
    }
  
    // Optional: draw the center cell highlight
    ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
    ctx.fillRect(
      x1 + CELL_WIDTH,
      y1 + CELL_HEIGHT,
      CELL_WIDTH,
      CELL_HEIGHT
    );
  
    try {
      const response = await fetch("http://127.0.0.1:8000/cube-state", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: base64Image }),
      });
  
      const data = await response.json();
      console.log("Cube result:", data);
    } catch (error) {
      console.error("Error sending image to backend:", error);
    }
  };

  const handleScanCenter = async (label: string) => {
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx || !videoRef.current || !canvasRef.current) return;

    ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
    const imageData = canvasRef.current.toDataURL("image/png");
    const base64Image = imageData.replace(/^data:image\/png;base64,/, "");

    try {
      const response = await fetch("http://127.0.0.1:8000/scan-center", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image, label }), // e.g., "Red"
      });

      const data = await response.json();
      console.log("Scan Center Response:", data);
    } catch (error) {
      console.error("Error scanning center:", error);
    }
  };

  

  useEffect(() => {
    // p5.js canvas setup and draw loop behavior
    if (typeof window === "undefined" || !sketchRef.current) return;

    cubesRef.current = createCubeletsFromCubeString(defaultCube);

    import("p5").then((p5) => {
      const sketch = (p: typeof p5.prototype) => {
        p.setup = () => {
          p.createCanvas(710, 400, p.WEBGL); // Setup canvas
          p.angleMode(p.DEGREES);
          p.camera(
            350, -250, 600, // Camera position
            0, 0, 0,        // Look at the origin
            0, 1, 0         // Up direction
          );
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

    if (videoRef.current) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          videoRef.current!.srcObject = stream;
        })
        .catch((err) => {
          console.error("Failed to access webcam:", err);
        });
    }

    // New: continuously draw ROI overlay on the canvas once video feed is active
    const drawOverlay = () => {
      const ctx = canvasRef.current?.getContext("2d");
      if (!ctx || !videoRef.current || !canvasRef.current) return;

      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

      const ROI_WIDTH = 200;
      const ROI_HEIGHT = 200;
      const NUM_ROWS = 3;
      const NUM_COLS = 3;
      const CELL_WIDTH = ROI_WIDTH / NUM_COLS;
      const CELL_HEIGHT = ROI_HEIGHT / NUM_ROWS;

      const x_center = canvasRef.current.width / 2;
      const y_center = canvasRef.current.height / 2;
      const x1 = x_center - ROI_WIDTH / 2;
      const y1 = y_center - ROI_HEIGHT / 2;

      ctx.strokeStyle = "red";
      ctx.lineWidth = 1;

      // Draw grid lines
      for (let i = 0; i <= NUM_ROWS; i++) {
        const y = y1 + i * CELL_HEIGHT;
        ctx.beginPath();
        ctx.moveTo(x1, y);
        ctx.lineTo(x1 + ROI_WIDTH, y);
        ctx.stroke();
      }

      for (let i = 0; i <= NUM_COLS; i++) {
        const x = x1 + i * CELL_WIDTH;
        ctx.beginPath();
        ctx.moveTo(x, y1);
        ctx.lineTo(x, y1 + ROI_HEIGHT);
        ctx.stroke();
      }

      // Draw center cell highlight
      ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
      ctx.fillRect(x1 + CELL_WIDTH, y1 + CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT);
    };

    const animationLoop = () => {
      drawOverlay();
      requestAnimationFrame(animationLoop);
    };

    requestAnimationFrame(animationLoop);

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-[320px] h-[240px]">
        <video
          ref={videoRef}
          width="320"
          height="240"
          autoPlay
          muted
          className="absolute top-0 left-0 rounded border z-0 transform scale-x-[-1]"
        />
        <canvas
          ref={canvasRef}
          width="320"
          height="240"
          className="absolute top-0 left-0 z-10 pointer-events-none"
        />
      </div>
      <button
        onClick={handleCaptureFrame}
        className="mt-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
      >
        Capture & Analyze Frame
      </button>
      
      <div className="mt-4 flex items-center gap-2">
        <label htmlFor="face" className="text-white">Select Face:</label>
        <select
          id="face"
          value={selectedLabel}
          onChange={(e) => setSelectedLabel(e.target.value)}
          className="px-2 py-1 rounded"
        >
          {colorOptions.map((color) => (
            <option key={color} value={color}>{color}</option>
          ))}
        </select>
        <button
          onClick={() => handleScanCenter(selectedLabel)}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Scan Center
        </button>
      </div>
      
      <div ref={sketchRef}/>
      {/* <button
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
      </button> */}
    </div>
  );
};

export default SolvingCube;