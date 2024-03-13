import sys
import os

class Aventurier:
    def __init__(self, name, posX, posY, orientation, sequence_moves):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.orientation = orientation
        self.remaining_moves = len(sequence_moves)
        self.moves = list(sequence_moves)
        self.tresors = 0

    #Met à jour le nombre de coup restant de l'aventurier
    def update_remaining_moves(self) :
        self.remaining_moves -= 1

    #Retourne Vrai si le mouvement transmis est un mouvement d'orientation - Retourne Faux sinon
    def is_orientation(self, move):
        if move in ["G", "D"]:
            return True
        else :
            return False

    #Met à jour l'orientation de l'aventurier en fonction du mouvement d'orientation et de l'orientation cardianale de l'aventurier   
    def update_orientation(self, move):
        match self.orientation:
            case "S":
                if move == "D":
                    self.orientation = "O"
                if move == "G":
                    self.orientation = "E"
            case "N":
                if move == "D":
                    self.orientation = "E"
                if move == "G":
                    self.orientation = "O"
            case "O":
                if move == "D":
                    self.orientation = "N"
                if move == "G":
                    self.orientation = "S"
            case "E":
                if move == "D":
                    self.orientation = "S"
                if move == "G":
                    self.orientation = "N"
    
    #Retourne le mouvement à exécuter de l'aventurier à partir de son nombre de coups restants
    def get_current_move(self):
        return self.moves[len(self.moves) - self.remaining_moves]
    
    #Retourne la position supposée de l'aventurier en fonction de l'orientation cardinale de l'aventurier
    def next_move(self):
        next_posX = 0
        next_posY = 0
        match self.orientation:
            case "N":
                next_posY -= 1
            case "S":
                next_posY += 1
            case "O":
                next_posX -= 1 
            case "E":
                next_posX += 1
        return next_posX + self.posX, next_posY + self.posY

    #Met à jour la position de l'aventurier en fonction du tuple de positions transmis
    def update_position(self, position):
        self.posX = position[0]
        self.posY = position[1]
    
    #Met à jour le nombre de trésors de l'aventurier
    def update_tresors(self):
        self.tresors += 1

class Tresor:
    def __init__(self, posX, posY, nb_tresors):
        self.posX = posX
        self.posY = posY
        self.nb_tresors = nb_tresors
    
    #Met à jour le nombre de trésors de l'instance trésors
    def update_nb_tresors(self):
        if self.nb_tresors > 0:
            self.nb_tresors -= 1

class Mountain:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY

