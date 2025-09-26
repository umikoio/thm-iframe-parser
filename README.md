<div align="center">
  <img width="40%" src="assets/logo.png" />
  <h1>TryHackMe iframe Parser</h1>
  <p>Ingest profile data from TryHackMe's public iframe and convert it to JSON.</p>
</div>

This project is pretty simple in nature. It ingests the public iframe provided by TryHackMe, parses the incoming data, and converts it to JSON. The JSON report provides almost all of the data you would probably be interested in for sharing info about your TryHackMe account. This tool does not collect any private information or bypass any API infrastructure.

# Endpoints
| Title           | Data Type | Example
|-----------------|-----------|---------|
| Rank            | `String`  | 464176
| Streak          | `String`  | 30 days
| Badges          | `Integer` | 10
| Completed Rooms | `Integer` | 100
| Level           | `String`  | [0x5]

## Usage
```bash
python3 thm-iframe-parser.py --user 5672619 --output thm_user.json
```

## JSON Example
```json
{
  "userPublicId": "5672619",
  "Source URL": "https://tryhackme.com/api/v2/badges/public-profile?userPublicId=5672619",
  "Data": {
    "Rank": "464201",
    "Streak": "9 days",
    "Badges": "7",
    "Completed Rooms": "17",
    "Level": "[0x5]"
  }
}
```

> [!IMPORTANT]  
> At any time TryHackMe can change the HTML data within their iframe. This could potentially break the script. If you do notice any problems, feel free to open an [issue](https://github.com/umikoio/thm-iframe-parser/issues)!
