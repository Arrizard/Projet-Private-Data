class UserContext:
    def __init__(self, id, liste_data, node_accessible, arc_length_to_node):
        self.id = id
        self.liste_data = liste_data
        self.node_accessible = node_accessible
        self.arc_length_to_node = arc_length_to_node

    def get_liste_data(self):
        return self.liste_data
    
    def get_node_accessible(self):
        return self.node_accessible
    
    def get_id(self):
        return self.id
    
    def get_arc_length_to_node(self):
        return self.arc_length_to_node