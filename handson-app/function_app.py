import azure.functions as func
from data_ingestor import data_ingestor_bp
from chat_app import chat_app_bp
from indexer import indexer_bp

app = func.FunctionApp()

app.register_functions(indexer_bp)
app.register_functions(chat_app_bp)
app.register_functions(data_ingestor_bp)