class Map:
    def __init__(self, dimensionX, dimensionY):
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY
        self.mountains = []
        self.tresors = []
        self.aventuriers = []

    #Ajoute une montagne à la liste de montagnes de la carte
    def add_mountain(self, mountain):
        if self.is_in_bounds((mountain.posX, mountain.posY)):
            self.mountains.append(mountain)
            
    #Ajoute un trésor à la liste de trésors de la carte
    def add_tresor(self, tresor):
        if self.is_in_bounds((tresor.posX, tresor.posY)):
            self.tresors.append(tresor)

    #Ajoute un aventurier à la liste d'aventuriers de la carte
    def add_aventurier(self, aventurier):
        if self.is_in_bounds((aventurier.posX, aventurier.posY)):
            self.aventuriers.append(aventurier)
    
    #Retourne Vrai si le tuple de positions transmis correspond à une montagne - Retourne Faux sinon
    def is_mountain(self, position):
        for mountain in self.mountains:
            if position[0] == mountain.posX and position[1] == mountain.posY:
                return True
        return False      

    #Retourne Vrai si le tuple de positions transmis correspond à un aventurier - Retourne Faux sinon
    def is_aventurier(self, position):
        for aventurier in self.aventuriers:
            if position[0] == aventurier.posX and position[1] == aventurier.posY:
                return True
        return False
    
    #Retourne Vrai si le tuple de positions transmis correspond à un trésor - Retourne Faux
    def is_tresor(self, position):
        for tresor in self.tresors:
            if position[0] == tresor.posX and position[1] == tresor.posY:
                return True
        return False
    
    #Met à jour le nombre de trésors d'un trésor identifié grâce à sa position - Supprime le trésor de la liste des trésors si son compte de trésors est égal à 0
    def update_tresors(self, position):
        for tresor_to_find in self.tresors:
            if position[0] == tresor_to_find.posX and position[1] == tresor_to_find.posY:
                tresor_to_find.update_nb_tresors()
            if tresor_to_find.nb_tresors == 0:
                self.tresors.remove(tresor_to_find)

    #Retourne le nombre de trésors d'un trésor en fonction de sa position
    def nb_tresors_from_pos(self, position):
        for tresor in self.tresors:
            if position[0] == tresor.posX and position[1] == tresor.posY:
                return tresor.nb_tresors
    
    #Retourne le nom de l'aventurier en fonction de sa position
    def aventurier_name_from_pos(self, position):
        for aventurier in self.aventuriers:
            if position[0] == aventurier.posX and position[1] == aventurier.posY:
                return aventurier.name

    #Retourne Vrai si la position transmise est dans les limites de la carte - Retourne Faux sinon    
    def is_in_bounds(self, position):
        if position[0] < 0 or position[0] > self.dimensionX - 1:
            return False
        if position[1] < 0 or position[1] > self.dimensionY - 1:
            return False
        return True

    #Affiche la carte, les montagnes, les aventuriers ainsi que les trésors
    def display_map(self):
        #Estime le texte à afficher le plus long pour adapter la réprésentation des colonnes du jeu
        longest_value_to_print = 0
        for aventurier in self.aventuriers:
            if len(aventurier.name) > longest_value_to_print:
                longest_value_to_print = len(aventurier.name)
        #Ajout de 5 pour l'esthétique aérée
        longest_value_to_print += 5

        #Affiche pour chaque position i,j l'élément du jeu correspondant
        for j in range(self.dimensionY):
            for i in range(self.dimensionX):
                if self.is_mountain((i, j)):
                    print("M" + " " * longest_value_to_print, end="")
                elif self.is_aventurier((i,j)):
                    print(f"A({self.aventurier_name_from_pos((i,j))})" + " " * (longest_value_to_print - 2 - len(self.aventurier_name_from_pos((i,j)))), end="")
                elif self.is_tresor((i, j)):
                    print(f"T({self.nb_tresors_from_pos((i,j))})" + " " * (longest_value_to_print - 3), end="")
                else:
                    print("." + " " * (longest_value_to_print), end="")
            print("\n")  
        print("-" * self.dimensionX * longest_value_to_print)

    #Retourne dans un fichier filename_output.txt, le résultat final du jeu
    def write_output(self, filename):
        output_name = filename.replace(".txt", "_output.txt")
        if os.path.exists(output_name):
            os.remove(output_name)
        f = open(output_name, "a")
        f.write(f"C - {self.dimensionX} - {self.dimensionY}\n")
        for moutain in self.mountains:
            f.write(f"M - {moutain.posX} - {moutain.posY}\n")
        for tresor in self.tresors:
            f.write(f"T - {tresor.posX} - {tresor.posY} - {tresor.nb_tresors}\n")
        for aventurier in self.aventuriers:
            f.write(f"A - {aventurier.name} - {aventurier.posX} - {aventurier.posY} - {aventurier.orientation} - {aventurier.tresors}\n")
        f.close()

#Retourne Vrai si la position transmise n'est ni une montagne ni un aventurier et qu'elle est bien dans les limites de la carte - Retourne Faux sinon
def possible_movement(map, position):
    if not map.is_in_bounds(position) or map.is_mountain(position) or map.is_aventurier(position):
        return False
    else :
        return True

