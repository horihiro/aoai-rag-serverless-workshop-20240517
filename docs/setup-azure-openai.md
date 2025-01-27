# 🧪 S1. Azure OpenAI Service のセットアップ

ここでは、Azure OpenAI Service のリソースの作成とモデルのデプロイを行ないます。

- 0-1. Azure OpenAI Service のリソースの作成
- 0-2. モデルのデプロイ
- 0-3. クォータの更新

## 🔖 Azure OpenAI Service のリソースの作成

**※ すでに Azure OpenAI Service のリソースを作成済みの場合は、「Azure OpenAI Service のリソースの作成」は飛ばして「0-2. モデルのデプロイ」からご確認ください。**


Azure portal (`portal.azure.com`) を開き、上部の検索で「azure openai」と入力して表示される "Azure OpenAI" をクリックします。

![image](./images/0-1-1.png)

<br>

Azure OpenAI Service の一覧が表示されますので、"作成" をクリックします。


![image](./images/0-1-2.png)

<br>

Azure OpenAI の作成画面になります。以下を参考に入力し、"次へ" をクリック (⑥) します。

No.  | 項目 | 入力内容
---: | --- | ---
1 | サブスクリプション | 任意のサブスクリプションを選択します。
2 | リソースグループ | "新規作成" をクリックし、「rg-handson202309」と入力します。
3 | リージョン | 任意の場所を選択します。下図は東日本リージョンである「Japan East」を選択しています。
4 | 名前 | 任意の名称を入力します。これはグローバルで一意の名称になる必要があります。例:「oai-xxxx-handson202309」( "xxx" は自分のハンドルネームや任意のプロジェクト名など) 。
5 | 価格レベル | "Standard S0" を選択します。


"ネットワーク" と "タグ" はデフォルトの設定のままで "次へ" をクリックし "レビューおよび送信" まで進み、"作成" をクリックします。

![image](./images/0-1-3.png)

<br>

これでリソースの作成は完了です。リソースの作成が完了したら、"リソースに移動" をクリックします。

## 🔖 モデルのデプロイ

ここでは、ハンズオンで利用する2つのモデルをデプロイします。すでにデプロイ済みで利用可能なモデルがある場合は、そのモデルを利用しても問題ありません。

1. `text-embedding-ada-002`
2. GPT モデル (`gpt-35-turbo`, `gpt-4` などのいずれか)

### text-embedding-ada-002 のデプロイ

Azure OpenAI のリソースが表示されたら "概要" の上部にある "Go to Azure OpenAI Studio" をクリックして Azure OpneAI Studio に移動します。

![image](./images/0-2-1.png)

<br>

以下の手順でモデルのデプロイの準備をします。

- Azure OpenAI Studio の左メニュー "Models (モデル)" をクリック (①) します。
- "text-embedding-ada-002" をクリックしてチェックオン (②) にします。
- "Deploy (作成)" をクリック (③) します。

![image](./images/0-2-2.png)

<br>

"Deploy Model (モデルのデプロイ)" の画面が表示されます。

- "Select a model (モデルを選択してください)" で "text-embedding-ada-002" を選択されていることを確認します (①)。
- "Model Version (モデルバージョン)" はデフォルトのままにします。
- "Deployment Name (デプロイ名)" には、Model name と同様の "text-embedding-ada-002" を入力します (②)。
- "Create (作成)" をクリックしてデプロイを開始します (③)。

![image](./images/0-2-3.png)

### GPT モデル のデプロイ

前述と同様の手順で、GPT のモデル (`gpt-35-turbo`, `gpt-4` などのいずれか) をデプロイします。

> [!TIP]
> gpt-35-turbo や gpt-4 はバージョンが新しい方がコストも性能も高い傾向にあります。詳細は以下のドキュメントで確認できます。
>
> - [Azure OpenAI Service モデル | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/concepts/models)


また、"Deploy Model (モデルのデプロイ)" の画面で入力する "Deployment Name (デプロイ名)" はモデル名と同じにします。

<br>

最後に、左メニューの "Deployments" をクリックして2つのモデルがデプロイされていることが確認します。

<br>

## 🔖 クォータの更新

Azure OpenAI Service は、TPM (Tokens-per-Minute) という単位で、モデルがアクセスできるトークンの数を制限しています。クォータの詳細について興味がありましたら、以下のドキュメントをご参照ください。

- [Azure OpenAI Service のクォータを管理する | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/quota?tabs=rest)

ここではハンズオンを円滑に行なうためにクォータを変更します。

画面左の "クォータ" (Quatas) (①) をクリック > "Text-Embeddings-Ada-002" (②) を展開 > 今回作成した `text-enbedings-ada-002` のデプロイ (Deployment ID) (③) をクリックします。

![image](./images/0-3-1.png)

<br>

"詳細設定オプション" (Advanced options) をクリックします。

![image](./images/0-3-2.png)

<br>

"1分あたりのトークンレート制限" (Token per Minute Rate Limit) を「50k」に設定 (①)し、"保存して閉じる" (Save and close) (②) をクリックします。

![image](./images/0-3-3.png)

<br>

同様の手順で、GPTのモデルも10K程度に上げておきます。


## 📚 参考情報

- [Azure OpenAI Service モデル | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/concepts/models)
- [Azure OpenAI Service のクォータと制限](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/quotas-limits#regional-quota-limits)
- [Azure OpenAI Service のクォータを管理する | Microsoft Learn](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/quota?tabs=terraform)


## ⏭️ NEXT STEP ✨

最初の一歩として Azure OpenAI Service のセットアップが完了しました。続けて他に必要な Azure のリソースのセットアップを進めます。

---

[📋 目次](../README.md) | [⏭️ 次へ](.//setup-azure-resources.md)
