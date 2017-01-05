from config.driver import Driver


class BasePage(object):
    def __init__(self, url):
        self.driver = Driver.get()
        self.page_url = url
        self.open_page()

    def open_page(self, url=None):
        if not url:
            url = self.page_url
        self.driver.get(url)
        return self
