from suds.client import Client
from suds import WebFault
from model.proj_mod import Proj


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + '/api/soap/mantisconnect.php?wsdl')
        #client = Client('http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl')
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def convert_projects_to_model(self, l):
        def convert(x):
            return Proj(name=x.name, description=x.description)

        result = []
        for z in l:
            result.append(convert(z))
        return result

    def get_soap_pr_list(self, username, password):
        client = Client(self.app.base_url + '/api/soap/mantisconnect.php?wsdl')
        #client = Client('http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl')
        pr_list = client.service.mc_projects_get_user_accessible(username, password)
        return self.convert_projects_to_model(pr_list)