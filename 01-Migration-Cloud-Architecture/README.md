# Stratégie de Migration Cloud & Analyse FinOps : OptiGreen

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white) ![FinOps](https://img.shields.io/badge/FinOps-Cost_Optimization-green?style=for-the-badge)

## 📋 Présentation du projet

Ce projet, réalisé dans le cadre de ma certification Data Engineer, simule une mission de **consulting en architecture cloud**. Le client, *OptiGreen Solutions* (entreprise d'énergies renouvelables), souhaite migrer son infrastructure informatique interne (On-Premise) vers le cloud pour gagner en scalabilité, sécurité et agilité.

Mon rôle a été d'auditer l'infrastructure existante, de comparer les fournisseurs cloud (Benchmark), de concevoir une architecture **Cloud Native** sur Microsoft Azure et de réaliser une estimation financière précise (FinOps).

> **Note :** Ce projet démontre ma capacité à analyser des besoins infrastructurels et à concevoir des solutions Azure adaptées aux contraintes d'entreprise (Coûts, Sécurité, Haute Disponibilité).

## 🎯 Objectifs Pédagogiques

*   **Audit d'infrastructure :** Cartographier les données et les serveurs existants.
*   **Architecture Cloud :** Concevoir une solution cible (PaaS/SaaS) plutôt qu'un simple "Lift & Shift".
*   **Benchmark :** Comparer Azure, AWS et GCP sur des critères techniques et financiers.
*   **FinOps :** Calculer le TCO (Total Cost of Ownership) et optimiser les coûts mensuels.
*   **Sécurité :** Proposer une stratégie de sécurisation (Firewall, Identity Management).

## 🛠 Outils et Technologies

*   **Cloud Provider :** Microsoft Azure.
*   **Services Azure proposés :** Azure Kubernetes Service (AKS), Azure SQL Database, Azure IoT Hub, Azure Blob Storage, Azure Active Directory.
*   **Outils d'analyse :** Azure Pricing Calculator, Microsoft Excel (TCO), Azure Migrate (analyse théorique).
*   **Concepts clés :** Cloud Native, FinOps, SLA, Disaster Recovery (Azure Site Recovery).

## 📊 Architecture et Stratégie de Migration

### 1. Diagramme de Migration (On-Premise vers Azure)

```mermaid
graph LR
    subgraph On_Premise ["Infrastructure Actuelle (On-Premise)"]
        direction TB
        ServerApp[17 VMs Application]
        DB_SQL[SQL Server / MySQL]
        NAS[NAS Stockage Fichiers]
        IoT_Local[Serveur NodeJS Local]
        Network_Local[MPLS & Fortigate FW]
    end

    subgraph Azure_Target ["Cible : Azure Cloud Native"]
        direction TB
        AKS[Azure Kubernetes Service (AKS)]
        AzSQL[Azure SQL Database]
        Blob[Azure Blob Storage]
        IoTHub[Azure IoT Hub]
        AzNet[Azure VNet + Azure Firewall]
    end

    ServerApp -->|Migration & Containerisation| AKS
    DB_SQL -->|Migration PaaS| AzSQL
    NAS -->|Migration Données| Blob
    IoT_Local -->|Refonte IoT| IoTHub
    Network_Local -->|Sécurité Cloud| AzNet

    style On_Premise fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Azure_Target fill:#e6f7ff,stroke:#0078d4,stroke-width:2px
