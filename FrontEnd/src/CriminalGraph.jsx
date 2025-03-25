import React, { useEffect, useRef } from "react";
import NeoVis from "neovis.js";

const CriminalGraph = () => {
  const visRef = useRef(null);

  useEffect(() => {
    const config = {
      containerId: "neo4j-graph",
      neo4j: {
        serverUrl: "bolt://localhost:7687",
        serverUser: "neo4j",
        serverPassword: "your_password", // Change this
      },
      labels: {
        Criminal: {
          caption: "name", // Show criminal name
          size: "age", // Set node size by age
          community: "modus_operandi",
        },
      },
      relationships: {
        // Instead of filtering by relationship type, apply to all
        "": {
          caption: "type", // Show relationship type
          thickness: "weight",
        },
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
