# Building You Own Whois

The whois tool allows us to look up registration details for a domain, IP address (or block of) and autonomous system (AS). If you’re not aware ASes are used in BGP routing and are a key part of the infrastructure of the Internet.

The whois tool relies on the WHOIS protocol which is defined in RFC 3912. In this coding challenge you’re going to implement your own whois tool that will use the protocol to lookup details of hosts and IP addresses.

---

# Whois-py

A Python implementation of the WHOIS protocol for querying domain and IP address information. This tool provides recursive WHOIS lookups, automatically following referral servers to get complete information.

## Features

- **Recursive WHOIS Queries**: Automatically follows referral servers to get complete domain/IP information
- **Support for Both Domains and IP Addresses**: Handles both domain names and IPv4/IPv6 addresses
- **Raw Response Display**: Shows the complete raw WHOIS response for transparency
- **Error Handling**: Graceful error handling for network issues and server problems
- **Clean Output**: Parses and displays WHOIS data in a readable format

## Installation

### Prerequisites

- Python 3.6 or higher
- Internet connection for WHOIS queries

### Setup

1. Clone or download the repository:
```bash
git clone <repository-url>
cd Whois-py
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. The script is ready to use - no additional dependencies required!

## Usage

### Basic Usage

```bash
python whois.py <domain_or_ip>
```

### Examples

Query a domain:
```bash
python whois.py example.com
```

Query an IP address:
```bash
python whois.py 8.8.8.8
```

Query an IPv6 address:
```bash
python whois.py 2001:4860:4860::8888
```

### Output

The tool will:
1. Start with the default WHOIS server (whois.iana.org)
2. Display the raw WHOIS response
3. Parse the response to find referral servers
4. Automatically query referral servers if found
5. Continue until no more referrals are available

Example output:
```
=== Querying whois.iana.org ===
% IANA WHOIS server
% for more information on IANA services, go to http://www.iana.org
%
% This query returned 1 object

refer:        whois.verisign-grs.com

=== Querying whois.verisign-grs.com ===
Domain Name: EXAMPLE.COM
Registry Domain ID: 2336799_DOMAIN_COM-VRSN
...
```

## How It Works

1. **Initial Query**: Starts with `whois.iana.org` as the default server
2. **Response Parsing**: Parses the WHOIS response to extract key-value pairs
3. **Referral Detection**: Looks for referral servers in the response
4. **Recursive Queries**: Automatically queries referral servers until no more are found
5. **Error Handling**: Gracefully handles network errors and server issues

## Key Functions

- `whois_query(query, server, port)`: Performs a single WHOIS query
- `parse_whois_response(response)`: Parses raw WHOIS response into structured data
- `get_referred_server(parsed)`: Extracts referral server information
- `is_ip_address(query)`: Detects if the query is an IP address
- `whois_recursive(query, start_server)`: Performs recursive WHOIS lookups

## Technical Details

- **Protocol**: Uses TCP port 43 (standard WHOIS port)
- **Encoding**: UTF-8 with error handling for malformed responses
- **Network**: Raw socket implementation for direct WHOIS protocol communication
- **Parsing**: Handles both single values and multiple values for the same key
