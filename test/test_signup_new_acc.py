
import string
import random

# генерация рандомного имени создаваемого пользователя на почтовом сервере (к слову делаем так, что имена юзеров на почте и на сайте у нас будут совпадать)
def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])

# тестовый метод создания нового аккаунта в Mantis
def test_signup_new_acc(app):
    #app.session.logout()
    # сохраняем в переменную сгенеренное рандомное имя пользователя
    username = random_username('user_',10)
    # сохраняем в переменную адрес почтового ящика нового пользователя
    email = username + '@mail.home'
    # созраняем в переменную пароль от почтового ящика (статичный, не генерим его)
    password = 'test'
    # проверка предусловия что у юзера есть почта (работа с James с помощью telnetlib)
    app.james.ensure_user_exists(username, password)
    # сам метод создания нового аккаунта (работа с Mantis (заполяем формы), работа с почтой POP3, подтверждение по ссылке и завершение регистрации)
    app.signup.new_acc(username, email, password)
    # проверка, логинимся под новым созданным аккаунтом
    #app.session.login(username, password)
    # альтернативная проверка возможности залогиниться с помощью SOAP
    assert app.soap.can_login(username, password)
    # разлогиниваемся
    app.session.logout()