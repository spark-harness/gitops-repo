# Lendora dev-1 / sta-1 Runtime

`LEN-136` 将 Lendora runtime 拆为 `dev-1` 和 `sta-1` 两个业务环境，并共享 PostgreSQL、Redis 和 Consul。

## Namespace

| Boundary | Namespace |
|---|---|
| dev business | `lendora-dev-1` |
| sta business | `lendora-sta-1` |
| PostgreSQL | `lendora-shared-postgres` |
| Redis | `lendora-shared-redis` |
| Consul | `lendora-shared-consul` |

## Public Hosts

| Environment | Web | API |
|---|---|---|
| dev-1 | `dev-1-fides.fuzzytails.fun` | `dev-1-api.fuzzytails.fun` |
| sta-1 | `sta-1-fides.fuzzytails.fun` | `sta-1-api.fuzzytails.fun` |

## Consul

Consul address is `consul.lendora-shared-consul.svc.cluster.local:8500`.

KV keys use:

```text
spark/lendora/{env}/{component}/{kind}
```

Service names use:

```text
{env}-{service}
```

Examples:

```text
spark/lendora/dev-1/applicant-api/config
dev-1-applicant-api
sta-1-quote-api
```

## Data Isolation

PostgreSQL uses one shared instance with environment-specific databases and roles.

Redis uses one shared instance with logical DB 1 for `dev-1` and logical DB 2 for `sta-1`.

## Promotion And Sync

`dev-1` is the automatic environment. Image release promotion updates dev overlays and Argo CD syncs automatically.

`sta-1` is the manual environment. Maintainers set digest values in sta overlays and sync Argo CD manually.

## Secret Bootstrap

Secret values are not stored in Git. Keep secret names stable inside each namespace:

```text
postgres-auth
redis-auth
applicant-api-runtime
quote-api-runtime
origination-api-runtime
fides-bff-runtime
ghcr-pull
```

PostgreSQL init jobs run in `lendora-shared-postgres`. Bootstrap `applicant-api-runtime`, `quote-api-runtime`, and `origination-api-runtime` there for database role creation, and bootstrap the same runtime secret names in `lendora-dev-1` / `lendora-sta-1` for service startup.

## Legacy Cleanup

Legacy cleanup has been executed after both environments passed runtime smoke.

Removed:

- old `lendora-sta-*` namespaces and PVCs
- old `clusters/lendora-sta`, `apps/*/overlays/lendora-sta`, and `apps/lendora-sta-dependencies` GitOps state
- old Consul KV keys under `config/<service>/data`
- old bare Consul service registrations without environment prefixes
- old `api.fuzzytails.fun` Lendora route and DNS record

GitHub webhook traffic now uses `github.fuzzytails.fun`; do not reintroduce `api.fuzzytails.fun` for Lendora.
