class ArcContext:
    def __init__(self, id,node1 ,node2,longueur):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.longueur = longueur

    def get_id(self):
        return self.id
    
    def get_longueur(self):
        return self.longueur