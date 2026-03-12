class DonneContext:
    def __init__(self, id,taille):
        self.id = id
        self.taille = taille

    def get_id(self):
        return self.id
    
    def get_taille(self):
        return self.taille