# Spartans Tracker Stats

Visitor counter for the Spartans Game Tracker, hosted as the Netlify project
`spartans-tracker-stats` (base directory: `stats`).

- `POST /api/hit` - the app calls this once per open (random device ID only; no names or IPs)
- `GET /api/stats` - totals by day and by state
- `/` - the stats page
