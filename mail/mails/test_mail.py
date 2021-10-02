from .base_mail import BaseMail


class TestMail(BaseMail):
    def __init__(self):
        super().__init__()
        self.subject = '測試信件'
        self.body = 'test_mail'
