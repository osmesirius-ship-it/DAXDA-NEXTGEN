g# Deploying DAXDA on Hostinger VPS

**Author:** Manus AI  
**Date:** May 2026  
**Project:** DAXDA.IA (Nicole Protocol / 886-Ops Architecture)

---

This guide provides step-by-step instructions for deploying the DAXDA 886-Ops Python backend to a Hostinger Virtual Private Server (VPS). 

Hostinger provides raw, unmanaged VPS environments. Unlike a managed Kubernetes cluster or a PaaS like Heroku, you are responsible for process management, reverse proxying, and SSL termination. This guide uses **Systemd** to keep the Python application running and **Nginx** as a reverse proxy to handle web traffic securely.

## 1. Initial VPS Setup

After purchasing a Hostinger VPS (Ubuntu 22.04 or 24.04 is recommended), connect via SSH:

```bash
ssh root@<your-vps-ip>
```

Update the system packages to ensure you have the latest security patches:

```bash
apt update && apt upgrade -y
```

Install the necessary system dependencies:

```bash
apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git
```

## 2. Prepare the Application Environment

It is a security best practice to run web applications under a dedicated, non-root user.

```bash
# Create a dedicated user for the application
useradd -m -s /bin/bash daxda

# Switch to the new user
su - daxda
```

Clone your DAXDA repository (or upload the files via SFTP/SCP):

```bash
git clone https://github.com/your-username/daxda.git /home/daxda/app
cd /home/daxda/app
```

Set up an isolated Python Virtual Environment to prevent dependency conflicts with the system Python:

```bash
python3 -m venv venv
source venv/bin/activate

# Install the DAXDA dependencies
pip install -r requirements.txt
```

Test that the application starts manually:

```bash
uvicorn daxda.api.main:app --host 127.0.0.1 --port 8080
```

Press `Ctrl+C` to stop the server once you confirm it prints "Application startup complete."

Type `exit` to return to the `root` user session.

## 3. Configure Systemd for Process Management

To ensure DAXDA runs in the background and restarts automatically if the server reboots or the application crashes, we will create a Systemd service file.

Create the file `/etc/systemd/system/daxda.service`:

```ini
[Unit]
Description=DAXDA.IA 886-Ops Engine
After=network.target

[Service]
User=daxda
Group=daxda
WorkingDirectory=/home/daxda/app
Environment="PATH=/home/daxda/app/venv/bin"
Environment="PYTHONPATH=/home/daxda/app"

# Start Uvicorn bound only to localhost (Nginx will proxy external traffic)
ExecStart=/home/daxda/app/venv/bin/uvicorn daxda.api.main:app --host 127.0.0.1 --port 8080

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable daxda
systemctl start daxda
```

Verify it is running:

```bash
systemctl status daxda
```

## 4. Configure Nginx as a Reverse Proxy

Currently, DAXDA is running on port 8080, but it is only listening to `127.0.0.1` (localhost). We will use Nginx to listen on port 80 (HTTP) and proxy the traffic to DAXDA.

Create an Nginx configuration file at `/etc/nginx/sites-available/daxda`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com; # Replace with your actual domain

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Prevent Nginx from timing out during long 886-ops reasoning passes
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

Enable the site by linking it to the `sites-enabled` directory:

```bash
ln -s /etc/nginx/sites-available/daxda /etc/nginx/sites-enabled/
```

Test the Nginx configuration for syntax errors:

```bash
nginx -t
```

If the test is successful, restart Nginx:

```bash
systemctl restart nginx
```

## 5. Secure the Endpoint with SSL (HTTPS)

DAXDA processes sensitive reasoning and governance data. It must never be accessed over plain HTTP. 

Ensure your domain name (`api.yourdomain.com`) is pointing to your Hostinger VPS IP address in your DNS settings. Then, use Certbot to automatically provision a free Let's Encrypt SSL certificate and configure Nginx to use it:

```bash
certbot --nginx -d api.yourdomain.com
```

Certbot will ask for your email address and whether you want to redirect HTTP traffic to HTTPS. **Always choose to redirect.**

## 6. Verification

Your deployment is now complete. From your local machine, test the live endpoint:

```bash
curl -s https://api.yourdomain.com/health
```

You should receive the JSON health response confirming that the 886-Ops engine is online.

To run a full reasoning pass against your live server:

```bash
curl -X POST https://api.yourdomain.com/run \
  -H "Content-Type: application/json" \
  -d '{"input": "Is this system secure?", "runtime_mode": "full_886"}'
```

### Updating the Code

When you make changes to the DAXDA code and want to deploy them to the VPS, follow this sequence:

```bash
ssh root@<your-vps-ip>
su - daxda
cd /home/daxda/app
git pull origin main
exit
systemctl restart daxda
```
