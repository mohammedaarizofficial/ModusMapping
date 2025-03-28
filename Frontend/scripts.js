const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 5000;

// PostgreSQL Database Configuration
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'Aariz13518',
  port: 1351 // Ensure this matches your DB port
});

app.use(cors());
app.use(express.json());

// Search for a criminal based on ID, Name, or FIR Number
app.get('/search_criminal', async (req, res) => {
  try {
    const { criminal_id, name, fir_no } = req.query;
    
    let query = `
      SELECT c.id, c.name, c.date_of_birth, cr.fir_no, cr.location, cr.area
      FROM criminal_person c
      JOIN cc_mapping m ON c.id = m.criminal_id
      JOIN crime cr ON m.crime_id = cr.crime_id
      WHERE 1=1
    `;
    let values = [];

    if (criminal_id) {
      values.push(criminal_id);
      query += ` AND c.id = $${values.length}`;
    }
    if (name) {
        values.push(`%${name}%`); // Properly format the wildcard search
        query += ` AND c.name ILIKE $${values.length}`;
      }
      
    if (fir_no) {
      values.push(fir_no);
      query += ` AND cr.fir_no = $${values.length}`;
    }

    const result = await pool.query(query, values);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: "No records found." });
    }

    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching criminal records:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
