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
