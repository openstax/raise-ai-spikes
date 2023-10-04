from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import boto3

client = boto3.client('sagemaker-runtime')

app = FastAPI(
    title="Raise AI API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET, POST"]
)


class ResponseModel(BaseModel):
    labels: List[str]
    scores: List[float]


class InputModel(BaseModel):
    input: str
    labels: List[str]
    multi_label: bool


@app.post("/predict/", response_model=ResponseModel)
async def post_predict(input_model: InputModel):
    data = {
        'inputs': input_model.input,
        'parameters': {
            'candidate_labels': input_model.labels,
            'multi_label': input_model.multi_label
        }
    }

    response = client.invoke_endpoint(
        EndpointName='zero-shot-classifier',
        ContentType='application/json',
        Body=json.dumps(data)
    )

    response_stream = json.loads(response['Body'].read())

    return {
        'labels': response_stream.get('labels'),
        'scores': response_stream.get('scores')
    }
