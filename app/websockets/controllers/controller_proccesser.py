class ControllerProcesser:
    def __init__(self):
        self.handlers = {}

    async def process(self, handler_data, user):
        type = handler_data.get("type")
        if type not in self.handlers:
            return

        return await self.handlers[type](handler_data, user)

    def handler(self, path):
        def add_to_handlers(function):
            assert path not in self.handlers
            self.handlers[path] = function

        return add_to_handlers
