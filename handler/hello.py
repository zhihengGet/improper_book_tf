
import json
import local_package.GetBook


def res(data):
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {
            "content-type": "application/json",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }


def handler(event, context):
    old_books = json.loads(event["body"])["old"]
    if not old_books or len(old_books) < 3:
        return res("failed not enough")
    source = local_package.GetBook.GetBookFromSource()
    new_books = source.fetch_new_books(old_books)
    return res(new_books)
