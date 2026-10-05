# ModusMapping

An AI-powered crime investigation and criminal relationship analysis platform that helps investigators analyze criminal networks, uncover hidden relationships, and generate AI-assisted investigative insights.

## Overview

ModusMapping is designed to assist law enforcement agencies by combining structured case records, graph databases, and Artificial Intelligence into a single investigation platform.

Traditional investigation systems store criminal records as isolated data, making it difficult to discover hidden connections between suspects, victims, organizations, vehicles, locations, and criminal activities.

ModusMapping solves this problem by integrating relational databases, graph databases, and Large Language Models (LLMs) to provide investigators with contextual insights and relationship-based intelligence.

---

## Features

- AI-assisted crime investigation
- Criminal relationship graph visualization
- Intelligent case search
- REST API backend
- Cross-database querying
- AI-generated investigation summaries
- Secure authentication
- Modular backend architecture
- Scalable API design

---

## System Architecture

```
                Frontend
                    │
                    │ REST API
                    ▼
            Flask Backend (Python)
                    │
     ┌──────────────┴──────────────┐
     │                             │
     ▼                             ▼
PostgreSQL                     Neo4j
Structured Data          Criminal Relationships
(Cases, Evidence,        (Suspects, Victims,
Users, Reports)           Organizations, Links)
     │                             │
     └──────────────┬──────────────┘
                    │
                    ▼
             LLM Integration
        AI Investigation Summary
```

---

## Technology Stack

### Backend

- Python
- Flask
- REST APIs

### Databases

- PostgreSQL
- Neo4j

### AI

- Large Language Models (LLMs)

### Development

- Git
- Postman

---

## Core Features

### Criminal Relationship Analysis

Represent criminals, victims, organizations, vehicles, locations, and incidents as a graph.

Investigators can instantly visualize relationships that would otherwise require manually reviewing thousands of records.

---

### AI Investigation Assistant

Investigators can query cases and receive AI-generated summaries that explain:

- Criminal associations
- Patterns
- Similar historical cases
- Investigation recommendations

---

### REST API

The backend exposes secure REST APIs for:

- Case management
- Criminal records
- Relationship queries
- Evidence retrieval
- AI summary generation

---

### Cross Database Querying

ModusMapping combines two different database models:

**PostgreSQL**

Stores structured information including:

- Case files
- Users
- Evidence
- Reports
- Investigation logs

**Neo4j**

Stores relationship-based information including:

- Criminal associations
- Organization links
- Vehicles
- Phone numbers
- Financial transactions
- Locations

The backend combines data from both databases into a unified investigation response.

---

## Security

- Secure REST API design
- Input validation
- Role-based access
- Protected endpoints
- Secure database access

---

## Project Goals

- Reduce investigation time
- Improve criminal network discovery
- Enhance investigative decision making
- Provide AI-powered investigative assistance
- Scale to support enterprise law-enforcement systems

---

## Future Improvements

- Real-time crime analytics
- Predictive crime pattern detection
- Facial recognition integration
- Geographic crime heatmaps
- Mobile investigator application
- Multi-agency collaboration
- Evidence timeline visualization

---

## Learning Outcomes

This project strengthened my understanding of:

- Backend architecture
- REST API development
- Flask
- PostgreSQL
- Neo4j graph databases
- Database design
- AI integration
- Large Language Models
- System architecture
- Enterprise software development

---

## Author

**Mohammed Aariz**

GitHub: https://github.com/mohammedaarizofficial
