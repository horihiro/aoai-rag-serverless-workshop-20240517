import azure.functions as func
from azure.cosmos import CosmosClient
import os

data_ingestor_bp = func.Blueprint()

cosmos_client = CosmosClient.from_connection_string(os.getenv("COSMOS_CONNECTION"))


@data_ingestor_bp.function_name(name="data-upload")
@data_ingestor_bp.route(route="data/upload_json", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def upload_json(req: func.HttpRequest) -> func.HttpResponse:
    container = cosmos_client.get_database_client(os.getenv("COSMOS_DB_NAME")).get_container_client(os.getenv("COSMOS_CONTAINER_NAME"))

    items = req.get_json()

    for item in items:
        container.upsert_item(item)

    return func.HttpResponse(f"{len(items)} data uploaded.", status_code=200)
