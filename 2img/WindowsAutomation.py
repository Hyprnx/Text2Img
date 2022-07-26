from pywinauto import application
from pywinauto.keyboard import send_keys
from configparser import ConfigParser
from base import BaseClass


# Currently only support Windows 10 and Office 365 only, if you want to support other OS/office version,
# please contact me, or if you can do it yourself, create a PR :D

class AutomationGenerator(BaseClass):
    def __init__(self):
        super().__init__()
        config_path = 'common/config.ini'
        self.log.info(f'Reading config file from {config_path}')
        config = ConfigParser()
        config.read_file(open(config_path))
        application_path = config.get('local', 'application_path')
        self.save_path = config.get('local', 'save_path')
        self.log.info("Opening Word")
        self.app = application.Application(backend="uia")
        self.app.start(application_path)
        self.app.connect(path="WINWORD.EXE")
        self.log.info("Word opened")
        self._open_blank_document()

    def _experimental(self):
        pass



    def _open_blank_document(self):
        self.log.info("Opening blank document")
        self.app.Word.Pane0.Pane3.HomeGroupBox.HomePane.NewGroupBox.NewListBox.ListItem0.invoke()
        self.log.info("Blank document opened")

    def _edit_document(self, text):
        # apparently, if this doesn't work, try to close all Word windows, it should work, if it still not,
        # create a issue
        self.log.info("Editing document")
        text = text.replace('\n', '{ENTER}')
        text = text.replace('\t', '{TAB}')
        text = text.replace(' ', '{VK_SPACE}')
        self.app['Dialog']['Document'].type_keys(text)
        self.log.info("Document edited")


    def fetch_data(self):
        pass

    def save_document(self, text='Hello World', _id='12345678'):
        self._edit_document(text)
        self.app.Document['File Tab'].click()
        self.app.Document['Save As'].select()
        self.app.Document['Browse'].click()
        save_path = self.save_path.replace('\n', '{ENTER}').replace('\t', '{TAB}').replace(' ', '{VK_SPACE}')
        save_path = save_path + f'\\{_id}.pdf'
        send_keys(save_path)
        self.app.Document['Save as type:ComboBox'].click()
        # self.app.Document['Save as type:ComboBox'].type_keys("%{DOWN}")
        self.app.Document.print_control_identifiers()
        # self.app.Document['Save as type:ComboBox'].select("pdf")
        # send_keys("{ENTER}")


if __name__ == '__main__':
    text = '(Dân trí) - Ông Trần Văn Dự (SN 1961) - Nguyên Phó Cục trưởng Cục Quản lý xuất nhập cảnh, Bộ Công an, ' \
           'bị khởi tố, bắt tạm giam để điều tra về tội "Nhận hối lộ". Tối 25/7, Bộ Công an cho biết, mở rộng điều ' \
           'tra vụ án "Đưa hối lộ, nhận hối lộ" xảy ra tại Cục Lãnh sự Bộ Ngoại giao, Hà Nội và các tỉnh, thành phố, ' \
           'ngày 25/7, Cơ quan An ninh điều tra Bộ Công an đã ra quyết định bổ sung quyết định khởi tố vụ án hình sự ' \
           '"Lừa đảo chiếm đoạt tài sản"; quyết định khởi tố bị can, lệnh bắt bị can để tạm giam, lệnh khám xét chỗ ' \
           'ở, nơi làm việc đối với 6 bị can: Bà Nguyễn Mai Anh (SN 1976, tại Quảng Ninh) - Chuyên viên Vụ Quan hệ ' \
           'quốc tế Văn phòng Chính phủ;\n Ông Ngô Quang Tuấn (SN 1984, tại Hà Nội) - Chuyên viên Vụ Hợp tác quốc tế Bộ ' \
           'Giao thông vận tải; Ông Trần Văn Dự (SN 1961, tại Thái Bình) - Nguyên Phó Cục trưởng Cục Quản lý xuất ' \
           'nhập cảnh Bộ Công an; Ông Vũ Sỹ Cường (SN 1986, tại Hưng Yên) - Nguyên cán bộ Cục Quản lý xuất nhập cảnh ' \
           'Bộ Công an;Các bị can trên cùng bị khởi tố về tội "Nhận hối lộ", quy định tại Điều 354 Bộ luật Hình sự. ' \
           '\nNgoài ra, Cơ quan An ninh điều tra Bộ Công an còn khởi tố ông Bùi Huy Hoàng (SN 1988, tại Hải Dương) - ' \
           'Cán bộ Cục Y tế dự phòng Bộ Y tế, về tội "Lừa đảo chiếm đoạt tài sản" quy định tại Điều 174 Bộ luật Hình ' \
           'sự; Ông Nguyễn Tiến Mạnh (SN 1970, tại Bắc Giang) - Phó Giám đốc Công ty cổ phần du lịch thương mại Lữ ' \
           'Hành Việt, Giám đốc Công ty vận tải du lịch Hoàng Long Luxury, bị khởi tố về tội "Đưa hối lộ" quy định ' \
           'tại Điều 364 Bộ luật Hình sự. '
    AutomationGenerator().save_document(text, _id='132456789')
