from selenium.webdriver import Chrome


class Driver(object):
    instance = None

    @classmethod
    def get(cls, browser_type=Chrome):
        if not cls.instance:
            cls.instance = browser_type()
        return cls.instance

    @classmethod
    def close(cls):
        cls.get().quit()
        cls.instance = None
