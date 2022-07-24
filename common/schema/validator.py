from jsonschema import validate
from jsonschema.exceptions import ValidationError
from base import BaseClass
from common.schema.schema import SCHEMA_NEWS


class Validator(BaseClass):
    SCHEMA = None

    def __init__(self):
        super().__init__()

    def validate(self, entry):
        try:
            self.log.info('Validating %s' % entry)
            validate(instance=entry, schema=self.SCHEMA)
            self.log.info('Entry validated: passed')
            return True, "OK"
        except ValidationError as e:
            return False, e.message


class NewsValidator(Validator):
    SCHEMA = SCHEMA_NEWS

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    sample = {
        "source": "Thanh Niên",
        "title": "Đà Nẵng nghiên cứu tiện ích nhắn tin khi vi phạm đến chủ phương tiện",
        "sapo": "Theo thống kê của Phòng CSGT (PC67, Công an TP.Đà Nẵng), từ ngày 1.1.2016 đến hết tháng 1.2018, "
                "PC67 gửi 13.479 lượt thông báo đến chủ phương tiện vi phạm luật Giao thông đường bộ.",
        "body": "Xử lý phạt nguội qua camera giám sát tại Phòng CSGT Công an TP.Đà Nẵng - Nguyễn Tú \nĐến nay còn "
                "5.199 trường hợp chưa đến giải quyết, chiếm 38,5%. Đối với 8.280 trường hợp đến làm việc, "
                "qua phân tích lỗi, cơ quan chức năng đã lập biên bản 7.184 trường hợp, chuyển kho bạc hơn 9 tỉ đồng, "
                "tước giấy phép lái xe (có thời hạn) 2.107 trường hợp.\n Hiện PC67 Đà Nẵng có nhiều kênh để thông báo "
                "đến chủ xe như gửi thông báo đến địa chỉ đăng ký qua đường bưu điện, cập nhật danh sách lên trang "
                "Facebook “Cảnh sát giao thông Công an TP.Đà Nẵng”. Từ ngày 22.9.2017, trang thông tin điện tử Công "
                "an TP.Đà Nẵng cũng có chuyên mục tra cứu vi phạm giao thông qua hệ thống camera giám sát tại địa chỉ "
                "www.catp.danang.gov.vn:8001/thongtinvipham...\n Tuy nhiên, số trường hợp chưa giải quyết được cũng "
                "tương tự TP.HCM là do thay đổi địa chỉ, chưa sang tên đổi chủ sau mua bán, xe thuê, sai thông tin... "
                "\n Trung tá Phan Văn Thương, Phó trưởng phòng PC67 Công an TP.Đà Nẵng, cho hay hiện trang Facebook "
                "và cổng thông tin có nhiệm vụ 1 - 2 ngày phải cập nhật danh sách vi phạm mới nhất để người dân tra "
                "cứu. Nếu chủ phương tiện không đến giải quyết thì danh sách được chuyển sang Trung tâm đăng kiểm để "
                "từ chối đăng kiểm các phương tiện này. \n Thời gian đầu áp dụng hình thức phạt nguội, có chủ phương "
                "tiện bị phạt đến 15 lần, khi xe hết hạn, đi đăng kiểm mới nhận được thông báo nộp phạt với số tiền "
                "rất lớn. Nay thì khác, với tổ chức, công dân vi phạm 2 lần trở lên sẽ bị lực lượng chức năng gọi "
                "điện trực tiếp để xác minh, nhắc nhở chủ xe " "kịp thời chấn chỉnh, vì các xe vi phạm nhiều lần chủ "
                "yếu là xe làm dịch vụ cho thuê, giao người khác sử dụng, khai thác...”, trung tá Phan Văn Thương cho "
                "hay. \n Công an TP.Đà Nẵng đang nghiên cứu cho ra đời ứng dụng trên thiết bị di động, thông báo vi "
                "phạm đến số máy " "chủ phương tiện, vừa sử dụng cho công tác phạt nguội, kết hợp các tiện ích phục "
                "vụ phòng chống tội phạm khác bằng biện pháp tăng mức tương tác với chủ phương tiện.",
        "id": 24858235,
        "publish": "2018-02-04T22:15:07Z",
        "tags": [],
        "keywords": [
            "Công an TP.Đà Nẵng",
            "Phan Văn Thương",
            "Nguyễn Tú",
            "Luật giao thông đường bộ",
            "Đăng kiểm",
            "Sang tên",
            "Tra cứu",
            "Server",
            "Phòng cảnh sát giao thông",
            "Giấy phép lái xe",
            "Cổng thông tin",
            "Chấn chỉnh",
            "Cho thuê",
            "Nhắc nhở",
            "Di động",
            "Phòng chống",
            "Vi phạm",
            "Mua bán",
            "Đà Nẵng",
            "Ra đời",
            "Giám sát"
        ],
        "cates": [
            "Pháp luật"
        ]
    }

    validator = NewsValidator()
    print(validator.validate(sample))
