# Argo CD

保存 Argo CD 自身安装、AppProject、repository credential 引用和平台级同步策略。

不要在本目录提交真实 repository token 或 kubeconfig。

## 目录边界

它不是什么：这里不是业务应用 overlay，也不是环境入口。

它是什么：这里保存可被各环境引用的 Argo CD 平台对象。

```text
platform/argocd/
  kustomization.yaml
  platform-metadata.yaml
```

每个环境的 `AppProject` 保存在 `clusters/<env>/argocd-project.yaml`。这样环境入口可以用默认 `kubectl kustomize clusters/<env>` 独立渲染，不依赖跨目录 load restrictor。

## 环境入口

每个环境目录必须能独立渲染：

```bash
kubectl kustomize clusters/sta1
kubectl kustomize clusters/sta2
kubectl kustomize clusters/prod
```

环境入口包含：

- 环境元数据。
- 环境 namespace。
- 环境 AppProject。
- 平台级 Application。
- 业务应用 Application。

生产环境 Application 必须显式表达自动同步策略，不继承 STA 环境默认值。
