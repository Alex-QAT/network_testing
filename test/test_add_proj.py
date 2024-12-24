from model.proj_mod import Proj

def test_add_project(app, data_projects, config):
    username = config["web_admin"]['username']
    password = config["web_admin"]['password']
    app.session.login(username, password)
    proj = data_projects
    # получение списка проектов из UI
    #old_pr_list = app.project.get_pr_list()
    # получение списка проектов с помощью soap
    old_pr_list = app.soap.get_soap_pr_list(username, password)
    # Отладка
    print('\n Before - ', app.project.count_pr())
    #print(old_pr_list)
    app.project.create_project(proj)
    # Отладка
    print('\n After - ', app.project.count_pr())
    #new_pr_list = app.project.get_pr_list()
    new_pr_list = app.soap.get_soap_pr_list(username, password)
    #print(new_pr_list)
    assert len(old_pr_list) + 1 == app.project.count_pr()
    old_pr_list.append(proj)
    sort_old_pr_list = sorted(old_pr_list)
    sort_new_pr_list = sorted(new_pr_list)
    assert sort_old_pr_list == sort_new_pr_list
    app.session.logout()



