# Claude Code Operating Rules

## Interaction Rules
- 要件確認は最大2問まで
- 変更は原則1コミット
- PRは必ず自動作成
- 完成したら必ず
  「公開してURLを出しますか？」と聞く
- ユーザーが「はい」と答えたらPRをマージ
- GitHub Actionsは使用しない

## Repository Structure
- アプリは必ず apps/<appName>/ に作成する
- 各アプリは独立ディレクトリで管理する
- 既存アプリに影響を与えない

## Deployment Model
- main へのマージがデプロイトリガー
- デプロイはGCP側で行う

## Release rules（最小運用）
- main への直接pushは試みない（失敗しやすい）
- 変更は必ず作業ブランチで1コミット
- push後、必ずPR作成URLを表示する
- ユーザーに「このリンクを開いて、Create pull request → Merge を押してください」と案内する
- PR自動作成は行わない（token/ghが無いので）
