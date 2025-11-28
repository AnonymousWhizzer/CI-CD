from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

class OperationMeasure(BaseModel):
    a: float
    b: float
    operator: str
    result: float
    durationMs: float

def get_operation_name(op: str) -> str:
    if op == '+':
        return 'Sum'
    if op == '-':
        return 'Subtraction'
    if op == '*':
        return 'Multiplication'
    if op == '/':
        return 'Division'
    return 'Operation'


class ExpressionMeasures(BaseModel):
    expression: str
    result: float
    totalDurationMs: float
    operations: List[OperationMeasure]

app = FastAPI()

@app.post("/measures")
async def receive_measures(measures: ExpressionMeasures):
    # Do whatever you want with the data here (store in DB, log, etc.)
    print("=== New measures received ===")
    print("Expression:", measures.expression)
    print("Result:", measures.result)
    print("Total duration (ms):", measures.totalDurationMs)
    for i, op in enumerate(measures.operations, start=1):
        name = get_operation_name(op.operator)
        print(
            f"{name}: {op.a} {op.operator} {op.b} = {op.result} "
            f"({op.durationMs:.3f} ms)"
        )

    print("=============================\n")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50060)
