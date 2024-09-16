# Cloudflare Zero Trust Access Group IP Updater

This Docker container fetches the public IP address of the host it is running on and updates a Cloudflare Zero Trust Access Group by adding the current public IP to the group. It also accepts a comma-separated list of additional IPs to whitelist. The updates are made at a configurable interval.

## Features:
- Fetches the current public IP address from `https://ip.tiippex.de`.
- Adds the current public IP to Cloudflare Zero Trust's Access Group.
- Accepts a list of IPs addresses to whitelist alongside the public IP.
- Runs at a user-defined interval (in minutes), or runs once and exits if no interval is specified.

## Prerequisites:
- A Cloudflare API key with permissions to manage Access Groups in Zero Trust.
- The Cloudflare account ID from your Cloudflare dashboard.
- The Access Group ID from your Zero Trust dashboard.
- Docker installed on the system.

## API Key Permissions:

- When creating the API token in Cloudflare, set the following permission for the token:
   - **Account** > **Access: Organizations, Identity Providers, and Groups** > **Edit**.

## Environment Variables:

- **`CLOUDFLARE_API_KEY`**: Your Cloudflare API key (required).
- **`CLOUDFLARE_ACCOUNT_ID`**: The account ID from your Cloudflare dashboard (required).
- **`CLOUDFLARE_GROUP_ID`**: The Access Group ID from your Zero Trust dashboard (required).
- **`IP_RANGE`**: A comma-separated list of IPs to whitelist (optional, public IP will always be added).
- **`UPDATE_INTERVAL_MINUTES`**: Time in minutes between updates (optional). If not set, the script will run once and then stop.

## Build and Run the Docker Image:

To build the Docker image, run the following command:

```bash
docker build -t cloudflare-access-group-ip-updater .
```

To run the Docker container with necessary environment variables:

```bash
docker run -e TZ=Europe/Berlin \
           -e CLOUDFLARE_API_KEY=your_api_key \
           -e CLOUDFLARE_ACCOUNT_ID=your_account_id \
           -e CLOUDFLARE_GROUP_ID=your_group_id \
           -e IP_RANGE="127.0.0.1,10.0.0.0/24" \
           -e UPDATE_INTERVAL_MINUTES=15 \
           tiippex/cloudflare-access-group-ip-updater:latest
```

## Docker Compose Example:

Below is an example `docker-compose.yml` file that you can use to set up the container using Docker Compose:

```yaml
version: "3"
services:
  cloudflare-access-group-updater:
    image: tiippex/cloudflare-access-group-ip-updater:latest
    environment:
      - TZ=Europe/Berlin
      - CLOUDFLARE_API_KEY=your_api_key
      - CLOUDFLARE_ACCOUNT_ID=your_account_id
      - CLOUDFLARE_GROUP_ID=your_group_id
      - IP_RANGE=127.0.0.1,10.0.0.0/24
      - UPDATE_INTERVAL_MINUTES=15
    restart: always
```

## How to Use Docker Compose:

1. Create a `docker-compose.yml` file in your working directory with the content shown above.
2. Replace the environment variable values with your own Cloudflare API key, account ID, group ID, and desired IP list.
3. Run the following command to start the container:

   ```bash
   docker-compose up -d
   ```

This will start the container and run the Cloudflare Access Group updater at the specified interval.

### Running the Script Without `UPDATE_INTERVAL_MINUTES`:

If the `UPDATE_INTERVAL_MINUTES` variable is not set, the script will run once, update the Access Group with the public IP and any provided IP ranges, and then exit. This is useful for running the script as a one-time task instead of as a long-running service.
