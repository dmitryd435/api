### 1. Infrastructure Setup (Terraform & Local Environment)

1. Create a GitHub account.
2. Create a public repository for infrastructure: [infrastructure](https://github.com/dmitryd435/infrastructure).
3. Generate a token with the following permissions: `repo`, `workflow`, `read:org`, `read:discussion`, `write:packages` [Create a token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
4. Add the token as a variable in GitHub Secrets for CI/CD.
5. Clone the repository to your local machine if necessary.
6. Add the following files: `terraform.tf`, `.github/workflows/tf_deploy.yml`, `variables.tf`, `.gitignore`.
7. Push the code to GitHub if working locally.
8. Ensure the API repository is created.

### 2. Application Setup (Docker & Kubernetes)

1. Add required variables (`DB_NAME`, `DB_PASSWORD`, `DB_USER`, `TOKEN`) to GitHub Secrets for CI/CD.
2. Clone the API repository to your local machine if necessary.
3. The Python application code has been generated by ChatGPT.
4. Create and add necessary YAML manifests for Kubernetes, Docker, application files, and CI/CD pipeline.
5. Set up a new server on AWS (`t2.large` with a 15GB disk) running DebianOS 12 for Minikube:
    - Install [Helm](https://helm.sh/docs/intro/install/), [Docker](https://docs.docker.com/engine/install/debian/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), [Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fdebian+package), and self-hosted [GitHub Runner](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners) for the API repository.
6. Install [prometheus-and-grafana](https://mahira-technology.medium.com/how-to-set-up-minikube-prometheus-and-grafana-for-monitoring-your-application-performance-a-808a52b0812f).
7. Start Minikube: ```minikube start --driver=docker```
8. Created secret k8s for github packages:```kubectl create secret docker-registry ghcr-secret --docker-server=ghcr.io --docker-username=your_github-username --docker-password=GITHUB_TOKEN  --docker-email=yourgithub@mail.com```
9. Scans code for secrets enabled by default in repo settings.
10. Deployed application by Github Actions to minirube.

    

