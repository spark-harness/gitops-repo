# CI Workflow Entrypoints

保存由 Argo Events 触发的 workflow 入口。

GitHub webhook 先进入 Argo Events EventSource，再由 Sensor 创建 Argo Workflow。

PR 合并门禁需要由 Workflow 回写 GitHub commit status 或 check run；只触发 Workflow 本身不能阻止合并。

`github-pr-smoke` 只验证 GitHub webhook 到 Argo Workflow 的最小链路。

`github-repo-gates` 是 Spark 仓库门禁入口。它接收 `harness-repo`、`business-repo`
和 `idl-repo` 的 PR 事件，为每个仓库创建对应 Argo Workflow，并回写稳定的
`spark/*` GitHub commit status。GitHub 仍是分支保护和合并控制面，Argo 是唯一门禁执行面。

业务仓接入镜像发布时，应新增面向目标仓库的 Sensor，并调用 `workflows/templates/github-image-release-workflow-template.yaml` 中的 `github-image-release` 模板。Sensor 负责把仓库名、commit、PR 编号、镜像名、Dockerfile 路径和 promotion 开关映射为模板参数。
