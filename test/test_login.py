import os.path


def test_login(app):
    #app.session.logout()
    # логинимся под заданными логином и паролем (данные заданы напрямую)
    app.session.login(username='administrator', pswd='root')
    # проверка что залогинены под заданной учёткой
    assert app.session.is_logged_in_as('administrator')
    #print(os.path.join(os.path.dirname(__file__)))