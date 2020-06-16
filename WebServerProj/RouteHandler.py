

class RouteHandler(object):
    def __init__(self, path: str = "/home"):
        self.path_to_handle = path

    def __call__(self, func, *args, **kwargs):
        def new_func(*args, **kwargs):
            return func(*args, **kwargs)

        return new_func


