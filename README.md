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

# ネットワーク構成図
```mermaid
flowchart LR

%%外部要素のUser
OU1[User]
OUS[Slack]

%%グループとサービス
subgraph GC[AWS]
  subgraph GV[vpc]
    subgraph GS1[public subnet]
      NW1{{"ELB"}}
    end
    subgraph GS2[private subnet]
      CP1("ECS")
      CP2("ECS")
    end
  end
end

%%サービス同士の関係
OU1 --> OUS
OUS --> NW1
NW1 --> CP1
NW1 --> CP2

%%グループのスタイル
classDef SGC fill:none,color:#345,stroke:#345
class GC SGC

classDef SGV fill:none,color:#0a0,stroke:#0a0
class GV SGV

classDef SGPrS fill:#def,color:#07b,stroke:none
class GS2 SGPrS

classDef SGPuS fill:#efe,color:#092,stroke:none
class GS1 SGPuS

%%サービスのスタイル
classDef SOU fill:#aaa,color:#fff,stroke:#fff
class OU1 SOU
class OUS SOU

classDef SNW fill:#84d,color:#fff,stroke:none
class NW1 SNW

classDef SCP fill:#e83,color:#fff,stroke:none
class CP1 SCP
class CP2 SCP

classDef SDB fill:#46d,color:#fff,stroke:#fff
class DB1 SDB

classDef SST fill:#493,color:#fff,stroke:#fff
class ST1 SST


```
