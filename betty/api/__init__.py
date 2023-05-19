from abc import ABCMeta, abstractmethod


class BaseAPI(metaclass=ABCMeta):
    @abstractmethod
    def build_messages(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_json(self, *args, **kwargs):
        ...

    @abstractmethod
    def stream_json(self, *args, **kwargs):
        ...
