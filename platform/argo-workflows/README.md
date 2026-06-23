# Argo Workflows

保存 Argo Workflows controller、RBAC、artifact repository 引用和平台级 WorkflowTemplate。

Workflow 可以执行 CI/CD 任务，但 GitHub PR 是否允许合并由 required check 决定。

## 安装说明

Argo Workflows 和 Argo Events 的 CRD 较大，安装时使用 server-side apply，避免 client-side apply 写入过大的 last-applied annotation。

```bash
kubectl apply --server-side -k platform/argo-workflows
```
