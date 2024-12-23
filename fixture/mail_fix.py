# библиотека для получения почты poplib
import poplib

# библиотека для анализа текста email
import email
# библиотека для использования едениц измерения времени (таймауты в секундах и т.д.)
import time

# Класс-помощник по работе с почтовым ящиком польтзователя
class MailHelper:

    def __init__(self, app):
        self.app = app

    # метод получения письма со ссылкой на активацию аккаунта (параметр subject - тема письма)
    def get_mail(self, username, password, subject):
        for i in range(5):
            # установка сессии с хостом почтового сервера (адрес хоста из конфига в джейсоне)
            pop = poplib.POP3(self.app.config['james']['host'])
            # с каким именем логинемся
            pop.user(username)
            # с каким паролем логинемся
            pop.pass_(password)
            # определяем количество писем (первый элемент возвращаемого кортежа содержит количество писем)
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # получить первое письмо n+1 т.к. индексация писем начинается с 1 а не с 0.
                    # метод retr тоже возвращает кортеж, и сам текст письма назходится во втором элементе кортежа [0,1,2,...]
                    # поэтому берём второй элемент т.е. [1]
                    msglines = pop.retr(n+1)[1]
                    # но это список строчек, которые предстоит ещё склеить вместе
                    # ф-ия map с вложенной labda ф-ией, применяющей метод decode используется для перекодирования байтового типа в тип string
                    msgtext = '\n'.join(map(lambda x: x.decode('utf-8'), msglines))
                    # присваиваем переменной msg декодированный текст содержимого письма
                    msg = email.message_from_string(msgtext)
                    # анализируем полученный текст письма
                    # Если тема письма равна заданной
                    if msg.get('Subject') == subject:
                        # помечаем найденное письмо на удаление
                        pop.dele(n+1)
                        # закрываем сессию с сохранением (т.е. письма помеченные на удаление - удалятся)
                        # если нужно закрыть сессию без сохранения то выполняем pop.close() (письма помеченные на удаление - не удалятся)
                        pop.quit()
                        # возвращаем полезную нагрузку (тело) этого письма
                        return msg.get_payload()
            # если не найдено писам с такой темой или вообще не найдено никаких писем то тоже закрываем сессию
            pop.quit()
            # ждём 3 секунды (в цикле из 5 попыток)
            time.sleep(3)
            # если ничего не получилось то возвращаем None
            return None

