require('dotenv').config();
const fastify = require('fastify')({ logger: true });
const { Client } = require('pg');
const path = require('path');

// PostgreSQL connection setup
const client = new Client({
  host: 'localhost',
  user: 'postgres',
  password: process.env.PG_PASSWORD,
  database: process.env.PG_DATABASE,
  port: process.env.PG_PORT,
});
client.connect();

// Serve static files (HTML/CSS)
fastify.register(require('@fastify/static'), {
  root: path.join(__dirname, 'public'),
  prefix: '/',
});

// Parse form data
fastify.register(require('@fastify/formbody'));

fastify.register(require('fastify-cors'), { 
  origin: '*' 
});
// Route: Show the form
fastify.get('/', (req, reply) => {
  reply.type('text/html').sendFile('index.html');
});

// Route: Add criminal record
fastify.post('/add-criminal', async (req, reply) => {
  const { name, dob, description, uniqueIdentifier, people, firNumber} = req.body;
  
  try {
    const result = await client.query(
      'INSERT INTO criminal_person (name, date_of_birth, description, unique_identification) VALUES ($1, $2, $3, $4) RETURNING id',
      [name, dob, description, uniqueIdentifier]
    );

    const criminalId = result.rows[0].id;
    const crimeResult = await client.query(
      'SELECT crime_id FROM crime WHERE fir_no = $1',
      [firNumber]
    );
    if (crimeResult.rows.length === 0) {
      // If no matching crime is found, handle it accordingly:
      console.error("No crime found with FIR number:", firNumber);
      return reply.status(404).send({ error: 'No crime found for the given FIR number' });
    }
    
    const crimeId = crimeResult.rows[0].crime_id;
    
    //insert into cc_mapping 
    await client.query(
      'INSERT INTO cc_mapping (crime_id, criminal_id ) VALUES ($1, $2)',
      [crimeId ,criminalId]
    );

    // Insert related people if provided
    if (Array.isArray(people) && people.length > 0) {
      for (const person of people) {
        var presult = await client.query(
          'INSERT INTO persons (name, date_of_birth) VALUES ($1, $2) RETURNING person_id',
          [person.personName, person.personDob]
        );
        var personId = presult.rows[0].person_id
        await client.query(
          'INSERT INTO related_to (person_id, criminal_id, relationship) VALUES ($1, $2, $3) ',
          [personId, criminalId, person.relation]
        );
      }
    }

    reply.send({ success: true, id: criminalId });
  } catch (err) {
    console.error(err);
    reply.status(500).send({ error: 'Failed to add record' });
  }
});

// Route: Add crime record
fastify.post('/add-crime', async (req, reply) => {
  const { type, location, area,modusOperandi, date, status, firNumber, bailDetails, bailGrantDate, progress, victimDetails } = req.body;

  try {
    await client.query(
      'INSERT INTO crime (type, location, area,modus_operandi, date, fir_status, fir_no, bail_details, bail_grant_date, trial_progress, victim_name) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)',
      [type, location, area,modusOperandi, date, status, firNumber, bailDetails, bailGrantDate, progress, victimDetails]
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
