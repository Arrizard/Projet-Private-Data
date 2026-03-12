import heapq

class NetWorkContext:
    def __init__(self, nodes, arcs, users, data): 
        self.nodes = nodes 
        self.arcs = arcs
        self.users = users 
        self.data = data
        self.graph = {}  # Graphe sous forme d'adjacence

    def build_graph(self):
        # Ajouter tous les nœuds système
        for node in self.nodes:
            self.graph[node.id] = []

        # Ajouter les nœuds virtuels des utilisateurs
        for user in self.users:
            self.graph[f"U{user.id}"] = []

        # Ajouter les arcs physiques (sans doublons)
        for arc in self.arcs:
            self.add_unique_edge(arc.node1, arc.node2, arc.longueur)
            self.add_unique_edge(arc.node2, arc.node1, arc.longueur)
        
        # # Placer les données sur les nœuds
        # for user in self.users:
        #     for data in user.liste_data:
        #         self.place_data_for_user(user, data)

        self.place_all_data_mkp()  # Placement MKP de toutes les données
        


    def place_data_for_user(self, user, data):
        best_node = self.find_best_node_for_data(user, data)
        if best_node:
            best_node.liste_data_stocked.append(data)
            best_node.memoryCapacity -= data.taille
            print(f"Donnée {data.id} placée sur le nœud {best_node.id}")


    def add_unique_edge(self, node1, node2, weight):
        # Ajoute un arc seulement s'il n'existe pas déjà
        if (node2, weight) not in self.graph[node1]:
            self.graph[node1].append((node2, weight))

    def add_data_on_user(self, user, data):
        user_node = f"U{user.id}"
        data_node = f"D{data.id}"

        # Lier Ux → Dx
        self.add_unique_edge(user_node, data_node, 0)

        # Lier Dx → Ux
        if data_node not in self.graph:
            self.graph[data_node] = []
        self.add_unique_edge(data_node, user_node, 0)

        self.place_data_for_user(user, data)
   
    def add_data_for_two_users(self, user1, user2, data):
        user1_node = f"U{user1.id}"
        user2_node = f"U{user2.id}"
        data_node = f"D{data.id}"

        # Lier U1 → Dx et U2 → Dx
        self.add_unique_edge(user1_node, data_node, 0)
        self.add_unique_edge(user2_node, data_node, 0)

        # Lier Dx → U1 et Dx → U2
        if data_node not in self.graph:
            self.graph[data_node] = []
        self.add_unique_edge(data_node, user1_node, 0)
        self.add_unique_edge(data_node, user2_node, 0)

        self.place_data_for_two_users(user1, user2, data)

    def place_data_for_two_users(self, user1, user2, data):
        best_node_id = self.find_best_node_for_two_users(user1, user2, data)

        if best_node_id is None:
            print("Aucun nœud optimal trouvé")
            return

        # Trouver l'objet NodeContext correspondant
        best_node = next(n for n in self.nodes if n.id == best_node_id)

        best_node.liste_data_stocked.append(data)
        best_node.memoryCapacity -= data.taille

        print(f"Donnée {data.id} placée sur le nœud {best_node.id} pour U{user1.id} et U{user2.id}")


    def dijkstra(self, start):
        # Initialiser toutes les distances à +infini
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0  # Distance du départ à lui-même = 0

        # File de priorité contenant les nœuds à explorer
        file_priorite = [(0, start)]  # (distance, nœud)

        while file_priorite:
            # Extraire le nœud le plus proche
            current_dist, current_node = heapq.heappop(file_priorite)

            # Si on a déjà trouvé mieux, on ignore
            if current_dist > distances[current_node]:
                continue

            # Explorer tous les voisins du nœud courant
            for neighbor, weight in self.graph[current_node]:
                new_dist = current_dist + weight  # Nouveau coût

                # Si meilleur chemin trouvé → mise à jour
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(file_priorite, (new_dist, neighbor))

        return distances
    

    def find_best_node_for_data(self, user, data):
        # Calculer les distances depuis l'utilisateur
        distances = self.dijkstra(f"U{user.id}")

        # Trier les nœuds système du plus proche au plus loin
        sorted_nodes = sorted(
            self.nodes,
            key=lambda node: distances[node.id]
        )

        # Choisir le premier nœud ayant assez de mémoire
        for node in sorted_nodes:
            if node.memoryCapacity >= data.taille:
                return node

        return None  # Aucun nœud compatible


    def print_graph(self):
        print("\n=== GRAPHE (lisible) ===")
        for node_id in sorted(self.graph, key=lambda x: str(x)):
            voisins = ", ".join([f"{v} (w={w})" for v, w in self.graph[node_id]])
            print(f"{node_id} -> {voisins}")

    def print_network_details(self):
        print("\n=== NŒUDS ===") 
        for n in self.nodes: 
            print(f"Node {n.id} | Capacité: {n.memoryCapacity} | Accessible: {n.noeud_accessible}") 

        print("\n=== UTILISATEURS ===") 
        for u in self.users: 
            print(f"User {u.id} | Données requises: {[(f'D{data.id}({data.taille})') for data in u.liste_data]} | Nœud de départ: {u.node_accessible} | Longueur arc: {u.arc_length_to_node}") 

        print("\n=== ARCS ===") 
        for a in self.arcs: 
            print(f"Arc {a.id} | {a.node1} <-> {a.node2} | longueur {a.longueur}")

    def dijkstra_with_path(self, start):
        # Distances initialisées à +infini
        distances = {node: float('inf') for node in self.graph}
        # Pour reconstruire le chemin
        previous = {node: None for node in self.graph}

        distances[start] = 0

        # File de priorité (distance, nœud)
        file_priorite = [(0, start)]

        while file_priorite:
            current_dist, current_node = heapq.heappop(file_priorite)

            # Si on a déjà mieux, on ignore
            if current_dist > distances[current_node]:
                continue

            # Parcours des voisins
            for neighbor, weight in self.graph[current_node]:
                new_dist = current_dist + weight

                # Meilleur chemin trouvé
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_node
                    heapq.heappush(file_priorite, (new_dist, neighbor))

        return distances, previous
    
    def reconstruct_path(self, previous, start, end):
        # Remonte depuis end jusqu'à start
        path = []
        node = end

        while node is not None:
            path.append(node)
            node = previous[node]

        path.reverse()

        # Vérifie que le chemin commence bien au bon endroit
        if path[0] == start:
            return path
        return None

    def find_best_node_for_two_users(self, user1, user2, data):
        # 1. Meilleur nœud pour user1
        best_u1 = self.find_best_node_for_data(user1, data)

        # 2. Distances + prédécesseurs depuis ce nœud
        distances, previous = self.dijkstra_with_path(best_u1.id)

        # 3. Chemin entre best_u1 et user2
        path = self.reconstruct_path(previous, best_u1.id, f"U{user2.id}")

        if path is None:
            return None  # Aucun chemin trouvé

        # Distances depuis U1 et U2
        dist_u1 = self.dijkstra(f"U{user1.id}")
        dist_u2 = self.dijkstra(f"U{user2.id}")

        best_node = None
        best_cost = float('inf')

        # 4. On teste chaque nœud du chemin
        for node in path:
            if isinstance(node, int):  # On ignore U0, U1...
                cost = dist_u1[node] + dist_u2[node]

                if cost < best_cost:
                    best_cost = cost
                    best_node = node

        return best_node

    def show_all_data_stored(self):
        print("\n=== DONNÉES STOCKÉES PAR NŒUD ===")
        for node in self.nodes:
            data_ids = [data.id for data in node.liste_data_stocked]
            print(f"Nœud {node.id} : Données stockées {[f'D{data_id}' for data_id in data_ids]} | Capacité restante {node.memoryCapacity}")

    def show_all_data_per_user(self):
        print("\n=== DONNÉES REQUISES PAR UTILISATEUR ===")
        for user in self.users:
            print(f"Utilisateur {user.id} : Données requises {[f'D{data.id}({data.taille})' for data in user.liste_data]}")


    def place_all_data_mkp(self):
        # 1. Pré-calcul des distances utilisateur → nœud
        user_distances = {}
        for user in self.users:
            user_distances[user.id] = self.dijkstra(f"U{user.id}")

        # 2. Trier les données par taille décroissante (heuristique MKP)
        sorted_data = sorted(self.data, key=lambda d: d.taille, reverse=True)

        for data in sorted_data:
            # Trouver les utilisateurs qui demandent cette donnée
            users_for_data = [u for u in self.users if data.id in u.liste_data]

            best_node = None
            best_cost = float('inf')

            # 3. Tester chaque nœud
            for node in self.nodes:
                if node.memoryCapacity < data.taille:
                    continue  # pas assez de place

                # Calcul du coût total si la donnée est placée sur ce nœud
                total_cost = sum(user_distances[u.id][node.id] for u in users_for_data)

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_node = node

            # 4. Placer la donnée dans le meilleur nœud
            if best_node:
                best_node.liste_data_stocked.append(data)
                best_node.memoryCapacity -= data.taille
                print(f"Donnée {data.id} placée sur le nœud {best_node.id} (coût total = {best_cost})")
            else:
                print(f"Impossible de placer la donnée {data.id} (pas assez de mémoire)")