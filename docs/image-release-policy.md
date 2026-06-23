# Image Release Policy

本文定义 Spark GitOps 仓的镜像构建、扫描和发布边界。

它不是什么：它不是业务仓 Dockerfile 规范，也不是 registry 密钥管理手册。

它是什么：它规定 Argo CI 如何把 GitHub 提交变成可追溯镜像，以及 GitOps 环境如何只引用已验证的不可变产物。

## 构建器

默认构建器是 BuildKit。

原因：

- BuildKit 支持 daemonless 构建，适合在 Argo Workflow 中按任务启动。
- BuildKit 能输出镜像 digest，便于 GitOps promotion。
- Kaniko 仓库已经归档，不作为新的 Spark CI 构建器选型。

当前 Argo 模板使用 `moby/buildkit:rootless` 和 `buildctl-daemonless.sh`。BuildKit rootless 容器显式使用 UID/GID `1000` 运行。由于 `vincent-k3s` 还没有专用 rootless builder 节点池，模板暂时保留 `privileged: true`。后续加固时，应先建立专用运行时，再移除该权限。

## Tag 与 digest

PR 构建：

- tag 格式：`pr-<pr-number>-<short-sha>`。
- 用途：扫描、门禁和人工排查。
- 禁止：作为环境部署输入。

主干构建：

- tag 格式：`sha-<short-sha>`。
- 用途：和 commit SHA 建立可读追溯。
- promotion 输入：镜像 digest。

环境部署：

- GitOps overlay 必须使用 `digest: sha256:<digest>`。
- Argo CD 只同步 GitOps 仓中已经提交的 digest。
- 不允许环境 overlay 依赖可移动 tag。

## 扫描门禁

镜像扫描使用 Trivy。

默认阻塞条件：

- `HIGH` 或 `CRITICAL` 漏洞。
- 扫描命令返回非零退出码。

扫描失败时，Workflow 必须回写 GitHub commit status 为 `failure`，对应 required check 不得通过。

## Promotion 边界

PR workflow 默认 `promote=false`，只构建、扫描和回写状态。

主干 release workflow 才允许 `promote=true`。promotion 执行以下动作：

1. 读取构建产物 digest。
2. 克隆 GitOps 仓目标分支。
3. 更新目标环境 overlay 的 `images[].digest`。
4. 提交并推送 GitOps 变更。

这意味着环境部署不是由业务仓直接 `kubectl apply` 触发，而是由 GitOps 仓中 digest 变化触发。

## Secret 引用

Argo 模板只引用 Secret 名称：

- `github-source-token`
- `registry-dockerconfig`
- `github-status-token`
- `github-gitops-token`

Secret 值不进入 Git。Secret 的创建和轮换属于集群运维职责。
