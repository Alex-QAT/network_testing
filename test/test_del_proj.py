from model.proj_mod import Proj
import random


def test_del_rnd_project(app, config):
    username = config["web_admin"]['username']
    password = config["web_admin"]['password']
    app.session.login(username, password)
    if len(app.project.get_pr_list()) == 0:
        app.project.create_project(Proj(name="test_proj", description="jgksl;gajdlgkr"))
    # получение списка проектов из UI
    #old_pr_list = app.project.get_pr_list()
    # альтернативный метод - получение списка проектов с помощью soap
    old_pr_list = app.soap.get_soap_pr_list(username, password)
    index = random.randrange(len(old_pr_list))
    # Отладка
    print('\n Before - ', app.project.count_pr())
    app.project.del_project_by_index(index)
    #Отладка
    print('\n After - ', app.project.count_pr())
    assert len(old_pr_list) - 1 == app.project.count_pr()
    # получение списка проектов из UI
    #new_pr_list = app.project.get_pr_list()
    # альтернативный метод - получение списка проектов с помощью soap
    new_pr_list = app.soap.get_soap_pr_list(username, password)
    old_pr_list[index:index+1] = []
    sort_old_pr_list = sorted(old_pr_list)
    sort_new_pr_list = sorted(new_pr_list)
    assert sort_old_pr_list == sort_new_pr_list
    app.session.logout()


