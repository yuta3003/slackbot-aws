# 環境変数を設定する
## direnv
```
export AccessKey="XXXXXXXXXXXXXXXXXXX"
export SecretAccessKey="XXXXXXXXXXXXXXXXXXXXXX"
export SLACK_BOT_TOKEN="xoxb-XXXXXXXXXXXXXXX-XXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXX"
export SLACK_APP_TOKEN="xapp-X-XXXXXXXXXX-XXXXXXXXXX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

# Usage
- rename
```
mv credentials.json.template credentials.json
```
- edit


- package install
```
poetry install
```
- Into poetry
```
poetry shell
```
- start
```
cd slack_bot
python slackbot.py
```
