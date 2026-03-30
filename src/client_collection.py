class ClientCollection:
    def __init__(self, clients):
        self.clients = clients 
    
    def get_client_by_id(self, client_id):
        for cl in self.clients:
            if cl.client_id == client_id:
                return cl 
        return None 
    
    def clients_by_country(self, country):
        result = []
        for cl in self.clients:
            if cl.country == country:
                result.append(cl)
        return result 
    
    