from pathlib import Path
import argparse
import requests
import json


def get_tree_page_contents(book_tree):
    contents = []

    if "contents" in book_tree:
        for node in book_tree["contents"]:
            contents += get_tree_page_contents(node)
    else:
        contents.append(book_tree["id"].split("@")[0])

    return contents


def main():
    parser = argparse.ArgumentParser(description="Fetch OpenStax book pages")
    parser.add_argument(
        "book_json_url",
        type=str,
        help="URL to book JSON",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Output directory",
    )
    args = parser.parse_args()

    book_json_url = args.book_json_url
    output_dir = Path(args.output_dir).resolve(strict=True)

    book_json = requests.get(book_json_url).json()
    book_tree = book_json["tree"]

    pages = get_tree_page_contents(book_tree)

    for page_uuid in pages:
        page_json_url = f"{book_json_url.split('.json')[0]}:{page_uuid}.json"
        page_json = requests.get(page_json_url).json()

        with (output_dir / f"{page_uuid}.html").open("w") as outfile:
            outfile.write(page_json["content"])

        with (output_dir / f"{page_uuid}.html.metadata.json").open("w") as outfile:
            metadata = {
                "title": page_json["title"],
                "url": f"https://openstax.org/books/{book_json['slug']}/pages/{page_json['slug']}",
            }
            outfile.write(json.dumps(metadata))


if __name__ == "__main__":
    main()
