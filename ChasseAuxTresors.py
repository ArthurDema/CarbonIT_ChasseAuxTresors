import sys

class Aventurier:
    def __init__(self, name, posX, posY, orientation, sequence_moves):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.orientation = orientation
        self.remaining_moves = len(sequence_moves)
        self.moves = list(sequence_moves)

    def update_remaining_moves(self) :
        self.remaining_moves -= 1

    def is_orientation(self, move):
        if move in ["G", "D"]:
            return True
        else :
            return False
        
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
    
    def get_current_move(self):
        return self.moves[len(self.moves) - self.remaining_moves]
    
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

    def update_position(self, position):
        self.posX = position[0]
        self.posY = position[1]

class Tresor:
    def __init__(self, posX, posY, nbTresors):
        self.posX = posX
        self.posY = posY
        self.nbTresors = nbTresors

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

    def add_mountain(self, mountain):
        self.mountains.append(mountain) 

    def add_tresor(self, tresor):
        self.tresors.append(tresor)

    def add_aventurier(self, aventurier):
        self.aventuriers.append(aventurier)
    
    def is_mountain(self, position):
        for mountain in self.mountains:
            if position[0] == mountain.posX and position[1] == mountain.posY:
                return True
        return False
    def is_aventurier(self, position):
        for aventurier in self.aventuriers:
            if position[0] == aventurier.posX and position[1] == aventurier.posY:
                return True
        return False
    
    def is_in_bounds(self, position):
        if position[0] < 0 or position[0] > self.dimensionX - 1:
            return False
        if position[1] < 0 or position[1] > self.dimensionY - 1:
            return False
        return True

    def display_map(self):
        for j in range(self.dimensionY):
            for i in range(self.dimensionX):
                if self.is_mountain((i, j)):
                    print("M   ", end="")
                elif self.is_aventurier((i,j)):
                    print("A   ",end="")
                else:
                    print(".   ",end="")
            print("\n")  
        print("-------------")

def possible_movement(map, pos):
    if not map.is_in_bounds(pos) or map.is_mountain(pos):
        return False
    else :
        return True

def tour_par_tour(map):
    aventurier_peut_toujours_jouer = len(map.aventuriers)
    while aventurier_peut_toujours_jouer > 0:
        map.display_map()
        for aventurier in map.aventuriers:
            if aventurier.remaining_moves > 0:
                move_to_do = aventurier.get_current_move()
                if aventurier.is_orientation(move_to_do):
                    aventurier.update_orientation(move_to_do)
                else:
                    if possible_movement(map, aventurier.next_move()):
                        aventurier.update_position(aventurier.next_move())
                aventurier.update_remaining_moves()
            else:
                aventurier_peut_toujours_jouer -= 1
        


#Faire des tests sur le positionnement de départ des éléments

#S'assure que l'argument fourni n'est pas vide
def get_valid_argument():
    while True:
        if len(sys.argv) < 2 or not sys.argv[1].strip():
            print("Erreur : L'argument ne peut pas être une string vide")
            sys.exit(1)
        else:
            return sys.argv[1]
        

def create_map(filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                result1 = line.replace(" ", "")
                result1 = result1.replace("\u200b", "")
                result1 = result1.replace("\n", "")
                result2 = result1.split("-")
                match result2[0]:
                    case "C":
                        map_game = Map(int(result2[1]), int(result2[2]))
                    case "M":
                        mountain = Mountain(int(result2[1]), int(result2[2]))
                        map_game.add_mountain(mountain)
                    case "T":
                        tresor = Tresor(int(result2[1]), int(result2[2]), int(result2[3]))
                        map_game.add_tresor(tresor)
                    case "A":
                        aventurier = Aventurier(result2[1], int(result2[2]), int(result2[3]), result2[4], result2[5])
                        map_game.add_aventurier(aventurier)
                    case _:
                        pass
    except FileNotFoundError:
        print(f"Erreur: File '{filename} not found.")
    except Exception as e:
        print(f"Une erreur : {str(e)}")
    return map_game


# Main
def main():
    file_path = get_valid_argument()
    map = create_map(file_path)
    tour_par_tour(map)

if __name__ == "__main__":
    main()