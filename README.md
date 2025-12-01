#  High Availability Distributed Storage with Ceph Cluster

![Ceph](https://img.shields.io/badge/Ceph-Distributed_Storage-EF4A50?style=for-the-badge&logo=ceph)
![Ubuntu](https://img.shields.io/badge/Ubuntu-Server-E95420?style=for-the-badge&logo=ubuntu)
![Python](https://img.shields.io/badge/Python-Automation-3776AB?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Alerting-26A5E4?style=for-the-badge&logo=telegram)

##  Overview
This project demonstrates the implementation of a **3-Node Ceph Cluster** using **MicroCeph** on Ubuntu Server. The primary goal is to simulate a production-grade distributed storage environment, implement real-time monitoring via Telegram, and perform **Chaos Engineering** tests to verify High Availability (HA) and Self-healing capabilities.

## ️ Architecture
The cluster consists of 3 Virtual Machines interconnected via a local network:

| Node Name | Role | OS | Configuration |
| :--- | :--- | :--- | :--- |
| **ceph-node1** | Monitor, Manager, OSD | Ubuntu 22.04 LTS | 2 vCPU, 2GB RAM, 10GB OSD Disk |
| **ceph-node2** | Monitor, OSD | Ubuntu 22.04 LTS | 2 vCPU, 2GB RAM, 10GB OSD Disk |
| **ceph-node3** | Monitor, OSD | Ubuntu 22.04 LTS | 2 vCPU, 2GB RAM, 10GB OSD Disk |

* **Total Storage Pool:** ~30GB (Raw)
* **Replication Factor:** 3 (Data is replicated across all nodes for redundancy)

##  Key Features
1.  **Distributed Storage:** Unified storage solution supporting Block, File (CephFS), and Object storage.
2.  **Real-time Monitoring System:**
    * Custom Python daemon running as a **Systemd Service**.
    * Parses Ceph status JSON output.
    * Sends instant alerts to **Telegram** upon health status changes (e.g., `HEALTH_OK` -> `HEALTH_WARN`).
    * Secure credential management using `.env`.
3.  **High Availability (HA):** Zero-downtime data writing during node failures.

## eployment Steps

### 1. Cluster Bootstrap (MicroCeph)
Installing and bootstrapping the cluster on Node 1:
```bash
sudo snap install microceph
sudo microceph cluster bootstrap
