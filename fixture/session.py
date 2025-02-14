class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, username, pswd):
        wd = self.app.wd
        # open home page
        self.app.open_home_page()
        # login
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(pswd)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()
        wd.find_element_by_name("username")

    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()
        #wd.find_element_by_name("user")

    def ensure_login(self, username, pswd):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, pswd)

        #wd.find_element_by_name(username, pswd)

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector('td.login-info-left span').text


