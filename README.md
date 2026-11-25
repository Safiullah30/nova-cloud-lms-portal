# nova cloud — Student LMS Portal (lms-portal)
**RFP Exercise:** DESC/SKR/2026/012 — Hybrid Cloud-Native Application Platform (DESC Shankar, Mardan)

## 1. Quick Start
git clone https://github.com/Safiullah30/nova-cloud-lms-portal.git
cd nova-cloud-lms-portal
docker build --network=host -t nova-cloud/lms-portal:v1.0.0 .
docker run -d --name lms-portal -p 5000:5000 -e APP_ENV="k3s-dev" nova-cloud/lms-portal:v1.0.0
curl http://localhost:5000/health

## 2. Team Roles & Tasks
* Hafsa (Team Lead — Platform Architect): docs-finance/ — Hybrid architecture diagram, 6-phase work plan, aur risk register.
* Shabeer (DevOps Engineer): .github/workflows/ + baqi 3 apps — CI/CD workflow aur baqi 3 simple apps ke containers.
* Safiullah (Cloud & Infrastructure Engineer): k8s/ — K3s manifests aur AWS production infrastructure design.
* Muskan (QA, Security & Documentation Lead): security-qa/ — Secrets/RBAC/security, monitoring/alerts, backup/DR, aur T1-T10 test checklist.
* Rehanullah (Finance & Operations Lead): docs-finance/ — PKR cost breakdown (PKR 10,000,000 ceiling) aur 3-year TCO.
