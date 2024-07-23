from pathlib import Path
import argparse
import json
from langchain_community.document_loaders import BSHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_openai import OpenAIEmbeddings
import settings


TEXT_SPLIT_CHUNK_SIZE = 1000
TEXT_SPLIT_OVERLAP_PERCENT = 0.2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_dir",
        type=str,
        help="Input directory with book data",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve(strict=True)

    docs = []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_SPLIT_CHUNK_SIZE,
        chunk_overlap=int(TEXT_SPLIT_CHUNK_SIZE * TEXT_SPLIT_OVERLAP_PERCENT),
        add_start_index=True,
    )

    for html_content in input_dir.glob("*.html"):
        metadata_file = html_content.parent / Path(f"{html_content.name}.metadata.json")
        metadata = json.loads(metadata_file.read_text())

        loader = BSHTMLLoader(html_content)
        data = loader.load()

        # Adjust document metadata
        del data[0].metadata["source"]
        data[0].metadata["title"] = metadata["title"]
        data[0].metadata["url"] = metadata["url"]

        # Split document into chunks
        all_splits = text_splitter.split_documents(data)
        docs.extend(all_splits)

    total_chunk_size = 0
    for doc in docs:
        total_chunk_size += len(doc.page_content)
    print(
        f"Chunking produced {len(docs)} docs with average "
        f"size of {int(total_chunk_size / len(docs))}"
    )

    # Process in batches of 500
    for index in range(0, len(docs), 500):
        docs_to_index = docs[index : index + 500]
        OpenSearchVectorSearch.from_documents(
            documents=docs_to_index,
            opensearch_url=f"https://{settings.OPENSEARCH_HOST_ENDPOINT}:9200",
            embedding=OpenAIEmbeddings(),
            http_auth=("admin", "admin"),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            index_name=settings.KB_INDEX_NAME,
        )


if __name__ == "__main__":
    main()
