from DonneContext import DonneContext
from NetWorkContext import NetWorkContext
from NodeContext import NodeContext
from UserContext import UserContext
from ArcContext import ArcContext

def start():
    # -----------------------------------------
    # LOT DE TEST MIS À JOUR AVEC LONGUEURS UTILISATEUR‑NŒUD
    # -----------------------------------------
    appOn = True

    # 1. Créer les nœuds
    nodeA = NodeContext(id=0, memoryCapacity=100, liste_data_stocked=[], noeud_accessible=[1, 2])
    nodeB = NodeContext(id=1, memoryCapacity=80, liste_data_stocked=[], noeud_accessible=[0, 2])
    nodeC = NodeContext(id=2, memoryCapacity=120, liste_data_stocked=[], noeud_accessible=[0, 1])
    nodeD = NodeContext(id=3, memoryCapacity=50, liste_data_stocked=[], noeud_accessible=[2])

    nodes = [nodeA, nodeB, nodeC, nodeD]

    # 2. Créer les arcs entre les nœuds
    arcAB = ArcContext(id=0, node1=0, node2=1, longueur=5)
    arcAC = ArcContext(id=1, node1=0, node2=2, longueur=3)
    arcBC = ArcContext(id=2, node1=1, node2=2, longueur=2)
    arcCD = ArcContext(id=3, node1=2, node2=3, longueur=7)

    # 3. Créer les arcs entre les utilisateurs et leurs nœuds de départ
    #    (arcs virtuels)
    arcUser1 = ArcContext(id=100, node1="U0", node2=0, longueur=1)
    arcUser2 = ArcContext(id=101, node1="U1", node2=3, longueur=4)

    arcs = [arcAB, arcAC, arcBC, arcCD, arcUser1, arcUser2]

    # 5. Créer les objets de données
    data0 = DonneContext(id=0, taille=10)
    data1 = DonneContext(id=1, taille=20)
    data2 = DonneContext(id=2, taille=15)

    # 4. Créer les utilisateurs
    user1 = UserContext(id=0, liste_data=[data0, data1], node_accessible=0, arc_length_to_node=1)
    user2 = UserContext(id=1, liste_data=[data2], node_accessible=3, arc_length_to_node=4)

    users = [user1, user2]

    data_list = [data0, data1, data2]

    network = NetWorkContext(nodes=nodes, arcs=arcs, users=users, data=data_list)
    network.build_graph()

    while appOn:
        menuChoice = -1
        print("\n---Menu---")
        print("1. Afficher le réseau actuel")
        print("2. Ajouter une donnée pour un utilisateur")
        print("3. Afficher les détails du réseau")
        print("4. Ajouter une donnée pour deux utilisateurs")
        print("5. Afficher les données stockées sur chaque nœud")
        print("6. Afficher les données requises par chaque utilisateur")
        print("0. Quitter")
        menuChoice = int(input("Choisissez une option: "))

        if menuChoice == 1:
            network.print_graph()
        elif menuChoice == 2:
            # Exemple : ajouter une nouvelle donnée à l’utilisateur 1
            data_new = DonneContext(id=len(network.data), taille=int(input("Taille de la nouvelle donnée: ")))
            network.data.append(data_new)
            for user in users:
                print("Liste des utilisateurs :\n")
                print(f"User {user.id}: {user.liste_data}")
            user = int(input("Pour quel utilisateur ajouter la donnée? : "))
            network.add_data_on_user(users[user], data_new)
        elif menuChoice == 3:
            network.print_network_details()
        elif menuChoice == 4:
            # Exemple : ajouter une nouvelle donnée pour deux utilisateurs
            data_new = DonneContext(id=len(network.data), taille=int(input("Taille de la nouvelle donnée: ")))
            network.data.append(data_new)
            print("Liste des utilisateurs :\n")
            for user in users:
                print(f"User {user.id}: {user.liste_data}")
            user1 = int(input("Pour quel utilisateur ajouter la donnée? : "))
            user2 = int(input("Pour quel autre utilisateur ajouter la donnée? : "))
            network.add_data_for_two_users(users[user1], users[user2], data_new)
        elif menuChoice == 5:
            network.show_all_data_stored()
        elif menuChoice == 6:
            network.show_all_data_per_user()
        elif menuChoice == 0:
            appOn = False

    network.print_graph()


start()
