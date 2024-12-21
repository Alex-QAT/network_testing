from model.proj_mod import Proj

def test_add_project(app, json_projects):
    proj = json_projects
    old_pr_list = app.project.get_pr_list()
    # Отладка
    print('\n Before - ', app.project.count_pr())
    app.project.create_project(proj)
    # Отладка
    print('\n After - ', app.project.count_pr())
    new_pr_list = app.project.get_pr_list()
    assert len(old_pr_list) + 1 == app.project.count_pr()
    old_pr_list.append(proj)
    sort_old_pr_list = sorted(old_pr_list)
    sort_new_pr_list = sorted(new_pr_list)
    assert sort_old_pr_list == sort_new_pr_list



