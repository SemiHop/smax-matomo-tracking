# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Matomo tracking integration for SMAX (Micro Focus Service Management Automation X), designed to track user interactions in a Single Page Application environment. The project consists of:

- **smax-matomo-tracking.js**: Client-side JavaScript tracking script that monitors URL changes, page views, and navigation events in SMAX
- **HTTPS servers**: Two Python-based HTTPS servers (Linux and Windows versions) to serve the tracking script with CORS headers

## Architecture

### Tracking Script (smax-matomo-tracking.js)

The tracking script uses three mechanisms to detect SPA navigation:

1. **Polling**: Checks for URL/title changes every 2 seconds via `setInterval`
2. **popstate listener**: Captures browser back/forward navigation
3. **hashchange listener**: Detects hash-based routing changes

All tracking events are pushed to the `_paq` array (Matomo's standard tracking queue).

### HTTPS Servers

Two server implementations exist:

- **simple_https_server.py**: Unix/Linux version using `os.system` for OpenSSL commands
- **windows_https_server.py**: Windows-compatible version using `subprocess` module and enhanced error handling

Both servers:
- Listen on port 4443
- Auto-generate self-signed SSL certificates if not present
- Include CORS headers (`Access-Control-Allow-Origin: *`) for cross-origin requests
- Serve JavaScript files with appropriate Content-Type and caching headers

## Development Commands

### Running the HTTPS Server

**Linux/Unix:**
```bash
python3 simple_https_server.py
```

**Windows:**
```bash
python windows_https_server.py
```

**Prerequisites:**
- OpenSSL must be installed and available in PATH
- Python 3.x

### Testing the Tracking Script

1. Start the HTTPS server
2. Access the script at `https://localhost:4443/smax-matomo-tracking.js`
3. Browser will show security warning (self-signed certificate) - accept and proceed
4. Include the script in your SMAX environment via browser extension or injection

## Key Configuration

- **Matomo URL**: `https://microfocus.matomo.cloud/`
- **Site ID**: `1`
- **Tracking interval**: 2000ms (2 seconds)
- **Server port**: 4443
- **Certificate files**: `server.crt`, `server.key` (auto-generated)

## Important Notes

- The servers use self-signed certificates, which will trigger browser security warnings
- CORS is set to allow all origins (`*`) for development purposes
- The tracking script logs to console for debugging (`console.log` statements throughout)
- Certificate files (`server.crt`, `server.key`) are auto-generated on first run and should not be committed to production repositories
