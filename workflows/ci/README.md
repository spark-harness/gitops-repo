# CI Workflow Entrypoints

保存由 Argo Events 触发的 workflow 入口。

GitHub webhook 先进入 Argo Events EventSource，再由 Sensor 创建 Argo Workflow。

PR 合并门禁需要由 Workflow 回写 GitHub commit status 或 check run；只触发 Workflow 本身不能阻止合并。
