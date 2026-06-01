import asyncio
from .schema import InputFeatures, OutputPredicted


class Engine:
    VERSION = ""

    def __init__(self):
        print("okay")

    def invoke(self, data: InputFeatures) -> OutputPredicted:
        return asyncio.run(self.ainvoke())

    async def ainvoke(self, data: InputFeatures) -> OutputPredicted:
        print("Async simulation")

    def __call__(self, data: InputFeatures) -> OutputPredicted:
        print("called")

    def __repr__(self):
        return
