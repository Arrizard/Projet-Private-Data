class NodeContext:
    def __init__(self, id, memoryCapacity, liste_data_stocked, noeud_accessible):
        self.id = id
        self.memoryCapacity = memoryCapacity
        self.liste_data_stocked = liste_data_stocked
        self.noeud_accessible = noeud_accessible

    def get_id(self):
        return self.id

    def get_memoryCapacity(self):
        return self.memoryCapacity

    def get_liste_data_stocked(self):
        return self.liste_data_stocked

    def get_noeud_accessible(self):
        return self.noeud_accessible