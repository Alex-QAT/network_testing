
def test_signup_new_acc(app):
    username = "user2"
    password = 'test'
    # проверка предусловия что у юзера есть почта
    app.james.ensure_user_exists(username, password)