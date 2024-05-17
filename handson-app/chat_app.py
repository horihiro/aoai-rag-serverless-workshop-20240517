import os
import azure.functions as func
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI

chat_app_bp = func.Blueprint()

aoai_client = AzureOpenAI(azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                          api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                          api_version="2024-02-15-preview")
search_client = SearchClient(os.getenv("AI_SEARCH_ENDPOINT"),
                             os.getenv("AI_SEARCH_INDEX_NAME"),
                             AzureKeyCredential(os.getenv("AI_SEARCH_QUERY_KEY")))


@chat_app_bp.function_name(name="chat")
@chat_app_bp.route(route="chat", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def chat(req: func.HttpRequest) -> func.HttpResponse:
    # A: 質問の文章の取得: クエリ文字列 query の値
    query = req.params.get('query')
    # 質問の文章がない場合はエラーにする
    if not query:
        return func.HttpResponse("クエリ文字列 'query' に検索したい文字列を指定してください。",
                                 status_code=400)

    # B: ベクター検索の結果を取得
    json_references = search_references(query)

    # C: ベクター検索の結果をもとに回答を生成
    answer = generate_answer(query, json_references)
    return func.HttpResponse(answer,
                             mimetype="application/json",
                             status_code=200)


def search_references(text: str) -> str:
    """
    parameter の値をベクター化し、

    Parameters:
    text (str): ユーザーからの質問の文章

    Returns:
    str: ベクター検索の結果。JSON フォーマットの文字列。 
    """
    
    # 質問の文章をベクター化
    query_vector = aoai_client.embeddings.create(input=text, model=os.getenv("DEPLOYMENT_NAME_ADA")).data[0].embedding

    # ベクター化した質問の文章を使って、AI Search でベクター検索
    vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=3, fields="contentVector")
    search_results = search_client.search(
        search_text="",
        vector_queries=[vector_query],
        select=["title", "content", "category"])

    documents = [
        {
            "title": search_result["title"],
            "content": search_result["content"],
            "category": search_result["category"],
            "score": search_result["@search.score"]
        }
        for search_result in search_results
    ]

    # JSON フォーマットの文字列で返す
    return json.dumps(documents)


def generate_answer(query: str, references: str) -> str:
    """
    RAG パターンで回答を生成した結果を返す

    Parameters:
    query (str): ユーザーからの質ユーザー
    references (str): ベクター検索の結果の JSON フォーマットの文字列

    Returns:
    str: LLM で生成した質問の回答
    """

    example_answers = """[
  { "title": "1つめのAzureのサービス名", "description": "サービスの概要"},
  { "title": "2つめのAzureのサービス名", "description": "サービスの概要"}
]"""

    system_message = f"""
<Instructions>
あなたは Microsoft Azure の専門家です。Microsoft Azure に関する質問にのみ回答してください。
質問への回答は、以下の "references" tag から回答を日本語で生成してください。
回答のフォーマットは "example" タグを参考に JSONフォーマットの配列で出力してください。
<Instructions/>

<references>
{references}
</references>

<example>
{example_answers}
</example>"""

    completion = aoai_client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME_GPT"),
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}],
        # Jsom mode は、gpt-4-1106-preview / gpt-35-turbo-1106 のモデルで使用可能
        # response_format={ "type": "json_object" }
    )

    return completion.choices[0].message.content
