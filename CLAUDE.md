このリポジトリは、市民開発者がチャットを通じてアプリを作成し、最小限のGitHub操作でCloud Runへ公開するためのものです。Claude Code はこのルールに従って動作してください。

🎯 Goal
市民開発者が自然言語で依頼し、Claudeが設計・実装を行う

GitHubでPRを作成し、市民がMergeボタンを押すだけで公開される

インフラ操作（GCP）はすべて自動化されているため、Claudeはコードに集中する

🗂 Repository structure
アプリ配置: apps/<appName>/ 配下に独立して作成

既存アプリへの干渉禁止（共通ライブラリがない限り、他ディレクトリは触らない）

🧠 Communication（説明 → 合意 → 実装）
依頼を受けたら、必ず以下のステップを踏むこと：

要件定義: 依頼を1〜3行で要約する

実装方針の提示: 使用技術、新規作成・修正するファイル一覧を説明する

リリースの案内:

「ブランチ作成 → Push → PR作成」の流れを説明

「マージ後、数分でPRのコメント欄にプレビューURLが届く」ことを伝える

承認確認: 「この方針で開発を開始してよいですか？」と確認し、合意後に着手する

🧩 Default tech choices
Language: Python 3.11

Framework: Flask (推奨)

App server: gunicorn

Container: Docker（python:3.11-slim をベースに使用。Port 8080で待受けること）

Deployment: 自動化済み（Cloud Build → Workflows → Cloud Run）

🌿 Git strategy
Branch: 必ず新規ブランチを作成する。命名: claude/<appName>-<short-uuid>

Commit: 原則1コミットにまとめ、意味のあるメッセージを付ける

Push: 作業ブランチへPushする。main への直接Pushは厳禁

🔁 PR policy
PRリンクの提示: Push後、PR作成URL（https://github.com/<owner>/<repo>/pull/new/<branch>）を出力する

手順案内: 市民に対し「PRを作成して、内容に問題がなければマージしてください」と案内する

デプロイの待ち合わせ:

「マージ後、Cloud Buildが自動でプレビュー環境を作成します」

「URLはPRのコメント欄に自動で投稿されるので、そちらを確認してください」と案内する

📛 Safety & Naming Rules
既存の破壊禁止: cloudbuild/*.yaml や既存アプリを削除・変更しない

サービス名: app-<appName> または <appName> を使用する

Workflows: 既存の citizen-deploy がデプロイを担うため、独自に作成しない

🧭 Output format
実装完了時は以下の順で出力する：

変更内容の要約

変更ファイル一覧

作業ブランチ名

PR作成用URL（リンク形式）

「マージ後、自動でデプロイが始まります。URLがコメントされるまでお待ちください」というメッセージ
