import azure.functions as func
import logging
import openai
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from typing import List

indexer_bp = func.Blueprint()


@indexer_bp.cosmos_db_trigger(arg_name="items",
                              connection="COSMOS_CONNECTION",
                              database_name=os.getenv("COSMOS_DB_NAME"),
                              container_name=os.getenv("COSMOS_CONTAINER_NAME"),
                              create_lease_container_if_not_exists=False,
                              feed_poll_delay=5000,
                              lease_container_name="leases")
def indexer(items: func.DocumentList):
    logging.info(f"Hello {items[0]['id']}")

    # Change Feed で取得したデータを1件ずつ取得
    # content の内容を Azure OpenAI Service にアクセスしてベクター化
    # AI Search のインデックスのスキーマへ変更
    # 複数のデータを一括で、AI Search のインデックスへ upsert で更新
