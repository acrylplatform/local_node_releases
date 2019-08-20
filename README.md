# Acryl Local Node releases
This repo is for publishing releases only.

## Download

Download latest release from [releases page](https://github.com/acrylplatform/local_node_releases/releases)

Currently supported OS: CentOS 7

## Setup

Run 
```bash
yum localinstall acryl-local-node-VERSION.rpm
```

After successful installation run 
```bash
systemctl enable acryl_node.service
systemctl start acryl_node.service
```

Check service:

```bash
systemctl status acryl_node.service
```

Node config files and data located at `/opt/acryl`

### Node API

```bash
systemctl enable acryl_nginx.service
systemctl start acryl_nginx.service
```

Node API is accessed from the URL: `http://YOUR_IP/`

Web server (nginx) config located at `/opt/acryl/acryl_nginx.conf`
 

## Updating
To update node run:
```bash
systemctl start acryl_node_update.service
``` 
By default update is running every hour (see `acryl_node_update.timer`)

## Troubleshooting

* Service status is not active after start

    Check log files at `/opt/acryl/acryl/logs` and systemd journal

* nginx always returns 403 code
    
    If selinux is enabled and its mode is enforcing allow http network connections:
    ```bash
    setsebool -P httpd_can_network_connect on
    ```