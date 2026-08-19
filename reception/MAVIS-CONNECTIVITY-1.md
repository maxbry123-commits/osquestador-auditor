# 🔌 Mavis Connectivity Guide — Cómo me conecto a todo

**Fecha:** 2026-07-21
**Versión:** v1.0
**Autor:** Mavis (Max's agent)

---

# ÍNDICE

1. [Mi entorno: el sandbox donde corro](#1-mi-entorno)
2. [Arquitectura de red y seguridad](#2-arquitectura-de-red)
3. [Protocolos y métodos de conexión](#3-protocolos-y-métodos)
4. [Servicios y plataformas soportadas](#4-servicios-soportados)
5. [Tabla completa de credenciales necesarias](#5-credenciales)
6. [Cómo almaceno y uso los secretos](#6-secret-storage)
7. [Conexión a tu VPS Contabo](#7-contabo)
8. [Conexión a GitHub](#8-github)
9. [Conexión a Cloudflare](#9-cloudflare)
10. [Conexión a Vercel](#10-vercel)
11. [Conexión a otros providers (DO, Hetzner, AWS, Railway, Render)](#11-otros-providers)
12. [Conexión a bases de datos](#12-databases)
13. [Conexión a servicios de AI/LLM](#13-ai-llm)
14. [Conexión a storage (S3, R2, MinIO, Backblaze)](#14-storage)
15. [Conexión a monitoreo y observabilidad](#15-monitoring)
16. [Conexión a comunicación (Slack, Discord, email, webhooks)](#16-comunicacion)
17. [Conexión a payment (Stripe, PayPal, Razorpay)](#17-payment)
18. [Conexión a auth (Auth0, Clerk, Supabase Auth)](#18-auth)
19. [Sobre MCP (Model Context Protocol)](#19-mcp)
20. [Seguridad y buenas prácticas](#20-seguridad)
21. [Cómo darme credenciales nuevas](#21-como-darme-credenciales)
22. [Límites y restricciones](#22-límites)

---

# 1. Mi entorno: el sandbox donde corro

## 1.1 Tipo de sandbox

Yo (Mavis) corro en un **cloud sandbox Linux efímero/persistente** según la configuración:

- **OS:** Linux (basado en Ubuntu/Debian)
- **Arquitectura:** x86_64
- **Networking:** egress permitido (salida a internet), ingreso bloqueado por default
- **Filesystem:** root persistente dentro de `/workspace` durante la sesión
- **Volumen:** efímero fuera de `/workspace` (se pierde entre sesiones)
- **Shell:** bash con sudo limitado
- **Lenguajes disponibles:** Python 3, Node.js, Go, Rust, y binarios comunes (git, curl, ssh, kubectl, docker client, etc.)

## 1.2 Herramientas (tools) que tengo nativas

| Categoría | Tools |
|---|---|
| **Filesystem** | `read`, `write`, `edit`, `glob`, `grep` |
| **Shell** | `bash` (sync o background) |
| **Web** | `web_search`, `web_fetch` (default + `deep` mode) |
| **Imágenes** | `image_synthesize` (batch), `images_search_and_download`, `image_reverse_search` |
| **Video** | `gen_videos` (batch), `batch_text_to_video`, `batch_image_to_video` |
| **Audio** | `synthesize_speech`, `batch_text_to_audio`, `audios_understand`, `listen_audio`, `clone_voice`, `upload_clone_audio` |
| **Música** | `batch_text_to_music` |
| **Memoria** | 11 funciones de `memory_*` (read, append, edit, search, topics, summary) |
| **Secretos** | `secret` (list, create, update, delete) — valores encriptados, nunca expuestos |
| **Deploy** | `website_deploy` (sitios estáticos) |
| **Tareas** | `todowrite`, `task_query`, `task_output`, `task_stop` |
| **Coordinación** | `skill` (cargar SKILL.md), `mavis` CLI (agents, sessions) |

## 1.3 Lo que NO tengo (por diseño)

- ❌ Acceso a internet desde "mi casa" (necesito que el destino sea público o que vos me des acceso)
- ❌ Credenciales guardadas entre sesiones (cada sesión arranca limpia, salvo secrets que guardes explícitamente)
- ❌ Push automático a tus repos sin tu token
- ❌ Capacidad de abrir puertos en el sandbox para ingreso
- ❌ Acceso root ilimitado (estoy en un container)
- ❌ GPU (solo CPU)

---

# 2. Arquitectura de red y seguridad

## 2.1 Flujo de una conexión típica

```
┌──────────────────┐
│ Mavis (sandbox)  │
│ 192.168.x.x      │
│ egress:permitido │
└────────┬─────────┘
         │ HTTPS / SSH / gRPC / API call
         ▼
┌──────────────────┐         ┌──────────────────┐
│ API Gateway      │◄────────┤ Tus credenciales │
│ (servicio X)     │         │ (secret storage) │
└──────────────────┘         └──────────────────┘
         │
         ▼
┌──────────────────┐
│ Backend del      │
│ servicio         │
└──────────────────┘
```

## 2.2 Capas de seguridad

1. **Transport:** TLS 1.3 obligatorio en HTTPS
2. **Auth:** Bearer tokens, API keys, OAuth, SSH keys
3. **Secret storage:** valores encriptados con KMS, nunca aparecen en mis outputs
4. **Least privilege:** te pido solo el scope mínimo necesario
5. **Audit:** cada tool call queda logueado

## 2.3 Lo que nunca hago

- Nunca imprimo el valor de un secret en mi respuesta
- Nunca commiteo credenciales a git
- Nunca las envío a servicios de terceros sin tu OK
- Nunca las guardo en archivos sin `chmod 600`

---

# 3. Protocolos y métodos de conexión

## 3.1 Protocolos que uso

| Protocolo | Puerto típico | Uso |
|---|---|---|
| **HTTPS** | 443 | APIs REST, webhooks, GraphQL, gRPC-web |
| **SSH** | 22 | Acceso a VPS, Git over SSH |
| **Git+SSH** | 22 | Push/pull a GitHub, GitLab, Gitea |
| **Git+HTTPS** | 443 | Clone de repos públicos/privados con token |
| **PostgreSQL** | 5432 | DBs (con SSL) |
| **MySQL** | 3306 | DBs |
| **Redis** | 6379 | Cache, streams |
| **MongoDB** | 27017 | DBs NoSQL |
| **gRPC** | variable | Servicios modernos (Temporal, Hatchet) |
| **WebSocket** | 443/80 | Real-time (Swiggy, Hotstar pattern) |
| **SMTP/IMAP** | 587/993 | Email |
| **DNS over HTTPS** | 443 | Resolución de dominios |

## 3.2 Métodos de auth que uso

| Método | Ejemplo |
|---|---|
| **Bearer token** | `Authorization: Bearer ghp_xxxx` |
| **API key header** | `X-API-Key: sk-xxxx` |
| **Basic auth** | `user:password` (base64) |
| **OAuth 2.0** | Client credentials, authorization code |
| **JWT** | `Authorization: Bearer eyJ...` |
| **SSH key** | `ssh -i ~/.ssh/id_rsa user@host` |
| **Service account JSON** | GCP, GCP service account |
| **mTLS** | Cert + key (raro, pero soportado) |

## 3.3 Patrones de uso

```bash
# Patrón 1: curl con header
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/v1/resource

# Patrón 2: SSH
ssh -i /tmp/key -o StrictHostKeyChecking=no user@host "command"

# Patrón 3: git push
git push https://x-access-token:$TOKEN@github.com/user/repo.git main

# Patrón 4: psql con SSL
psql "postgresql://user:pass@host:5432/db?sslmode=require"

# Patrón 5: Python con SDK
from github import Github
g = Github(os.environ['GH_TOKEN'])
```

---

# 4. Servicios y plataformas soportadas

## Resumen de servicios a los que me puedo conectar

| Categoría | Servicios |
|---|---|
| **Cloud VPS** | Contabo, Hetzner, DigitalOcean, Linode, Vultr, OVH, Scaleway |
| **Cloud hyperscaler** | AWS, GCP, Azure, Oracle Cloud, IBM Cloud |
| **PaaS** | Vercel, Netlify, Railway, Render, Fly.io, Heroku, Cloudflare Pages/Workers |
| **Repos Git** | GitHub, GitLab, Bitbucket, Gitea, self-hosted |
| **CDN/Edge** | Cloudflare, Fastly, Akamai, BunnyCDN, Vercel Edge |
| **Databases** | Postgres, MySQL, MongoDB, Redis, ClickHouse, Supabase, Neon, PlanetScale, Turso |
| **Storage** | S3, R2, GCS, Azure Blob, MinIO, Backblaze B2, Wasabi |
| **AI/LLM** | OpenAI, Anthropic, Google AI, Mistral, Cohere, Groq, Together, Ollama, llama.cpp, vLLM, local models |
| **Monitoring** | Grafana, Prometheus, Datadog, Sentry, New Relic, Logflare, Better Stack |
| **Comunicación** | Slack, Discord, Telegram, Email (SMTP), Twilio, webhooks genéricos |
| **Payment** | Stripe, PayPal, Razorpay, Mercado Pago, Lemon Squeezy, Paddle |
| **Auth** | Auth0, Clerk, Supabase Auth, Firebase Auth, Keycloak, custom JWT |
| **Workflow engines** | Temporal, Hatchet, Conductor, Airflow, Prefect, Dagster, Inngest, Trigger.dev |
| **Containers** | Docker Hub, GHCR, ECR, GCR, self-hosted registries |
| **K8s** | EKS, GKE, AKS, DOKS, k3s, microk8s, K0s, Rancher |
| **Mensajería** | Kafka, RabbitMQ, NATS, Redis Streams, Pub/Sub, SQS, SNS |
| **Email** | SendGrid, Resend, Postmark, Mailgun, SES, SMTP genérico |
| **Búsqueda** | Elasticsearch, Algolia, Meilisearch, Typesense |
| **Ticketing** | Jira, Linear, GitHub Issues, Notion DB |
| **Docs** | Notion, Confluence, Google Docs, Markdown en git |

---

# 5. Tabla completa de credenciales necesarias

## 5.1 Cloud VPS / IaaS

| Servicio | Credenciales | Notas |
|---|---|---|
| **Contabo** | SSH private key, IP, user (root), port | Key-based, no password por default |
| **Hetzner** | API token (`hcloud`), SSH key | hcloud CLI para crear/destroy servers |
| **DigitalOcean** | `DO_API_TOKEN` (PAT) + SSH key (UUID) | doctl CLI |
| **Linode** | `LINODE_TOKEN` + SSH key | linode-cli |
| **Vultr** | `VULTR_API_KEY` + SSH key | vultr-cli |
| **OVH** | `OVH_APPLICATION_KEY`, `OVH_APPLICATION_SECRET`, `OVH_CONSUMER_KEY`, `OVH_ENDPOINT` | ovh-cli (3 keys) |
| **Scaleway** | `SCW_ACCESS_KEY`, `SCW_SECRET_KEY`, `SCW_DEFAULT_ORGANIZATION_ID`, `SCW_DEFAULT_PROJECT_ID` | scw CLI |

## 5.2 Cloud hyperscaler

| Servicio | Credenciales |
|---|---|
| **AWS** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, opcional `AWS_SESSION_TOKEN` + región |
| **GCP** | Service Account JSON (path o contenido) + `GOOGLE_APPLICATION_CREDENTIALS` |
| **Azure** | `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` o service principal JSON |
| **Oracle Cloud** | `OCI_USER_OCID`, `OCI_TENANCY_OCID`, `OCI_COMPARTMENT_OCID`, `OCI_API_KEY_FINGERPRINT`, private key |
| **IBM Cloud** | `IBM_CLOUD_API_KEY` |

## 5.3 PaaS

| Servicio | Credenciales |
|---|---|
| **Vercel** | `VERCEL_TOKEN` (account token o team token) |
| **Netlify** | `NETLIFY_AUTH_TOKEN` |
| **Railway** | `RAILWAY_TOKEN` (account token) |
| **Render** | `RENDER_API_KEY` |
| **Fly.io** | `FLY_API_TOKEN` |
| **Heroku** | `HEROKU_API_KEY` + `HEROKU_API_EMAIL` |
| **Cloudflare Pages** | `CLOUDFLARE_API_TOKEN` (con permiso Pages:Edit) |
| **Cloudflare Workers** | `CLOUDFLARE_API_TOKEN` (con permiso Workers:Edit) |

## 5.4 Repos Git

| Servicio | Credenciales |
|---|---|
| **GitHub** | `GH_TOKEN` (PAT con scopes: `repo`, `workflow`, `admin:org`, etc.) o SSH key |
| **GitLab** | `GITLAB_TOKEN` (PAT) o SSH key |
| **Bitbucket** | `BITBUCKET_USER` + `BITBUCKET_APP_PASSWORD` |
| **Gitea** | `GITEA_TOKEN` o user+pass |

## 5.5 CDN/Edge

| Servicio | Credenciales |
|---|---|
| **Cloudflare** | `CLOUDFLARE_API_TOKEN` (con permisos específicos) + `CLOUDFLARE_ACCOUNT_ID` |
| **Fastly** | `FASTLY_API_TOKEN` |
| **Akamai** | `AKAMAI_CLIENT_TOKEN`, `AKAMAI_CLIENT_SECRET`, `AKAMAI_ACCESS_TOKEN`, `AKAMAI_HOST` |
| **BunnyCDN** | `BUNNY_API_KEY` |

## 5.6 Databases

| Servicio | Credenciales |
|---|---|
| **Postgres (self-host)** | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` |
| **Postgres (Neon)** | `DATABASE_URL` (postgres://...sslmode=require) |
| **Postgres (Supabase)** | `DATABASE_URL` + service role key |
| **MySQL** | `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` |
| **PlanetScale** | `DATABASE_URL` con `mysql://...ssl=true` |
| **MongoDB Atlas** | `MONGODB_URI` (mongodb+srv://...) |
| **Redis (Upstash)** | `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` (HTTP) o `REDIS_URL` (TCP) |
| **ClickHouse Cloud** | `CLICKHOUSE_URL`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD` |
| **Turso** | `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN` |

## 5.7 Storage

| Servicio | Credenciales |
|---|---|
| **AWS S3** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` + región + bucket |
| **Cloudflare R2** | `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` |
| **Backblaze B2** | `B2_APPLICATION_KEY_ID`, `B2_APPLICATION_KEY` |
| **GCS** | Service account JSON |
| **Azure Blob** | `AZURE_STORAGE_ACCOUNT`, `AZURE_STORAGE_KEY` o SAS token |
| **MinIO** | `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` |
| **Wasabi** | `WASABI_ACCESS_KEY`, `WASABI_SECRET_KEY` + endpoint |

## 5.8 AI/LLM

| Servicio | Credenciales |
|---|---|
| **OpenAI** | `OPENAI_API_KEY` |
| **Anthropic** | `ANTHROPIC_API_KEY` |
| **Google AI (Gemini)** | `GOOGLE_API_KEY` o service account |
| **Mistral** | `MISTRAL_API_KEY` |
| **Cohere** | `COHERE_API_KEY` |
| **Groq** | `GROQ_API_KEY` |
| **Together** | `TOGETHER_API_KEY` |
| **Replicate** | `REPLICATE_API_TOKEN` |
| **HuggingFace** | `HF_TOKEN` |
| **OpenRouter** | `OPENROUTER_API_KEY` |
| **Ollama** (local) | solo URL (`OLLAMA_HOST`) |

## 5.9 Monitoring

| Servicio | Credenciales |
|---|---|
| **Grafana Cloud** | `GRAFANA_API_KEY` + endpoint |
| **Datadog** | `DD_API_KEY`, `DD_APP_KEY` |
| **Sentry** | `SENTRY_AUTH_TOKEN` + `SENTRY_DSN` |
| **Better Stack** | `BETTER_STACK_TOKEN` |
| **Logflare** | `LOGFLARE_API_KEY` |
| **Prometheus** | `PROMETHEUS_URL` + basic auth (si habilitado) |

## 5.10 Comunicación

| Servicio | Credenciales |
|---|---|
| **Slack** | `SLACK_BOT_TOKEN` (xoxb-...) + opcional `SLACK_SIGNING_SECRET` |
| **Discord** | `DISCORD_BOT_TOKEN` + `DISCORD_GUILD_ID` |
| **Telegram** | `TELEGRAM_BOT_TOKEN` (de BotFather) + chat_id |
| **Twilio** | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` |
| **SendGrid** | `SENDGRID_API_KEY` |
| **Resend** | `RESEND_API_KEY` |
| **Mailgun** | `MAILGUN_API_KEY`, `MAILGUN_DOMAIN` |
| **SES (AWS)** | via creds AWS |
| **SMTP genérico** | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` |
| **Webhook genérico** | solo URL |

## 5.11 Payment

| Servicio | Credenciales |
|---|---|
| **Stripe** | `STRIPE_SECRET_KEY` (sk_live/sk_test) + opcional `STRIPE_WEBHOOK_SECRET` |
| **PayPal** | `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET` |
| **Razorpay** | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` |
| **Mercado Pago** | `MP_ACCESS_TOKEN` |
| **Lemon Squeezy** | `LEMONSQUEEZY_API_KEY` |
| **Paddle** | `PADDLE_API_KEY` |

## 5.12 Auth

| Servicio | Credenciales |
|---|---|
| **Auth0** | `AUTH0_DOMAIN`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET` |
| **Clerk** | `CLERK_SECRET_KEY` + `CLERK_PUBLISHABLE_KEY` |
| **Supabase Auth** | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |
| **Firebase Auth** | service account JSON |
| **Keycloak** | URL + admin user/pass o service account |

## 5.13 Workflow engines

| Servicio | Credenciales |
|---|---|
| **Temporal Cloud** | `TEMPORAL_ADDRESS`, `TEMPORAL_TLS_CERT`, `TEMPORAL_TLS_KEY` |
| **Temporal self-host** | `TEMPORAL_ADDRESS` (host:port) |
| **Hatchet** | `HATCHET_API_URL`, `HATCHET_API_TOKEN` |
| **Inngest** | `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY` |
| **Trigger.dev** | `TRIGGER_API_KEY` |
| **Airflow** | `AIRFLOW_URL` + basic auth |

## 5.14 Containers / K8s

| Servicio | Credenciales |
|---|---|
| **Docker Hub** | `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` |
| **GHCR** | `GHCR_TOKEN` (PAT con `read:packages`) |
| **ECR** | via AWS creds |
| **GCR** | via GCP creds |
| **ACR** | via Azure creds |
| **Kubernetes cluster** | `KUBECONFIG` (path o contenido base64) |

## 5.15 Mensajería

| Servicio | Credenciales |
|---|---|
| **Confluent Kafka** | `KAFKA_BROKERS`, `KAFKA_API_KEY`, `KAFKA_API_SECRET` |
| **CloudAMQP (RabbitMQ)** | `RABBITMQ_URL` (amqp://...) |
| **Upstash Kafka** | `KAFKA_REST_URL`, `KAFKA_REST_TOKEN` |
| **NATS** | `NATS_URL` + optional user/pass |
| **AWS SQS** | via AWS creds |
| **GCP Pub/Sub** | via GCP service account |

## 5.16 Búsqueda

| Servicio | Credenciales |
|---|---|
| **Elasticsearch** | `ELASTICSEARCH_URL` + `ELASTICSEARCH_USER`, `ELASTICSEARCH_PASSWORD` |
| **Algolia** | `ALGOLIA_APP_ID`, `ALGOLIA_API_KEY` |
| **Meilisearch** | `MEILI_URL`, `MEILI_MASTER_KEY` |
| **Typesense** | `TYPESENSE_HOST`, `TYPESENSE_API_KEY` |

## 5.17 Ticketing / Docs

| Servicio | Credenciales |
|---|---|
| **Jira** | `JIRA_HOST`, `JIRA_EMAIL`, `JIRA_API_TOKEN` |
| **Linear** | `LINEAR_API_KEY` |
| **Notion** | `NOTION_TOKEN` (internal integration) |
| **Confluence** | `CONFLUENCE_HOST`, `CONFLUENCE_EMAIL`, `CONFLUENCE_API_TOKEN` |
| **Google Docs** | service account JSON + domain delegation |

---

# 6. Cómo almaceno y uso los secretos

## 6.1 Función `secret`

```bash
# Listar nombres (nunca los valores)
secret list

# Crear
secret create --name=GITHUB_TOKEN --value=ghp_xxxx --description="GitHub PAT for Max repo"

# Actualizar
secret update --name=GITHUB_TOKEN --value=ghp_yyyy

# Borrar
secret delete --name=GITHUB_TOKEN
```

## 6.2 Características del secret storage

- **Encriptación:** AES-256 con KMS-managed keys
- **Acceso:** solo Mavis puede leerlos, vos no ves los valores (solo los nombres)
- **Scope:** se mantienen entre sesiones hasta que vos los borres
- **Audit:** cada lectura queda logueada
- **Inyección:** aparecen como env vars en mis shells (ej: `$GITHUB_TOKEN`)

## 6.3 Patrón de uso en mis scripts

```bash
# Patrón: leer secret y usar inmediatamente
export GH_TOKEN=$(secret_get GITHUB_TOKEN)
git push https://x-access-token:$GH_TOKEN@github.com/user/repo.git

# Patrón: usar SDK que lee de env
from openai import OpenAI
client = OpenAI()  # lee OPENAI_API_KEY del env
```

## 6.4 Lo que jamás hago

- ❌ `echo $GITHUB_TOKEN` en output
- ❌ `cat` de un archivo que contenga secrets
- ❌ Commits con secrets
- ❌ Imprimir el valor en mis respuestas
- ❌ Compartir el valor con un servicio de terceros sin tu OK explícito

---

# 7. Conexión a tu VPS Contabo

## 7.1 Credenciales necesarias

```bash
# Crear estos secrets (vos, desde tu lado)
secret create --name=CONTABO_SSH_KEY --value="$(cat ~/.ssh/contabo_key)" --description="SSH private key para Contabo"
secret create --name=CONTABO_HOST --value="95.111.232.89" --description="IP pública Contabo"
secret create --name=CONTABO_USER --value="root" --description="Usuario SSH"
```

## 7.2 Patrones de uso

```bash
# Leer secrets
export SSH_KEY=$(secret_get CONTABO_SSH_KEY)
export HOST=$(secret_get CONTABO_HOST)
export USER=$(secret_get CONTABO_USER)

# Guardar key temporal con permisos correctos
mkdir -p ~/.ssh
echo "$SSH_KEY" > ~/.ssh/contabo_key
chmod 600 ~/.ssh/contabo_key

# SSH command
ssh -i ~/.ssh/contabo_key -o StrictHostKeyChecking=no $USER@$HOST "docker ps"

# SCP
scp -i ~/.ssh/contabo_key /workspace/script.sh $USER@$HOST:/opt/mavis/

# Rsync
rsync -avz -e "ssh -i ~/.ssh/contabo_key" /workspace/ $USER@$HOST:/opt/mavis/workspace/

# Sesión interactiva (no recomendada, mejor nohup)
ssh -i ~/.ssh/contabo_key $USER@$HOST << 'EOF'
  cd /opt/mavis
  docker compose pull
  docker compose up -d
  docker compose logs -f --tail=50
EOF
```

## 7.3 Tareas típicas que puedo hacer

- Levantar / parar / reiniciar Docker compose
- Ver logs (`docker logs`, `journalctl`)
- Inspeccionar Postgres / Redis / MinIO
- Deployar código (`git pull` + restart)
- Editar archivos de config (`/opt/mavis/.env`, `docker-compose.yml`)
- Backup del workspace (`tar | rclone to S3`)
- Chaos test (matar contenedores)

---

# 8. Conexión a GitHub

## 8.1 Credenciales

```bash
secret create --name=GH_TOKEN --value="ghp_xxxxxxxxxxxxxxxxxxxx" --description="GitHub PAT"
# Scopes necesarios: repo, workflow, admin:org (opcional), read:packages, write:packages
```

Opcionalmente SSH key (recomendado para push frecuente):

```bash
# Generar
ssh-keygen -t ed25519 -C "mavis@max.dev" -f /tmp/gh_key
# Agregar pub key a GitHub > Settings > SSH and GPG keys
# Crear secret con la private key
secret create --name=GH_SSH_KEY --value="$(cat /tmp/gh_key)" --description="SSH key GitHub"
```

## 8.2 Patrones de uso

```bash
# Clonar repo público
git clone https://github.com/user/repo.git

# Clonar repo privado con token
git clone https://x-access-token:$GH_TOKEN@github.com/user/repo.git

# Push
git push https://x-access-token:$GH_TOKEN@github.com/user/repo.git main

# Con SSH
export GH_SSH_KEY=$(secret_get GH_SSH_KEY)
mkdir -p ~/.ssh && echo "$GH_SSH_KEY" > ~/.ssh/gh_key && chmod 600 ~/.ssh/gh_key
git clone git@github.com:user/repo.git

# GitHub API
curl -H "Authorization: Bearer $GH_TOKEN" https://api.github.com/user/repos

# Crear issue
curl -X POST -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/user/repo/issues \
  -d '{"title":"Bug","body":"..."}'

# GitHub CLI
gh auth login --with-token <<< "$GH_TOKEN"
gh issue list
gh pr create --title "X" --body "Y"
```

## 8.3 GitHub Actions / Workflows

Puedo leer/escribir `.github/workflows/*.yml` y disparar runs via API.

---

# 9. Conexión a Cloudflare

## 9.1 Credenciales

```bash
secret create --name=CF_API_TOKEN --value="your-api-token" --description="Cloudflare API token"
secret create --name=CF_ACCOUNT_ID --value="your-account-id" --description="Cloudflare Account ID"
# El token debe tener los scopes necesarios:
# - Zone:DNS:Edit (para DNS)
# - Zone:Zone:Read
# - Account:Workers Scripts:Edit (para Workers)
# - Account:Pages:Edit (para Pages)
# - Account:R2:Edit (para R2)
```

## 9.2 Patrones de uso

```bash
# CLI: wrangler
npm install -g wrangler
export CLOUDFLARE_API_TOKEN=$(secret_get CF_API_TOKEN)
export CLOUDFLARE_ACCOUNT_ID=$(secret_get CF_ACCOUNT_ID)

# Login
wrangler login  # o usa env vars

# Listar Workers
wrangler list

# Deploy Worker
wrangler deploy

# DNS API
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"www","content":"1.2.3.4"}'

# Crear DNS record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"api","content":"95.111.232.89"}'

# R2 upload
wrangler r2 object put my-bucket/file.txt --file ./file.txt

# Pages
wrangler pages deploy ./dist --project-name=my-site
```

## 9.3 Servicios Cloudflare que puedo usar

- DNS (records, zones, load balancing)
- Workers (serverless functions)
- Pages (static sites)
- R2 (object storage)
- KV (key-value)
- D1 (SQLite)
- Durable Objects
- Queues
- Stream (video)
- Images
- Access (zero-trust)
- Tunnel (Cloudflare → tu infra)
- Email Workers
- WAF / Rate limiting
- Analytics

---

# 10. Conexión a Vercel

## 10.1 Credenciales

```bash
secret create --name=VERCEL_TOKEN --value="your-token" --description="Vercel account token"
# Crear en: https://vercel.com/account/tokens
```

## 10.2 Patrones de uso

```bash
# CLI
npm install -g vercel
export VERCEL_TOKEN=$(secret_get VERCEL_TOKEN)

# Login
vercel login --token $VERCEL_TOKEN

# Deploy
cd /workspace/mi-proyecto
vercel deploy --prod --yes --token $VERCEL_TOKEN

# Env vars
vercel env add MY_VAR production --token $VERCEL_TOKEN

# Listar deployments
vercel ls --token $VERCEL_TOKEN

# Logs
vercel logs <deployment-url> --token $VERCEL_TOKEN

# API
curl -H "Authorization: Bearer $VERCEL_TOKEN" https://api.vercel.com/v6/deployments
```

---

# 11. Conexión a otros providers (DO, Hetzner, AWS, Railway, Render)

## 11.1 DigitalOcean

```bash
secret create --name=DO_API_TOKEN --value="dop_v1_xxxxx" --description="DO PAT"
# CLI
export DO_API_TOKEN=$(secret_get DO_API_TOKEN)
doctl auth init -t $DO_API_TOKEN
doctl compute droplet create my-vps --size s-1vcpu-1gb --image ubuntu-22-04 --region nyc1
```

## 11.2 Hetzner

```bash
secret create --name=HCLOUD_TOKEN --value="your-token"
export HCLOUD_TOKEN=$(secret_get HCLOUD_TOKEN)
hcloud server create --name mavis-prod --type cx22 --image ubuntu-22.04 --location nbg1
```

## 11.3 AWS

```bash
secret create --name=AWS_ACCESS_KEY_ID --value="AKIA..."
secret create --name=AWS_SECRET_ACCESS_KEY --value="..."
secret create --name=AWS_DEFAULT_REGION --value="us-east-1"

export AWS_ACCESS_KEY_ID=$(secret_get AWS_ACCESS_KEY_ID)
export AWS_SECRET_ACCESS_KEY=$(secret_get AWS_SECRET_ACCESS_KEY)
export AWS_DEFAULT_REGION=$(secret_get AWS_DEFAULT_REGION)

aws s3 ls
aws ec2 describe-instances
```

## 11.4 Railway

```bash
secret create --name=RAILWAY_TOKEN --value="your-token"
npm install -g @railway/cli
export RAILWAY_TOKEN=$(secret_get RAILWAY_TOKEN)
railway login --token $RAILWAY_TOKEN
railway up
```

## 11.5 Render

```bash
secret create --name=RENDER_API_KEY --value="rnd_xxxx"
# API
curl -H "Authorization: Bearer $RENDER_API_KEY" https://api.render.com/v1/services
```

## 11.6 Fly.io

```bash
secret create --name=FLY_API_TOKEN --value="Fo1_xxxx"
export FLY_API_TOKEN=$(secret_get FLY_API_TOKEN)
flyctl auth login --access-token $FLY_API_TOKEN
fly launch
fly deploy
```

---

# 12. Conexión a bases de datos

## 12.1 Postgres

```bash
# Self-host o managed
secret create --name=DATABASE_URL --value="postgresql://user:pass@host:5432/db?sslmode=require"
export DATABASE_URL=$(secret_get DATABASE_URL)
psql $DATABASE_URL

# Con Python
pip install psycopg2-binary asyncpg
python -c "import psycopg2; conn=psycopg2.connect('$DATABASE_URL')"
```

## 12.2 Redis

```bash
secret create --name=REDIS_URL --value="redis://default:pass@host:6379"
export REDIS_URL=$(secret_get REDIS_URL)
redis-cli -u $REDIS_URL ping
```

## 12.3 MongoDB

```bash
secret create --name=MONGODB_URI --value="mongodb+srv://user:pass@cluster.x.mongodb.net/db"
```

## 12.4 Supabase

```bash
secret create --name=SUPABASE_URL --value="https://xxx.supabase.co"
secret create --name=SUPABASE_SERVICE_ROLE_KEY --value="eyJ..."
secret create --name=SUPABASE_DB_URL --value="postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres"
```

## 12.5 Neon (Postgres serverless)

```bash
secret create --name=NEON_DATABASE_URL --value="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/db?sslmode=require"
```

---

# 13. Conexión a servicios de AI/LLM

## 13.1 OpenAI

```bash
secret create --name=OPENAI_API_KEY --value="sk-..."
export OPENAI_API_KEY=$(secret_get OPENAI_API_KEY)

# CLI
openai api chat.completions.create -m gpt-4o -g user "Hello"

# Python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(model="gpt-4o", messages=[...])
```

## 13.2 Anthropic

```bash
secret create --name=ANTHROPIC_API_KEY --value="sk-ant-..."
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(model="claude-opus-4", max_tokens=1024, messages=[...])
```

## 13.3 Google AI

```bash
secret create --name=GOOGLE_API_KEY --value="..."
pip install google-generativeai
```

## 13.4 OpenRouter (multi-provider)

```bash
secret create --name=OPENROUTER_API_KEY --value="sk-or-..."
# Accede a GPT-4, Claude, Gemini, Llama, etc. con una sola key
```

## 13.5 Local models (Ollama, vLLM, llama.cpp)

```bash
secret create --name=OLLAMA_HOST --value="http://100.64.0.5:11434"
# o SSH tunnel al VPS donde corre Ollama
ssh -L 11434:localhost:11434 user@vps
```

---

# 14. Conexión a storage (S3, R2, MinIO, Backblaze)

## 14.1 S3 / R2 / MinIO (mismo protocolo)

```bash
# AWS S3
secret create --name=AWS_ACCESS_KEY_ID --value="..."
secret create --name=AWS_SECRET_ACCESS_KEY --value="..."

# R2
secret create --name=R2_ACCESS_KEY_ID --value="..."
secret create --name=R2_SECRET_ACCESS_KEY --value="..."
secret create --name=R2_ENDPOINT --value="https://<account_id>.r2.cloudflarestorage.com"

# MinIO
secret create --name=MINIO_ENDPOINT --value="https://minio.example.com"
secret create --name=MINIO_ACCESS_KEY --value="..."
secret create --name=MINIO_SECRET_KEY --value="..."

# Uso con aws-cli
export AWS_ACCESS_KEY_ID=$(secret_get AWS_ACCESS_KEY_ID)
export AWS_SECRET_ACCESS_KEY=$(secret_get AWS_SECRET_ACCESS_KEY)
aws s3 ls s3://my-bucket/ --endpoint-url $(secret_get R2_ENDPOINT)

# Upload
aws s3 cp /workspace/file.txt s3://my-bucket/ --endpoint-url ...

# Sync
aws s3 sync /workspace s3://my-bucket/backups/ --endpoint-url ...
```

## 14.2 Backblaze B2

```bash
secret create --name=B2_KEY_ID --value="..."
secret create --name=B2_APP_KEY --value="..."
```

---

# 15. Conexión a monitoreo y observabilidad

## 15.1 Grafana / Prometheus

```bash
secret create --name=GRAFANA_URL --value="https://grafana.example.com"
secret create --name=GRAFANA_API_KEY --value="..."
export GRAFANA_API_KEY=$(secret_get GRAFANA_API_KEY)

# Crear dashboard
curl -X POST -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json $(secret_get GRAFANA_URL)/api/dashboards/db
```

## 15.2 Sentry

```bash
secret create --name=SENTRY_DSN --value="https://xxx@sentry.io/123"
secret create --name=SENTRY_AUTH_TOKEN --value="..."
```

## 15.3 Datadog

```bash
secret create --name=DD_API_KEY --value="..."
secret create --name=DD_APP_KEY --value="..."
```

---

# 16. Conexión a comunicación (Slack, Discord, email, webhooks)

## 16.1 Slack

```bash
secret create --name=SLACK_BOT_TOKEN --value="xoxb-..."
# Crear app en: https://api.slack.com/apps

curl -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-type: application/json" \
  --data '{"channel":"#general","text":"Hello from Mavis"}' \
  https://slack.com/api/chat.postMessage
```

## 16.2 Discord

```bash
secret create --name=DISCORD_BOT_TOKEN --value="..."
secret create --name=DISCORD_CHANNEL_ID --value="..."

curl -X POST -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"Hola\"}" \
  https://discord.com/api/v10/channels/$DISCORD_CHANNEL_ID/messages
```

## 16.3 Telegram

```bash
secret create --name=TELEGRAM_BOT_TOKEN --value="..."
secret create --name=TELEGRAM_CHAT_ID --value="..."

curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$TELEGRAM_CHAT_ID&text=Hola"
```

## 16.4 Email (SMTP / Resend / SES)

```bash
# SMTP
secret create --name=SMTP_HOST --value="smtp.gmail.com"
secret create --name=SMTP_PORT --value="587"
secret create --name=SMTP_USER --value="..."
secret create --name=SMTP_PASSWORD --value="..."

# Resend
secret create --name=RESEND_API_KEY --value="re_..."
curl -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -d '{"from":"...","to":"...","subject":"...","html":"..."}'

# SES (vía AWS creds)
aws ses send-email --from ... --to ...
```

## 16.5 Webhooks genéricos

```bash
# Solo URL, no necesita auth
curl -X POST https://hooks.example.com/abc \
  -H "Content-Type: application/json" \
  -d '{"event":"deploy","status":"success"}'
```

---

# 17. Conexión a payment (Stripe, PayPal, Razorpay)

## 17.1 Stripe

```bash
secret create --name=STRIPE_SECRET_KEY --value="sk_live_..." # o sk_test_
export STRIPE_SECRET_KEY=$(secret_get STRIPE_SECRET_KEY)

stripe customers list
stripe charges list --limit 10
stripe payment_intents create --amount 1000 --currency usd
```

## 17.2 PayPal

```bash
secret create --name=PAYPAL_CLIENT_ID --value="..."
secret create --name=PAYPAL_CLIENT_SECRET --value="..."
```

## 17.3 Razorpay

```bash
secret create --name=RAZORPAY_KEY_ID --value="rzp_live_..."
secret create --name=RAZORPAY_KEY_SECRET --value="..."
```

---

# 18. Conexión a auth (Auth0, Clerk, Supabase Auth)

## 18.1 Auth0

```bash
secret create --name=AUTH0_DOMAIN --value="xxx.auth0.com"
secret create --name=AUTH0_CLIENT_ID --value="..."
secret create --name=AUTH0_CLIENT_SECRET --value="..."
# API
curl -H "Authorization: Bearer $(secret_get AUTH0_CLIENT_SECRET)" \
  "https://$(secret_get AUTH0_DOMAIN)/api/v2/users"
```

## 18.2 Clerk

```bash
secret create --name=CLERK_SECRET_KEY --value="sk_test_..."
secret create --name=CLERK_PUBLISHABLE_KEY --value="pk_test_..."
```

---

# 19. Sobre MCP (Model Context Protocol)

## 19.1 ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo abierto (estandarizado por Anthropic en 2024) que define cómo un agente LLM se conecta a "tools" externas de forma estandarizada. Es como un USB-C para tools.

## 19.2 ¿Yo (Mavis) uso MCP?

**Depende del entorno donde corro.** En la implementación actual:
- **No uso MCP servers externos** por default
- **Sí uso un sistema propio de tools** que cumple una función similar (definir tools como funciones estructuradas que el LLM puede llamar)
- **Sí puedo conectarme a MCP servers** si vos me das el comando para arrancarlos

## 19.3 MCP servers populares que podría usar

| MCP server | Qué hace |
|---|---|
| **mcp-server-github** | Lee/escribe issues, PRs, code en GitHub |
| **mcp-server-gitlab** | Igual para GitLab |
| **mcp-server-postgres** | Query a Postgres (read-only o read-write) |
| **mcp-server-redis** | GET/SET, streams, pub/sub |
| **mcp-server-puppeteer** | Browser automation |
| **mcp-server-filesystem** | Lee/escribe archivos con permisos estrictos |
| **mcp-server-slack** | Lee/envía mensajes Slack |
| **mcp-server-docker** | Controla Docker daemon |
| **mcp-server-kubernetes** | K8s cluster admin |
| **mcp-server-aws** | SDK completo de AWS via MCP |
| **mcp-server-stripe** | Stripe API |
| **mcp-server-notion** | Notion DB/pages |
| **mcp-server-linear** | Linear issues |
| **mcp-server-sentry** | Sentry issues/projects |
| **mcp-cloudflare** | Cloudflare completo |

## 19.4 Cómo funcionan los MCP servers

```json
// Configuración típica (claude_desktop_config.json o similar)
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgresql://..."
      }
    }
  }
}
```

## 19.5 Diferencia entre MCP y mis tools nativas

| Aspecto | MCP | Mis tools nativas |
|---|---|---|
| **Estandarización** | Protocolo abierto, mismo formato en cualquier agente | Propietario del vendor |
| **Ecosistema** | Muchos servers de la comunidad | Lo que el vendor provee |
| **Performance** | Pequeño overhead (JSON-RPC) | Directo, sin overhead |
| **Setup** | Requiere config + run server | Ya integrado |
| **Flexibilidad** | Cualquiera puede escribir un server | Limitado al vendor |

## 19.6 Mi recomendación

Para tu caso (VPS Contabo + nct-hub), **no necesitás MCP** al principio. Mis tools nativas + `bash` para todo lo demás es suficiente. Cuando escales, podés considerar:
- MCP server filesystem (permisos granulares)
- MCP server postgres (queries estructuradas)
- MCP server git (operaciones git complejas)

---

# 20. Seguridad y buenas prácticas

## 20.1 Principios

1. **Least privilege:** cada secret tiene solo los permisos necesarios
2. **Rotación:** cambiá las keys cada 90 días
3. **Auditoría:** revisá quién accedió qué y cuándo
4. **No commit:** ningún secret en git
5. **No echo:** nunca imprimir el valor de un secret
6. **TTL:** algunos secrets con expiración automática

## 20.2 Scope mínimo por tarea

| Tarea | Secrets necesarios |
|---|---|
| Push a GitHub | `GH_TOKEN` con `repo` scope solo |
| Deploy a Vercel | `VERCEL_TOKEN` |
| Gestionar DNS en Cloudflare | `CF_API_TOKEN` con `Zone:DNS:Edit` solo |
| Ejecutar SQL en una DB | `DATABASE_URL` con usuario read-only si es posible |
| Deploy en Contabo | `CONTABO_SSH_KEY` con user limitado |
| Enviar emails | `RESEND_API_KEY` (no uses la master key de tu provider) |
| Stripe | `STRIPE_SECRET_KEY` sk_test primero, sk_live solo en prod |

## 20.3 Cómo manejar secretos en tu código

```bash
# MAL: hardcoded
DATABASE_URL="postgresql://user:mypassword@host/db"

# BIEN: env var
DATABASE_URL="${DATABASE_URL}"

# MEJOR: secret manager
export DATABASE_URL=$(secret_get DATABASE_URL)
```

## 20.4 Qué hacer si un secret se compromete

1. **Rotar inmediatamente** (`secret update`)
2. **Revisar logs** para detectar uso indebido
3. **Invalidar el secret anterior** en el provider original
4. **Alertar a stakeholders** si aplica

## 20.5 Compliance

- **GDPR:** no guardo PII innecesario
- **SOC2:** todos los accesos quedan logueados
- **HIPAA:** NO recomendado para datos médicos sin BAA
- **PCI-DSS:** para pagos usá siempre el provider (Stripe, etc.), nunca manejes PAN

---

# 21. Cómo darme credenciales nuevas

## 21.1 Flujo recomendado

```
Vos: "Mavis, necesito que deployes X a Vercel"
Yo: "Perfecto, necesito que crees este secret: 
     secret create --name=VERCEL_TOKEN --value=<token>
     ¿Me lo creás?"
Vos: <ejecutás el comando>
Yo: <uso el secret>
```

## 21.2 Comando para crear un secret (vos, desde tu lado)

```bash
# Sintaxis
secret create --name=NOMBRE --value="VALOR" --description="Qué es y para qué"

# Ejemplo
secret create --name=GITHUB_TOKEN \
  --value="ghp_xxxxxxxxxxxx" \
  --description="GitHub PAT con scope repo, para nct-hub"
```

## 21.3 Reglas para nombrar

- ✅ MAYÚSCULAS_CON_GUIONES_BAJOS
- ✅ Que sea descriptivo (`GITHUB_TOKEN_NCTHUB` no solo `TOKEN`)
- ❌ No incluir el valor en el nombre
- ❌ No compartir nombres entre providers (mejor `GH_TOKEN` y `GL_TOKEN` separados)

## 21.4 Cómo darme acceso SSH a un server nuevo

```bash
# 1. Generar key pair (en mi sandbox)
ssh-keygen -t ed25519 -C "mavis@max.dev" -f /tmp/server_key

# 2. Darte la pub key para que la agregues al server
cat /tmp/server_key.pub

# 3. Vos la agregás:
#    - Contabo: pegar en `~/.ssh/authorized_keys`
#    - AWS EC2: al crear instance, pasar como key pair
#    - DigitalOcean: agregar via panel

# 4. Crear secret con la private key
secret create --name=CONTABO_SSH_KEY --value="$(cat /tmp/server_key)"
```

---

# 22. Límites y restricciones

## 22.1 Límites duros

| Límite | Valor | Notas |
|---|---|---|
| **Timeout bash** | 600s default (configurable) | Comandos largos → `run_in_background: true` |
| **Tamaño de output** | ~100KB por respuesta | Outputs grandes → guardar a archivo |
| **Concurrent tools** | Sin límite duro | Pero el runtime puede throttlear |
| **Network egress** | Ilimitado | Pero algunos providers rate-limitean |
| **Background tasks simultáneos** | Sin límite duro | Cada una consume recursos del sandbox |
| **Storage efímero** | Limitado por disco del sandbox | `/workspace` es persistente dentro de la sesión |
| **Secretos** | Hasta ~100KB por secret | Suficiente para SSH keys, no para binarios |

## 22.2 Lo que no puedo hacer

- ❌ Iniciar conexiones INGRESAS (no soy un server, soy un cliente)
- ❌ Abrir puertos en mi sandbox
- ❌ Correr GUI / desktop apps
- ❌ Hacer acciones destructivas sin tu confirmación explícita
- ❌ Deploy público sin tu OK (sí, te pregunto antes de `website_deploy`)
- ❌ Acceder a recursos que vos no me diste acceso

## 22.3 Confirmaciones que SIEMPRE te pido

Antes de hacer cualquiera de estas, te pregunto:

- Borrar archivos importantes
- `git push` a main / master
- `git push --force`
- Deploy a producción
- Cambios en DNS / producción
- Cobrar / gastar dinero real
- Enviar emails / mensajes a terceros
- Modificar infraestructura crítica

## 22.4 Mejor práctica: el "dry run"

Para acciones riesgosas, primero te muestro QUÉ voy a hacer y vos decís "go":

```bash
# En vez de ejecutar directamente:
rm -rf /opt/mavis/data

# Te muestro:
echo "Voy a borrar /opt/mavis/data con 50GB de Postgres + 20GB Redis + 30GB MinIO.
¿Confirmás? (sí/no)"
```

---

# Apéndice A: Cheat sheet — Secret patterns por provider

```bash
# GitHub
GH_TOKEN=ghp_xxx

# GitLab
GITLAB_TOKEN=glpat-xxx

# Cloudflare
CLOUDFLARE_API_TOKEN=xxx
CLOUDFLARE_ACCOUNT_ID=xxx

# AWS
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Contabo
CONTABO_SSH_KEY="$(cat ~/.ssh/id_rsa)"
CONTABO_HOST=95.111.232.89
CONTABO_USER=root

# Postgres
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Redis
REDIS_URL=redis://default:pass@host:6379

# S3
S3_BUCKET=my-bucket
S3_REGION=us-east-1
S3_ACCESS_KEY=...
S3_SECRET_KEY=...

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

# Apéndice B: Glosario

- **Sandbox:** Entorno aislado donde corro (mi "computadora")
- **Egress:** Tráfico de red SALIENTE de mi sandbox
- **Ingress:** Tráfico de red ENTRANTE a mi sandbox (bloqueado)
- **PAT:** Personal Access Token (tipo de API key)
- **SSH key pair:** Private key (yo) + public key (server) para auth
- **mTLS:** Mutual TLS, ambos lados se autentican con certs
- **Bearer token:** Token que se envía en el header `Authorization: Bearer <token>`
- **Service account:** Identidad de máquina (no humana) con permisos específicos
- **Scope:** Permiso específico que un token tiene
- **Rotation:** Cambiar un secret periódicamente por seguridad
- **MCP:** Model Context Protocol, estándar abierto para tools de LLM
- **TTL:** Time To Live, cuánto vive algo antes de expirar
- **RTO:** Recovery Time Objective
- **RPO:** Recovery Point Objective

---

# FIN DEL DOCUMENTO

*Generado por Mavis. 1 sesión. Cubre 50+ servicios, todos los métodos de conexión, secrets necesarios, y patrones de uso real.*

*Versión 1.0 — listo para usar.*
