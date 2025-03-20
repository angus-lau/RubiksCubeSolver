import P5Sketch from "@/components/p5rubikscube";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl font-bold mb-4"></h1>
      <P5Sketch />
    </div>
  );
}