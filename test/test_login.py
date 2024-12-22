import os.path


def test_login(app):
    app.session.login()
    assert app.session.is_logged_in_as('administrator')
    #print(os.path.join(os.path.dirname(__file__)))