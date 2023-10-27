# TODO

- slackbot作成手順の作成
- slackbotの配置先をAWSにする
  - docker imageをECRに登録手順の作成
  - ECRからECSに登録手順の作成
  - ネットワーク構成図の作成
- slackbotのPythonをアップデート
- IAMロールに変更(ECSに適宜ポリシーを追加していく)


# AWS構成図

```mermaid
flowchart LR

subgraph PC[Local PC]
  subgraph Docker[Docker]
    Container("container")
  end
end

subgraph GitHub[GitHub]
  Repository[(slackbot-aws)]
end

subgraph AWS[AWS]
  CodeBuild[CodeBuild]
  subgraph VPC[VPC]
    ECR[(ECR)]
    subgraph PrivateSubnet[PrivateSubnet]
      ECS1[ECS]
      ECS2[ECS]
    end
    subgraph PublicSubnet[PublicSubnet]
      ALB{{ALB}}
    end
  end
end

USER[user]
SLACK[Slack]

%%サービス同士の関係
Container --> Repository
Repository --> CodeBuild
CodeBuild --> ECR
ECR --> ECS1
ECR --> ECS2
ALB --> ECS1
ALB --> ECS2
USER --> SLACK
SLACK --> ALB

%%グループのスタイル
classDef SGroup fill:none,color:#345,stroke:#345
class PC SGroup
class Docker SGroup
class GitHub SGroup
class AWS SGroup

classDef SPublicSubnet fill:#efe,color:#092,stroke:none
class PublicSubnet SPublicSubnet

classDef SPrivateSubnet fill:#def,color:#07b,stroke:none
class PrivateSubnet SPrivateSubnet

classDef SVPC fill:none,color:#0a0,stroke:#0a0
class VPC SVPC

%%サービスのスタイル
classDef SService fill:#aaa,color:#fff,stroke:#fff
class USER,SLACK,Container SService

classDef SCP fill:#e83,color:#fff,stroke:none
class ECS1,ECS2 SCP

classDef SNW fill:#84d,color:#fff,stroke:none
class ALB SNW

classDef SDB fill:#46d,color:#fff,stroke:#fff
class ECR,Repository SDB

classDef SDevTool fill:#a7d,color:#fff,stroke:#fff
class CodeBuild SDevTool

classDef SDocker fill:#33f,color:#fff,stroke:#fff
class Docker SDocker

```



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
