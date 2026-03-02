# citizen-apps – CLAUDE.md

このリポジトリは、市民開発者がチャットを通じてアプリを作成し、
最小限のGitHub操作でCloud Runへ公開するためのものです。

Claude Code はこのルールに従って動作してください。

---

# 🎯 Goal

- 市民開発者が自然言語で依頼
- Claudeが設計を説明
- 合意後に実装
- GitHubでPRを作成し、市民がMerge
- mainへの反映をトリガーに自動デプロイ
- Cloud RunのURLを確認して完了

---

# 🗂 Repository structure

- すべてのアプリは `apps/<appName>/` 配下に作成する
- 既存アプリは壊さない
- 変更は必要最小限にとどめる

例：

apps/
  hello/
  mini/
  <newAppName>/

---

# 🧠 Communication（説明 → 合意 → 実装）

依頼を受けたら、必ず以下を行う：

1. 要件を1〜3行で要約
2. 実装方針を説明する
   - どういう仕組みで実現するか
   - どの技術を使うか
   - どのファイルが作られるか
3. 公開までの流れを説明
   - ブランチ作成
   - PR作成
   - 市民がMerge
   - 自動デプロイ
4. 「この方針で開発を開始してよいですか？」と確認する

不明点があれば質問する。
ただし質問が多くなりすぎる場合は、デフォルト案を提示して合意を取る。

---

# 🧩 Default tech choices（指定がなければこれで進める）

- Language: Python 3.11
- Framework: Flask
- App server: gunicorn
- Container: Docker（python:3.11-slim）
- Deployment: Cloud Build → Artifact Registry → Workflows → Cloud Run
- Auth: なし（必要なら提案）
- Database: なし（必要ならFirestoreまたはCloud SQLを提案）

---

# 🌿 Git strategy（重要）

- mainブランチへ直接pushしない
- 必ず新規ブランチで作業する
  例: claude/<appName>-<shortRandom>
- 変更は原則1コミットにまとめる
- pushは作業ブランチへ行う

---

# 🔁 PR policy（重要）

- PRを自動作成しない（GitHub tokenやgh CLIが無い場合があるため）
- push後、必ず以下を出力する：

  1. ブランチ名
  2. PR作成URL（/pull/new/<branch>）
  3. 市民が行う操作手順：
     - Create pull request
     - Merge pull request

- 市民が「マージしました」と言ったら、
  デプロイ確認手順を案内する

---

# 🚀 Deploy

- 公開トリガーは main へのマージ
- mainへ反映されるとCloud Buildが自動実行される
- WorkflowsがCloud Runを更新する
- 市民はCloud RunのURLを確認するだけでよい

---

# 📛 Safety rules

- 既存アプリを削除しない
- cloudbuild.yaml を壊さない
- Workflows名は citizen-deploy を使用する
- サービス名は既存命名規則に従う（例: app-<appName>）

---

# 🧭 Output format

実装完了時は以下の順で出力する：

1. 変更内容の要約
2. 変更ファイル一覧
3. ブランチ名
4. PR作成URL
5. 「公開してURLを出しますか？」という確認文
