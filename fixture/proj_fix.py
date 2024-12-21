from model.proj_mod import Proj

class ProjHelper:

    def __init__(self, app):
        self.app = app

    def create_project(self, proj):
    #def create_project(self):
        self.start_create()
        self.fill_pr(proj)
        #self.fill_pr()
        self.complete_create()
        # кэш теряет актуалность
        self.proj_cache = None

    def start_create(self):
        wd = self.app.wd
        self.open_man_proj_page()
        # init group creation
        wd.find_element_by_css_selector("input[value='Create New Project']").click()

    def open_man_proj_page(self):
        wd = self.app.wd
        #if not (wd.current_url.endswith("group.php") and len(wd.find_elements_by_name("new")) > 0):
        wd.find_element_by_link_text("Manage").click()
        wd.implicitly_wait(1)
        wd.find_element_by_link_text("Manage Projects").click()



    def fill_pr(self, proj):
        wd = self.app.wd
        #wd.find_element_by_name("name").click()
        #wd.find_element_by_name("name").clear()
        #wd.find_element_by_name("name").send_keys("Project_name123")
        # fill group form
        self.chng_fld_pr("name", proj.name)
        self.chng_fld_pr("description", proj.description)

    def chng_fld_pr(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def complete_create(self):
        wd = self.app.wd
        # submit group creation
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        self.open_man_proj_page()


    def count_pr(self):
        wd = self.app.wd
        self.open_man_proj_page()
        l = 0
        l = len(wd.find_elements_by_xpath('//a[contains(@href,"manage_proj_edit_page.php?project_id")]'))
        return l
        #return wd.find_elements_by_xpath('//a[contains(@href,"manage_proj_edit_page.php?project_id")]')


    proj_cache = None
    # метод получения списка проектов
    def get_pr_list(self):
        if self.proj_cache is None:
            wd = self.app.wd
            self.open_man_proj_page()
            self.proj_cache = []
            for element in wd.find_elements_by_xpath('//a[contains(@href,"manage_proj_edit_page.php?project_id")]'):
                text = element.text
                self.proj_cache.append(Proj(name=text))
        return list(self.proj_cache)


    def del_project_by_index(self, index):
        wd = self.app.wd
        self.open_man_proj_page()
        #select project
        wd.find_elements_by_xpath('//a[contains(@href,"manage_proj_edit_page.php?project_id")]')[index].click()
        #submit delete project
        wd.find_element_by_xpath('//input[@value="Delete Project"]').click()
        wd.find_element_by_xpath('//input[@value="Delete Project"]').click()
        # return to group page
        #self.open_man_proj_page()
        # кэш теряет актуалность
        self.proj_cache = None