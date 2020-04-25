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
    @abc.abstractmethod
    def menu_scroll(self, screen_num, up_down):
        pass
    @abc.abstractmethod
    def create_menu(self, screen_num, items):
        pass
    @abc.abstractmethod
    def get_menu_item(self, screen_num):
        pass
    @abc.abstractmethod
    def touch(self, screen_num):
        pass