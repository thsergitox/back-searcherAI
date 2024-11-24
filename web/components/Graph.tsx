"use client";

import { useEffect, useRef } from "react";
import NeoVis, { NeovisConfig } from "neovis.js";
import { Card } from "@/components/ui/card";
import { Neo4jConfig, DEFAULT_CONFIG } from "@/lib/neo4j-config";

interface GraphProps {
  config?: Partial<Neo4jConfig>;
  className?: string;
}

export function Graph({ config = {}, className = "" }: GraphProps) {
  const visRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const drawGraph = async () => {
      if (!visRef.current) return;

      const finalConfig = { ...DEFAULT_CONFIG, ...config };

      const neovisConfig: NeovisConfig = {
        container_id: visRef.current.id,
        server_url: finalConfig.serverUrl,
        server_user: finalConfig.serverUser,
        server_password: finalConfig.serverPassword,
        initial_cypher: finalConfig.initialCypher,
        labels: {
          Node: {
            caption: "name",
            size: "pagerank",
            community: "community",
          },
        },
        relationships: {
          RELATES_TO: {
            thickness: "weight",
            caption: true,
          },
        },
        initial_cypher: finalConfig.initialCypher,
        visConfig: {
          nodes: {
            shape: "circle",
            font: {
              size: 12,
              color: "#ffffff",
            },
            borderWidth: 2,
            shadow: true,
          },
          edges: {
            font: {
              size: 10,
              color: "#ffffff",
            },
            arrows: {
              to: { enabled: true },
            },
          },
        },
      };

      const vis = new NeoVis(neovisConfig);
      vis.render();
    };

    drawGraph();
  }, [config]);

  return (
    <Card className={`h-full bg-gray-900 border-gray-800 ${className}`}>
      <div 
        id="neovis" 
        ref={visRef} 
        className="w-full h-full bg-gray-800 rounded-lg"
      />
    </Card>
  );
}