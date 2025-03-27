const fastify = require('fastify')({ logger: true });
const { Client } = require('pg');

// PostgreSQL connection setup
const client = new Client({
  host: 'localhost',
  user: 'postgres',
  password: 'lakshay',
  database: 'modusmapping',
});
client.connect();

// Serve static files (HTML/CSS)
fastify.register(require('@fastify/static'), {
  root: require('path').join(__dirname, 'public'),
  prefix: '/',
});

// Parse form data
fastify.register(require('@fastify/formbody'));

// Route: Show the form
fastify.get('/', (req, reply) => {
  reply.type('text/html').sendFile('index.html');
});

// Route: Add criminal record
fastify.post('/add-criminal', async (req, reply) => {
  const { name, age, description, uniqueIdentifier } = req.body;

  try {
    const result = await client.query(
      'INSERT INTO criminals (name, age, description, unique_identifier) VALUES ($1, $2, $3, $4) RETURNING id',
      [name, age, description, uniqueIdentifier]
    );

    reply.send({ success: true, id: result.rows[0].id });
  } catch (err) {
    console.error(err);
    reply.status(500).send({ error: 'Failed to add record' });
  }
});

// Route: Add crime record
fastify.post('/add-crime', async (req, reply) => {
  const { crimeId, criminalId, type, location, status, firNumber, bailDetails, bailGrantDate, progress, victimDetails } = req.body;

  try {
    await client.query(
      'INSERT INTO crimes (crime_id, criminal_id, type, location, status, fir_number, bail_details, bail_grant_date, progress, victim_details) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
      [crimeId, criminalId, type, location, status, firNumber, bailDetails, bailGrantDate, progress, victimDetails]
    );

    reply.send({ success: true });
  } catch (err) {
    console.error(err);
    reply.status(500).send({ error: 'Failed to add crime record' });
  }
});

// Start the server
fastify.listen({ port: 3000 }, (err, address) => {
  if (err) throw err;
  console.log(`Server running on ${address}`);
});

