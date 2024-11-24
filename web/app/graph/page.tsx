"use client";

import { useSearchParams } from "next/navigation";
import { Graph } from "@/components/Graph";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";

export default function GraphPage() {
  const searchParams = useSearchParams();
  const data = JSON.parse(decodeURIComponent(searchParams.get("data") || "{}"));

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
      <div className="h-screen flex">
        <div className="flex-1 p-6 overflow-hidden">
          <Graph className="h-full" />
        </div>

        <div className="w-96 border-l border-gray-800 flex flex-col">
          <div className="p-4 border-b border-gray-800 bg-gray-900">
            <h1 className="text-xl font-bold text-gray-100 mb-2">{data.prompt}</h1>
            {data.options && data.options.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {data.options.map((option: string) => (
                  <span
                    key={option}
                    className="px-2 py-1 bg-blue-600/20 text-blue-400 rounded-full text-xs"
                  >
                    {option}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
          </div>

 
          <div className="p-4 border-t border-gray-800 bg-gray-900">
            <form className="flex gap-2">
              <Input
                placeholder="Type your message..."
                className="flex-1 bg-gray-800 border-gray-700 text-gray-100"
              />
              <Button size="icon" className="bg-blue-600 hover:bg-blue-700">
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}