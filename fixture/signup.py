
import re

# Класс-помощник по работе с механизмом создания нового ползователя на сайте Mantis
class SignupHelper:

    def __init__(self, app):
        self.app = app

    # вспомогательные метод для создания нового аккаунта Mantis
    def new_acc(self, username, email, password):
        wd = self.app.wd
        # переход на страницу создания нового аккаунта
        wd.get(self.app.base_url + '/signup_page.php')
        # заполнение формы
        wd.find_element_by_name('username').send_keys(username)
        wd.find_element_by_name('email').send_keys(email)
        wd.find_element_by_xpath('//input[@type="submit"]').click()
        #получение письма для подтверждения аккаунта
        mail = self.app.mail.get_mail(username, password, '[MantisBT] Account registration')
        # извлечение ссылки для подтверждения аккаунта
        url = self.extract_confirm_url(mail)
        # переход по извлечённой ссылке
        wd.get(url)
        # заполнение формы завершения регистрации с заданием и подтверждением пароля
        wd.find_element_by_name('password').send_keys(password)
        wd.find_element_by_name('password_confirm').send_keys(password)
        wd.find_element_by_xpath('//input[@value="Update User"]').click()

    # вспомогательный метод извлечения url ссылки из полученного текста письма
    def extract_confirm_url(self, text):
        # ищем текст начинающийся с http:// дальше символы регулярного выражения $ - конец строки. извлекаем всё (.group(0))
        return re.search('http://.*$', text, re.MULTILINE).group(0)


