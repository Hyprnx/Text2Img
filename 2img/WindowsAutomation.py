from pywinauto import application
from pywinauto.keyboard import send_keys
from configparser import ConfigParser
from base import BaseClass



class AutomationGenerator(BaseClass):
    def __init__(self):
        super().__init__()
        config_path ='common/config.ini'
        self.log.info(f'Reading config file from {config_path}')
        config = ConfigParser()
        config.read_file(open(config_path))
        application_path = config.get('local', 'application_path')
        self.log.info("Opening Word")
        self.app = application.Application(backend="uia")
        self.app.start(application_path)
        self.app.connect(path="WINWORD.EXE")
        self.log.info("Word opened")
        self._open_blank_document()

    def _experimental(self):
        self.app['Document1 - Word']['Document'].Custom.Edit.TypeKeys("Hello World")

    def _open_blank_document(self):
        self.log.info("Opening blank document")
        self.app.Word.Pane0.Pane3.HomeGroupBox.HomePane.NewGroupBox.NewListBox.ListItem0.invoke()
        self.log.info("Blank document opened")

    # def edit_document(self, text):
    #     self.log.info("Editing document")
    #     self.app['Document1 - Word']['Document']["Custom"]["Edit"].TypeKeys(text)
    #     self.log.info("Document edited")

if __name__ == '__main__':
    text = 'Hello World'
    AutomationGenerator()._experimental()