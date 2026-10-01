# Spartans Gameday (Netlify project `spartans-gameday`, base directory `stats`)

Backend for the Spartans Game Tracker app:

- **Visitor counter**: `POST /api/hit` (one ping per app open; random device ID only), `GET /api/stats`, stats page at `/`
- **Watch parties**: `POST /api/party` (create/update, host key required to edit), `GET /api/party?id=`
- **Answers**: `POST /api/rsvp` (one answer per phone; host can remove)
- **Invite page**: `/p/<party id>` (friends answer here; `?via=Name` shows who forwarded it)
