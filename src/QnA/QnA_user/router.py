import json

from src.QnA.models import QuestionGet
from src.knowledge_base.models import SearchInput
from src.weaviate_client import client
from typing import List, Dict
from fastapi import APIRouter


router = APIRouter(
    prefix="/qna",
    tags=["Q&A User"]
)


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["question", "answer", "tags"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_questions(data: List[Dict]) -> List[QuestionGet]:
    questions = []
    for item in data:
        question = QuestionGet(
            id=item['_additional']['id'],
            question=item['question'],
            answer=item['answer'],
            tags=item['tags']
        )
        questions.append(question)
    return questions


@router.get("/get-questions", response_model=List[QuestionGet])
async def get_questions():
    cursor = None
    questions_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Question", 100, cursor)
        if len(next_batch) == 0:
            break
        questions_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    questions_output = parse_questions(questions_unformatted)
    return questions_output


@router.get("/get-question/{question_id}", response_model=QuestionGet)
async def get_question(question_id: str):
    question_object = client.data_object.get_by_id(
        question_id,
        class_name="Question"
    )
    return QuestionGet(id=question_object["id"], question=question_object["properties"]["question"],
                       answer=question_object["properties"]["answer"], tags=question_object["properties"]["tags"])




@router.post("/search-question/")
async def search_question(text: SearchInput):
    max_distance = 0.26
    if text.searchString == "":
        return await get_questions()
    response = (
        client.query
        .get("Question", ["question", "answer", "tags"])
        .with_hybrid(
            query=text.searchString,
            properties=["tags^3", "question^2", "answer"],
            alpha=0.5
        )
        .with_near_text({
            "concepts": [text.searchString],
            "distance": max_distance

        })
        .with_additional(["score", "explainScore"])
        .with_additional("id")
        .do()
    )

    questions = []
    if len(response["data"]["Get"]["Question"]) < 3:
        response = (
            client.query
            .get("Question", ["question", "answer", "tags"])
            .with_hybrid(
                query=text.searchString,
                properties=["tags^3", "question^2", "answer"],
                alpha=0.5
            )
            .with_near_text({
                "concepts": [text.searchString],
            })
            .with_additional("id")
            .with_limit(3)
            .do()
        )
    for i in range(len(response["data"]["Get"]["Question"])):
        questions.append(QuestionGet(
            id=response["data"]["Get"]["Question"][i]["_additional"]["id"],
            tags=response["data"]["Get"]["Question"][i]["tags"],
            question=response["data"]["Get"]["Question"][i]["question"],
            answer=response["data"]["Get"]["Question"][i]["answer"],
        ))
    return questions