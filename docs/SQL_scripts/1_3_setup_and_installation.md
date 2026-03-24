# 1.5 Setup and Installation

## Goal
Set the MotherDuck authentication token and verify that the connection works.

---

## Set the environment variable

Use your MotherDuck token as an environment variable.

### macOS / Linux
export MOTHERDUCK_TOKEN="your_token_here"

### Windows PowerShell (current session)
$env:MOTHERDUCK_TOKEN="your_token_here"

### Windows PowerShell (persistent for future sessions)
setx MOTHERDUCK_TOKEN "your_token_here"

## Test the connection

Open DuckDB and attach MotherDuck:

ATTACH 'md:';
SHOW DATABASES;

## Expected result

DuckDB should connect to MotherDuck and display the list of available databases.

## Notes

- $env:MOTHERDUCK_TOKEN=... works only in the current PowerShell session.
- setx persists the variable for future terminal sessions.
- You may need to restart your terminal after using setx.
- Do not commit real tokens to GitHub.
- Store secrets in .env or a secure password manager (e.g., Bitwarden).