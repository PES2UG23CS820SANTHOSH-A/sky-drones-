🚁 Skylark Drone Operations Coordinator – AI Agent

An AI-powered, chat-first operational dashboard to manage pilots, drones, and mission assignments for Skylark Drones.
The system combines Google Sheets sync, rule-based intelligence, and human-in-the-loop safety to reduce coordination overhead in high-stakes drone operations.

📌 Problem Overview

Skylark Drones manages:

Multiple pilots with different skills & certifications

A fleet of drones across locations and maintenance states

Concurrent client missions with varying priorities

Manual coordination using spreadsheets leads to:

High cognitive load

Frequent conflicts (double booking, skill mismatch)

Slow reaction during urgent reassignments

This project implements an AI agent that assists a Drone Operations Coordinator by:

Understanding natural language requests

Suggesting safe assignments

Handling urgent overrides

Syncing all changes back to Google Sheets

✨ Key Features
1️⃣ Pilot Roster Management

View available pilots

Filter by availability

Assign / unassign pilots to missions

Automatic status updates (Available → Unavailable)

Two-way sync with Google Sheets

2️⃣ Drone Inventory Management

View available drones

Track maintenance status

Prevent assigning drones under maintenance

Automatic deployment tracking

3️⃣ Mission Assignment Engine

Suggests pilot + drone combinations

Validates:

Availability

Skills & capabilities

Existing assignments

Requires explicit user confirmation before assignment

4️⃣ 🚨 Urgent Reassignment Mode

Overrides availability constraints

Used when missions are already assigned or blocked

Clear UI warnings before forcing assignment

Updates all related sheets consistently

5️⃣ Conversational Interface

Chat-based commands like:

show pilots

assign mission M101

urgent reassign M102

NLP-based intent detection

Combined with buttons to avoid accidental actions

🧠 System Architecture
streamlit_app/
│
├── app.py                     # Main Streamlit app
│
├── core/
│   ├── sheets_client.py       # Google Sheets connector
│   ├── pilot_manager.py       # Pilot logic
│   ├── drone_manager.py       # Drone logic
│   ├── matcher.py             # Normal assignment logic
│   ├── urgent_reassign.py     # Urgent override logic
│   └── nlp_client.py          # Intent parsing
│
├── config/
│   └── credentials.json       # Google API credentials
│
├── README.md
└── Decision_Log.md

🔄 Google Sheets Integration
Sheets Used

pilot_roster

drone_fleet

missions

Read Operations

Pilot availability

Drone status

Mission details

Write Operations

Pilot status updates

Drone deployment updates

Mission assignment updates

Google Sheets act as the single source of truth.

🧪 Assignment Logic (High-Level)
Normal Assignment

Only Available pilots & drones

Prevents double booking

Blocks already-assigned missions

Urgent Reassignment

Allows override

Explicit warning shown

Requires manual confirmation

Designed for emergency scenarios

🛡️ Safety & Error Handling

Prevents:

Double booking

Assigning unavailable drones

Silent overwrites

Displays:

Warnings

Clear error messages

Assignment confirmation

🚀 How to Run Locally
pip install -r requirements.txt
streamlit run app.py


Make sure credentials.json is configured for Google Sheets API access.

🌐 Deployment

The app can be hosted on:

Streamlit Cloud

HuggingFace Spaces

Railway / Render

No local setup required for evaluators.

📄 Decision Log

See Decision_Log.md for:

Assumptions

Trade-offs

Urgent reassignment interpretation

Future improvements

🔮 Future Improvements

Semantic skill matching using embeddings

Calendar-based conflict detection

Audit logs & role-based access

Multi-user session support

Full autonomous agent mode (optional)

👤 Author

Santhosh A
SRN:PES2UG23CS820
AI / Automation Engineer
Skylark Drones – Technical Assignment