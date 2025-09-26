<div align="center">
  <img width="40%" src="assets/logo.png" />
  <h1>TryHackMe iframe Parser</h1>
  <p>Ingest profile data from TryHackMe's public iframe and convert it to JSON.</p>
</div>

This project is pretty simple in nature. It ingests the public iframe provided by TryHackMe and parses the incoming data, converting it to JSON for easy parsing down the line.

The schema provides almost all of the data you would probably be interested in. The only thing we don't collect is the user's avatar. This tool does not collect any private information or bypass any API infrastructure.

# Endpoints
| Title           | Data Type | Example
|-----------------|-----------|---------|
| Rank            | `String`  | 464176
| Streak          | `String`  | 40 days
| Badges          | `Integer` | 7
| Completed Rooms | `Integer` | 100
| Level           | `String`  | [0x5]
