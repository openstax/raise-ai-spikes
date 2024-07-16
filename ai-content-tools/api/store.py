from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_openai import OpenAIEmbeddings
import settings


opensearch_vectorstore = OpenSearchVectorSearch(
    opensearch_url=f"https://{settings.OPENSEARCH_HOST_ENDPOINT}:9200",
    embedding_function=OpenAIEmbeddings(),
    http_auth=("admin", "admin"),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    index_name=settings.KB_INDEX_NAME,
)
