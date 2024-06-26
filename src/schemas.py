class_article = {
    "class" : "Article",
    "properties": [
        {
          "name" : "tags",
          "dataType" : ["text[]"]
        },
        {
          "name" : "title",
          "dataType" : ["text"]
        },
        {
          "name" : "text",
          "dataType" : ["text"]
        },
        {
            "name": "content",
            "dataType": ["text"],
            "vectorizer": "none"
        }
    ],
    "moduleConfig": {
        "generative-mistral": {
            "model": "mistral-medium-latest",
        },
    }
}

class_fund = {
    "class" : "Fund",
    "properties": [
        {
          "name" : "name",
          "dataType" : ["text"]
        },
        {
          "name" : "link",
          "dataType" : ["text"]
        },
        {
            "name": "logo_link",
            "dataType": ["text"]
        },
        {
            "name": "description",
            "dataType": ["text"]
        },
    ],
    "vectorizer": "none"
}


class_question = {
    "class" : "Question",
    "properties": [
        {
          "name" : "question",
          "dataType" : ["text"]
        },
        {
          "name" : "answer",
          "dataType" : ["text"]
        },
        {
          "name" : "tags",
          "dataType" : ["text[]"]
        },
    ],
    "moduleConfig": {
        "generative-mistral": {
            "model": "mistral-medium-latest",
        },
    }
}
