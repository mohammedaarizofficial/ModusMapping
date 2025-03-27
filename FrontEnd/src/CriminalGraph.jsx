import React, { useEffect, useRef } from "react";
import NeoVis from "neovis.js";

const CriminalGraph = () => {
  const visRef = useRef(null);

  useEffect(() => {
    const config = {
        containerId: "neo4j-graph",
        consoleDebug: true, // ✅ Enable console debugging
        neo4j: {
          serverUrl: "bolt://localhost:7689",
          serverUser: "neo4j",
          serverPassword: "Aariz13518",
        },
        labels: {
          Criminal: {
            caption: "criminal_name",
            size: "age",
            community: "modus_operandi",
          },
        },
        relationships: {
          "*": { caption: "type", thickness: "weight" }, // ✅ Show all relationships
        },
        initialCypher: `
          MATCH (c:Criminal)-[r]->(c2:Criminal)
          RETURN c, r, c2
        `,
      };
      
    visRef.current = new NeoVis(config);
    visRef.current.render();

    return () => {
      visRef.current = null;
    };
  }, []);

  return <div id="neo4j-graph" style={{ width: "100%", height: "500px" }}></div>;
};

export default CriminalGraph;
