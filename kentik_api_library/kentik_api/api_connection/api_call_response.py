from dataclasses import dataclass

@dataclass
class APICallResponse:
    http_status_code : int
    text : str # response body
    