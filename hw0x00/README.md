# 协作开发基础

## 基本任务

- [x] Git 基本概念
- [x] Git 基本使用
- [x] Gitee 基本使用
- [x] Github 基本使用

## Git 基本概念

- 分布式版本控制软件，历史可追溯
  - 网站构建切记不能将 `.git` 目录放在 web 目录下：[GitHacker](https://github.com/WangYihang/GitHacker)

## Git 基本使用

### `git stash apply` Vs. `git stash pop`

- `git stash pop` 在应用后丢弃储存的变更，而 `git stash apply` 只应用不丢弃储存的变更
- 可以认为 `git stash pop` 是 `git stash apply && git stash drop`

## Gitee 自动同步到 Github

- 在 Github 新建用于同步的仓库
- 在仓库 `Settings` 中选择 `Secrets`，新建 `SYNC_PRIVATE_KEY`，添加 SSH 私钥
  - 对应公钥添加到 Gitee 的 `SSH公钥` 中，用于 SSH 克隆仓库
  - 再添加对应公钥到 Github `SSH keys` 中，用于目标仓库代码上传
- 在 Github 设置 `Developer settings` 中新建 `Personal access tokens`，并将其添加到 Github 仓库的 `Secrets` 中，用于自动创建不存在的仓库
- 使用 Github Actions
  ```yml
  # .github/workflows/sync2github.yml
  name: Sync Gitee Repository To Github

  on:
    schedule:
      - cron:  '0 */6 * * *'  # 每 6 小时执行一次同步

  jobs:
    build:
      runs-on: ubuntu-20.04
      steps:
      - name: Sync Gitee Repository To Github
        uses: Yikun/hub-mirror-action@master
        with:
          src: gitee/cuc-ccs
          dst: github/YanhuiJessica
          dst_key: ${{ secrets.SYNC_PRIVATE_KEY }} # SSH 私钥，用于目标仓库代码上传
          dst_token:  ${{ secrets.SYNC_TOKEN }}
          account_type: user
          clone_style: "ssh"
          force_update: true
          mappings: "cs-yanhu1-2021=>CS-YanhuiJessica-2021" # 目标仓库名和源仓库名不一致时需要映射
          static_list: "cs-yanhu1-2021" # 需要同步的仓库
  ```

## 参考资料

- [Yikun/hub-mirror-action](https://github.com/Yikun/hub-mirror-action)
  - [同步时，Github和Gitee的仓库名可否不同？](https://github.com/Yikun/hub-mirror-action/issues/64#issuecomment-900877883)
  - [gitee向github同步失败](https://github.com/Yikun/hub-mirror-action/issues/121)
- [Crontab.guru - The cron schedule expression editor](https://crontab.guru/)