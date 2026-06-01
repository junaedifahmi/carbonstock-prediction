import asyncio


class Engine:
    VERSION = ""

    def __init__(self):
        print("okay")

    def invoke(self):
        return asyncio.run(self.ainvoke())

    async def ainvoke(self):
        print("Async simulation")

    def __call__(self, **kwargs):
        print("called")

    def __repr__(self):
        return
