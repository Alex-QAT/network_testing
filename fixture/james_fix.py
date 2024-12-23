
from telnetlib import Telnet

# Класс помощник по обращениям к почтовому серверу James
class JamesHelper:

    def __init__(self, app):
        self.app = app

    # метод проверки существования юзера на почтовом сервере
    def ensure_user_exists(self, username, password):
        # получаем конфиг из фикстуры app
        james_config = self.app.config['james']
        # устанавливаем сессию с почтовым сервером (прямые значения параметров)
        #session = JamesHelper.Session('localhost', 4555, 'root', 'root')
        # устанавливаем сессию с почтовым сервером (значения параметров берём из фикстуры app, которые прописаны в target.json)
        session = JamesHelper.Session(james_config['host'], james_config['port'], james_config['username'], james_config['password'])
        # проверяем методом из класса сессии is_user_reged_username:
        # если такой юзер есть - то поменять ему пароль
        if session.is_user_reged_username(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit_session()


    # Вспомогательный класс (класс в классе) внутри метода чтобы  все обращения к почтовому серверу по телнету шли в рамках одной сессии
    class Session:
        # конструктор класса сессии подключения к почтовому серверу (!!!логин и пароль от почтового сервера!!!)
        # подход очень простой пишем и читаем на синтаксисе james (для этого мы к нему подключились по телнету порт 4555, посмотрели в help синтаксис команд)
        # проделали все команды которые надо реализовать и записываем в коде что мы пишем туда и что оттуда ждём для чтения
        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host, port, 5)
            self.read_until('Login id:')
            self.write(username + '\n')
            self.read_until('Password:')
            self.write(password + '\n')
            self.read_until('Welcome root. HELP for a list of commands')

        # метод проверки существования пользователя
        def is_user_reged_username(self, username):
            # команда для james на проверку сущуствующего пользователя
            self.write('verify %s \n' % username)
            # в ответе может быть либо exist либо does not exist
            # команде expect в качестве параметра принимает список возможных вариантов
            # в качестве параметров могут быть даже не строки, но даже регулярные выражения
            # результатом будет кортеж состоящий из 3 частей: 1 - № совпадения (0,1,2...); 2 - объект типа match (результат проверки регулярного выражения);
            # 3 - сам прочитанный текст.
            res = self.telnet.expect([b'exists', b'does not exist'])
            # возвращаем нулевой элемент из результирующего кортежа который равен 0, т.е. нулевой номер совпадения, т.е. exists
            return res[0] == 0

        # вспомогательные функции для чтения и записи в кодировке ascii т.к. библиотека telnetlib использует тип данных string в байтовом формате
        # функция на чтение:
        def read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), 5)

        def write(self, text):
            self.telnet.write(text.encode('ascii'))

        # метод создания пользователя
        def create_user(self, username, password):
            self.write('adduser %s %s\n' % (username, password))
            self.read_until('User %s added' % username)

        # метод смены пароля
        def reset_password(self, username, password):
            self.write('setpassword %s %s\n' % (username, password))
            self.read_until('Password for %s reset' % username)

        # метод завершения сессии
        def quit_session(self):
            self.write('quit\n')



