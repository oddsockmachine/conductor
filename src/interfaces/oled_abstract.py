import abc

class OLED_abstract(abc.ABC):
    @abc.abstractmethod
    def text(self, screen_num, text):
        pass
    @abc.abstractmethod
    def get_text(self):
        pass
    @abc.abstractmethod
    def set_encoder_assignment(self, assignment, screen_num=None):
        pass
    