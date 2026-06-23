# Spark GitOps Repository

本仓库保存 Spark 环境的部署目标状态、平台组件配置和 Argo Workflows 模板。

它不是业务源码仓。业务源码、Dockerfile、测试代码、构建脚本仍保存在 `business-repo`；本仓库只引用构建后的镜像 tag 或 digest，并表达环境差异。

## 目录结构

```text
clusters/
  sta1/
  sta2/
  prod/
platform/
  argocd/
  argo-workflows/
  ingress/
  cert-manager/
  observability/
apps/
  applicant-api/
    base/
    overlays/
      sta1/
      sta2/
      prod/
workflows/
  templates/
  ci/
```

## 环境入口

- `clusters/sta1/`：STA1 集群入口，保存 STA1 namespace、AppProject 和 Argo CD Application 清单。
- `clusters/sta2/`：STA2 集群入口，保存 STA2 namespace、AppProject 和 Argo CD Application 清单。
- `clusters/prod/`：生产集群入口，保存生产 namespace、AppProject 和 Argo CD Application 清单。

每个环境目录只描述该环境要同步什么，不保存其他环境的默认值。
每个环境目录必须能通过 `kubectl kustomize clusters/<env>` 独立渲染。

## 平台组件

- `platform/argocd/`：Argo CD 自身安装和平台级配置。
- `platform/argo-workflows/`：Argo Workflows controller、RBAC、WorkflowTemplate 等配置。
- `platform/ingress/`：入口网关或 Ingress Controller 配置。
- `platform/cert-manager/`：证书管理配置。
- `platform/observability/`：日志、指标、追踪和告警相关组件配置。

## 应用部署

应用目录使用 Kustomize 形态：

- `apps/<app>/base/`：应用通用 Kubernetes 配置。
- `apps/<app>/overlays/<env>/`：环境差异，例如 namespace、replica、resource、image tag 或 digest。

首版示例使用 `apps/applicant-api/`。后续新增应用时沿用同样结构。

## Workflow

- `workflows/templates/`：可复用的 Argo WorkflowTemplate。
- `workflows/ci/`：由 Argo Events 触发的 CI/CD workflow 入口。

推荐边界：

- GitHub webhook 只负责把仓库事件送入 Argo Events。
- PR 触发 Argo gate workflow，并通过 GitHub required status 控制合并。
- merge 后 release workflow 构建或复用已验证镜像，并更新本仓库中的 image tag 或 digest。

镜像发布策略：

- PR 镜像使用临时 tag，只用于扫描和门禁，不作为环境部署输入。
- 主干发布镜像必须能追溯到 commit SHA。
- 环境 overlay 只接受不可变 digest。
- 业务仓负责 Dockerfile 和测试，本仓库负责 Argo Workflow 模板、Secret 引用和 GitOps digest promotion。

## 安全规则

- 不提交真实密钥、token、kubeconfig 或 registry 密码。
- Secret 只提交 ExternalSecret、SealedSecret 或 secret 引用。
- 生产环境配置必须显式表达，不继承临时环境的未审计配置。
- 镜像发布必须使用不可变 tag 或 digest，避免环境漂移。
