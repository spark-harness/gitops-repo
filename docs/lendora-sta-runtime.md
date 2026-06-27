# Lendora STA Runtime

`clusters/lendora-sta/` 是 LEN-77 的 runtime GitOps 入口。

它不是什么：它不是 CI namespace，也不是临时手工 apply 的清单集合。

它是什么：Lendora STA 环境的 app-of-apps，按依赖和服务边界拆分独立 namespace，并让 Argo CD 同步每个入口。

## 入口

| 入口 | 说明 |
|---|---|
| `clusters/lendora-sta/` | app-of-apps、namespace、AppProject、Argo CD Application |
| `apps/lendora-sta-dependencies/overlays/sta` | PostgreSQL、Redis、Consul |
| `apps/applicant-api/overlays/lendora-sta` | 内网身份服务 |
| `apps/quote-api/overlays/lendora-sta` | 内网试算服务 |
| `apps/origination-api/overlays/lendora-sta` | 内网申请草稿服务 |
| `apps/fides-bff/overlays/lendora-sta` | 公网 API 边界 |
| `apps/fides/overlays/lendora-sta` | 公网前端 |

## Secret bootstrap

Secret 值不进入 Git。集群 bootstrap 时必须在对应 namespace 创建：

```bash
kubectl -n lendora-sta-postgres create secret generic postgres-auth \
  --from-literal=POSTGRES_USER=applicant \
  --from-literal=POSTGRES_PASSWORD='<redacted>'

kubectl -n lendora-sta-redis create secret generic redis-auth \
  --from-literal=REDIS_PASSWORD='<redacted>'

kubectl -n lendora-sta-applicant-api create secret generic applicant-api-runtime \
  --from-literal=db-password='<redacted>' \
  --from-literal=redis-password='<redacted>' \
  --from-literal=token-secret='<redacted>' \
  --from-literal=otlp-traces-headers='<redacted>'

kubectl -n lendora-sta-postgres create secret generic quote-api-runtime \
  --from-literal=db-password='<redacted>' \
  --from-literal=otlp-traces-headers='<redacted>'

kubectl -n lendora-sta-quote-api create secret generic quote-api-runtime \
  --from-literal=db-password='<redacted>' \
  --from-literal=otlp-traces-headers='<redacted>'

kubectl -n lendora-sta-postgres create secret generic origination-api-runtime \
  --from-literal=db-password='<redacted>' \
  --from-literal=otlp-traces-headers='<redacted>'

kubectl -n lendora-sta-origination-api create secret generic origination-api-runtime \
  --from-literal=db-password='<redacted>' \
  --from-literal=otlp-traces-headers='<redacted>'
```

如果后续采用 ExternalSecret 或 SealedSecret，应替换这些 bootstrap 命令并保留 Secret 名称和 key 兼容性。

`apps/applicant-api/base/consul-config.yaml`、`apps/quote-api/base/consul-config.yaml` 和 `apps/origination-api/base/consul-config.yaml` 只写入 Consul 中的非密 YAML。数据库密码、Redis 密码、token secret 和 OTLP header 仍必须通过对应 runtime Secret 注入。

## Image promotion

三服务 overlay 只接受 digest：

| Service | Overlay | Image name |
|---|---|---|
| applicant-api | `apps/applicant-api/overlays/lendora-sta` | `ghcr.io/spark-harness/applicant-api` |
| quote-api | `apps/quote-api/overlays/lendora-sta` | `ghcr.io/spark-harness/quote-api` |
| origination-api | `apps/origination-api/overlays/lendora-sta` | `ghcr.io/spark-harness/origination-api` |
| fides-bff | `apps/fides-bff/overlays/lendora-sta` | `ghcr.io/spark-harness/fides-bff` |
| fides | `apps/fides/overlays/lendora-sta` | `ghcr.io/spark-harness/fides` |

Argo image release workflow 参数示例：

```text
repo-owner=spark-harness
repo-name=business-repo
build-context=.
dockerfile-dir=apps/<service>
dockerfile-name=Dockerfile
gitops-overlay-path=apps/<service>/overlays/lendora-sta
gitops-image-name=ghcr.io/spark-harness/<service>
promote=true
```

| Service | dockerfile-dir |
|---|---|
| applicant-api | `apps/applicant-api` |
| quote-api | `apps/quote-api` |
| origination-api | `apps/origination-api` |
| fides-bff | `apps/fides-bff` |
| fides | `apps/fides-web` |

## Verification

```bash
kubectl kustomize clusters/lendora-sta
kubectl kustomize apps/lendora-sta-dependencies/overlays/sta
kubectl kustomize apps/applicant-api/overlays/lendora-sta
kubectl kustomize apps/quote-api/overlays/lendora-sta
kubectl kustomize apps/origination-api/overlays/lendora-sta
kubectl kustomize apps/fides-bff/overlays/lendora-sta
kubectl kustomize apps/fides/overlays/lendora-sta
```

Runtime smoke 和回滚证据记录在 `harness-repo/requirements/LEN-77/evidence/`。
