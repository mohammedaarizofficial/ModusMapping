var config = {
    container_id: "viz",
    server_url: "bolt://localhost:7687",
    server_user: "neo4j",
    server_password: "lakshay1406",
    labels: {
        "Criminal": {
            caption: "name",
            size: "pagerank",
            community: "community"
        },
        "Person": {
            caption: "name",
            size: "degree"
        }
    },
    relationships: {
        "RELATED_TO": {
            caption: true,
            thickness: "weight"
        }
    },
    initial_cypher: "MATCH (n)-[r]-(m) RETURN n,r,m LIMIT 50"
};

var viz;
function draw() {
    viz = new NeoVis.default(config);
    viz.render();
}

draw();