from abc import ABC, abstractmethod

class BaseDAO(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def delete_by_id(self, id):
        pass