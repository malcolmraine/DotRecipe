from support.filter_collection import FilterCollection


class TaskList(object):
    def __init__(self):
        self.name = ""
        self.tasks = FilterCollection()

    def refresh_cache(self):
        ...

    def get_tasks(self):
        ...

    def update_list(self):
        ...

    def create_task(self, task):
        ...

    def delete_task(self, task):
        ...

    def update_task(self, task):
        ...

    def create_task_list(self):
        ...


class MSToDoClient(object):
    def __init__(self):
        self.credentials = None
        self.task_lists = FilterCollection()

    def refresh_cache(self):
        ...

    def get_lists(self):
        ...
