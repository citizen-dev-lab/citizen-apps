# citizen-apps – CLAUDE.md

このリポジトリは、市民開発者が自然言語で依頼するだけで、インフラやトークン、GitHubの操作を一切意識することなく、Cloud Runへアプリを公開するための「自動運転」環境です。Claude Code は以下のルールを厳守してください。

---

## 🎯 究極のゴール
- **ゼロ・クリック・デプロイ**: 依頼から公開まで、市民の手作業（マージボタンのクリック含む）を完全に排除する。
- **自律型エージェント**: AIが自ら鍵（トークン）を取得し、PRを作成し、デプロイ完了まで責任を持って見届ける。

---

## 🧠 コミュニケーション・プロトコル
依頼を受けたら、必ず以下のステップを踏むこと：
1. **要件定義**: 依頼を1〜3行で要約する。
2. **「全自動」の宣言**: 
   - 「これから実装し、PR作成からオートマージまで私がすべて代行します」
   - 「あなたは何も操作せず、このチャットでURLが届くのを待つだけでOKです」と伝える。
3. **承認確認**: 方針への合意を得てから実装を開始する。

---

## 🚀 完了プロトコル（実装完了時の自動実行）

実装が終わったら、Claudeはユーザーへの確認なしに以下の全工程を完遂する。

### Step 0: トークンの自給自足取得
環境変数 GITHUB_TOKEN がない場合、GCP Secret Managerから最新バージョンを自動取得する。
```bash
export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret="github-token")
Step 1: コミット & Push
新規ブランチ claude/<appName>-<uuid> を作成し、全作業内容をコミットしてリモートへPushする。

Step 2: PR作成（オートマージ前提）
取得した GITHUB_TOKEN を使い、curl で GitHub API を直接叩いて PR を作成する。
※Cloud Build側でオートマージが設定されているため、作成と同時にデプロイ工程が開始される。

Bash
curl -s -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d "{
    \"title\": \"Auto-deploy: <appName>\",
    \"head\": \"<branch-name>\",
    \"base\": \"main\",
    \"body\": \"AIによる全自動生成PRです。オートマージにより数分で本番公開されます。\"
  }" \
  "[https://api.github.com/repos/citizen-dev-lab/citizen-apps/pulls](https://api.github.com/repos/citizen-dev-lab/citizen-apps/pulls)"
Step 3: 執念深いURL報告（居残り監視）
PR作成後、すぐに会話を終了してはならない。main へのマージと Cloud Run への反映が完了するまで、gcloud コマンドで監視を継続する。

Bash
# 10秒おきに最大30回（約5分間）リトライしてURLを特定する
gcloud run services describe app-<appName> --region asia-northeast1 --format='value(status.url)'
公開URLが確認でき、かつアクセス可能（200 OK）になったことを確認してから最終報告を行う。

万が一失敗した場合は、Cloud Buildのログを確認し、市民に分かりやすく原因を説明する。

🧩 技術スタック（デフォルト）
Language: Python 3.11

Framework: Flask

Server: gunicorn

Container: python:3.11-slim (Port 8080で待受け)

Deployment: citizen-deploy (GCP Workflows)

🧭 出力フォーマット（最終報告時）
変更内容の簡潔な要約

作成された PR のリンク

✨ Cloud Run 公開URL（AIが自律的に取得したもの）

「お待たせしました！すべての工程が自動で完了し、アプリが公開されました。どうぞご確認ください！」というメッセージ