#Parcours la liste d'aventurier et les fait jouer tour à tour
def tour_par_tour(map):
    #Condition d'arrêt du jeu : Lorsqu'aventurier_peut_toujours_jouer est à 0, le tout par tour s'arrête
    #Initialisé au nombre de joueur (Considérant que tous les joueurs ont au moins un coup à jouer)
    aventurier_peut_toujours_jouer = len(map.aventuriers)

    #Affiche l'état de la carte au stage 0
    map.display_map()
    while aventurier_peut_toujours_jouer > 0:
        #Pour chaque joueur dans la liste des aventuriers
        for aventurier in map.aventuriers:
            if aventurier.remaining_moves > 0:
                #Récupère le mouvement à faire pour l'aventurier
                move_to_do = aventurier.get_current_move()
                #Vérification du type de mouvement
                #Vérification si le mouvement est un changement d'orientation
                if aventurier.is_orientation(move_to_do):
                    #Met à jour l'orientation de l'aventurier
                    aventurier.update_orientation(move_to_do)
                #Sinon le mouvement est un mouvement "Avancer"
                else:
                    #Vérication de la possibilité d'exécuter le mouvement
                    if possible_movement(map, aventurier.next_move()):
                        #Met à jour la position de l'aventurier
                        aventurier.update_position(aventurier.next_move())
                        #Vérifie que la position de l'aventurier est une position de trésor
                        if map.is_tresor((aventurier.posX, aventurier.posY)):
                            #Met à jour le trésor dans la carte puisque qu'un trésor à été récupéré par l'aventurier
                            map.update_tresors((aventurier.posX, aventurier.posY))
                            #Met à jour la liste de trésors de l'aventurier
                            aventurier.update_tresors()
                aventurier.update_remaining_moves()
                #Vérifie si le nombre de mouvement restant de l'aventurier est nul
                if aventurier.remaining_moves == 0:
                    #Met à jour le nombre d'aventurier pouvant jouer au prochain tour
                    aventurier_peut_toujours_jouer -= 1
        map.display_map()


#Faire des tests sur le positionnement de départ des éléments

#S'assure que l'argument fourni n'est pas vide
def get_valid_argument():
    while True:
        if len(sys.argv) < 2 or not sys.argv[1].strip():
            print("Erreur : L'argument ne peut pas être une string vide")
            sys.exit(1)
        else:
            return sys.argv[1]
        
#Constitue la carte de jeu à partir du ficher texte transmis
def create_map(filename):
    try:
        with open(filename, "r") as file:
            mountains, tresors, aventuriers = [], [], []
            map_init = None
            is_map_dimension = False
            for line in file:
                #Remplace les caractères spéciaux trouvés dans le fichier
                result1 = line.replace(" ", "")
                result1 = result1.replace("\u200b", "")
                result1 = result1.replace("\n", "")
                result2 = result1.split("-")
                #Pour chaque ligne, ajoute l'élément correspondant à la carte de jeu
                match result2[0]:
                    case "C":
                        if (int(result2[1]), int(result2[2])) > (0,0): 
                            map_init = (int(result2[1]), int(result2[2]))
                            is_map_dimension = True
                        else:
                            raise Exception("La carte ne peut pas être de taille 0")
                    case "M":
                        mountains.append((int(result2[1]), int(result2[2])))
                    case "T":
                        tresors.append((int(result2[1]), int(result2[2]), int(result2[3])))
                    case "A":
                        aventuriers.append((result2[1], int(result2[2]), int(result2[3]), result2[4], result2[5]))
                    case _:
                        pass
            if is_map_dimension:
                map_game = Map(map_init[0],map_init[1])
                for element in mountains :
                    map_game.add_mountain(Mountain(*element))
                for element in tresors :
                    map_game.add_tresor(Tresor(*element))
                for element in aventuriers :
                    map_game.add_aventurier(Aventurier(*element))

        return map_game      
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{filename} est introuvable.")
    except Exception as e:
        print(f"Une erreur : {str(e)}")
        sys.exit(1)
    
    

# Main
def main():
    file_path = get_valid_argument()

    map = create_map(file_path)

    tour_par_tour(map)
    map.write_output(file_path)

if __name__ == "__main__":
    main()