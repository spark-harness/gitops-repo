# Workflow Templates

保存可复用的 Argo WorkflowTemplate，例如 unit-test、pr-gate、release。

模板只描述执行流程和 secret 引用，不保存真实凭据。

## 镜像构建与发布策略

`github-image-release` 是 `business-repo` 主干镜像发布的标准模板。

它不是什么：它不是业务仓构建脚本，也不保存 registry 密钥或生产凭据。

它是什么：它定义 Argo CI 在收到 `business-repo` 主干 push 后如何取源码，并行构建和扫描 `applicant-api`、`fides-bff`、`fides` 三个镜像，回写 GitHub 状态，并把 GitOps 环境 overlay 一次性更新到不可变 digest。

### 构建器选择

默认使用 BuildKit，不使用 Kaniko。Kaniko 仓库已经归档，不再作为新的 Spark CI 构建器选型。

BuildKit 以 `moby/buildkit:rootless` 运行 `buildctl-daemonless.sh`，当前模板在 Kubernetes 中保留 `privileged: true`，后续如果集群启用更严格的 rootless builder 节点池，再收紧这项运行时权限。

### Tag 和 digest

- 主干构建推送 tag：`sha-<short-sha>`。
- 环境部署只引用 digest：`<image>@sha256:<digest>`。
- GitOps overlay 的 image 更新在三镜像扫描通过后统一提交，避免每个镜像各自 push。

### Secret 引用

模板只引用 Kubernetes Secret：

- `github-source-token`：读取源码仓。
- `registry-dockerconfig`：推送和扫描 registry 镜像。
- `github-status-token`：回写 GitHub commit status。
- `github-gitops-token`：把 digest promotion 提交回 GitOps 仓。

这些 Secret 必须由集群密钥管理或人工运维创建，不提交到 Git。
