import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image as PilImage, ImageTk
import cv2
import heapq
class Graphe :
    def __init__(self):
        self.sommets = list()

    def ajout_sommet(self, val):
        self.sommets.append(Sommet(val))

    def ajout_arete(self, sommet1, sommet2, poids):
        self.sommets[sommet1].listeAdjacents.append(Arete(sommet1, sommet2, poids))

class Sommet :
    def __init__(self, val):
        self.sommet = val
        self.listeAdjacents = list()
        self.previous = None
        self.temps_de_parcours = float("inf")

class Arete :
    def __init__(self, sommet1, sommet2, poids) :
        self.depart = sommet1
        self.arrive = sommet2
        self.poids = poids

class Image:
    def __init__(self, image_path):
        self.path = image_path
        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        self.graphe = Graphe()


    def toGraphe(self):
        #ajout des pixels de notre image comme sommet du graphe
        height, width = self.image.shape
        for i in range(0, height):
            for j in range(0, width):
                val = self.image[i, j]
                self.graphe.ajout_sommet(val)

        print("Nommbre de sommets :", len(self.graphe.sommets))

        departs = []
        test = []

        #ajout des aretes
        for x in range(height):
            for y in range(width):
                depart = x*width + y
                departs.append(depart)
                if x > 0:
                    #on ajoute une arete vers le haut si ce n'est pas une premiere ligne
                    destination = (x-1)*width + y
                    poids = abs(int(self.graphe.sommets[destination].sommet)- int(self.graphe.sommets[depart].sommet))
                    self.graphe.ajout_arete(depart, destination, poids)
                if y > 0:
                    # on ajoute une arete vers la gauche si ce n'est pas une premeire colonne
                    destination = x*width + y-1
                    poids = abs(int(self.graphe.sommets[destination].sommet) - int(self.graphe.sommets[depart].sommet))
                    self.graphe.ajout_arete(depart, destination, poids)
                if x < height-1:
                    #on ajoute une arete vers le bas si ce n'est pas la derniere ligne
                    destination = (x+1)*width + y
                    poids = abs(int(self.graphe.sommets[destination].sommet) - int(self.graphe.sommets[depart].sommet))
                    self.graphe.ajout_arete(depart, destination, poids)
                if y < width-1:
                    #on ajoute une arete vers la droite si ce n'est pas la derniere colonnes
                    destination = x*width + y+1
                    poids = abs(int(self.graphe.sommets[destination].sommet) - int(self.graphe.sommets[depart].sommet))
                    self.graphe.ajout_arete(depart, destination, poids)

        #print(f"test = {len(test)}, {width*height - (width*2 + height*2 - 4)}")

        for sommet in self.graphe.sommets:
            if len(sommet.listeAdjacents) == 2:
                print(sommet.listeAdjacents)

        print(len(set(departs)))

    def affichagePath(self, sommets):
        #affiche le chemin le plus court
        height, width = self.image.shape  # Obtenir les dimensions de l'image
        pixels = []

        for sommet in sommets:
            pixels.append((sommet % width, sommet // width))  # Convertir sommets en coordonnées (x, y)

        print("La liste des sommets est :", sommets)
        print("La liste des pixels est :", pixels)

        # Créer une copie de l'image pour tracer dessus (en gris care en RGB plus de calculs)
        image_couleur = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        # Tracer une ligne rouge entre les pixels du chemin
        for i in range(1, len(pixels)):
            cv2.line(image_couleur, pixels[i - 1], pixels[i], (0, 0, 255), 1)


        #redimensionner l'image
        redim = cv2.resize(image_couleur, (340,500))

        # Afficher l'image avec la ligne rouge
        cv2.imshow("Chemin Dijkstra", redim)
        cv2.waitKey(0)  # Attendre une touche pour fermer la fenêtre
        cv2.destroyAllWindows()

    def dijkstra(self, debut, fin):
        #L'algorithme de Dijkstra optimisé avec une file de priorité
        self.graphe.sommets[debut].temps_de_parcours = 0
        file_priorite = [(0, debut)]  # (distance, sommet)
        visited = set()

        while file_priorite:
            # Extraire le sommet avec la plus petite distance
            temps_courant, min_val = heapq.heappop(file_priorite)

            if min_val in visited:
                continue
            visited.add(min_val)

            if min_val == fin:
                break  # On arrête dès qu'on atteint le sommet final

            # Parcourir les voisins
            for arete in self.graphe.sommets[min_val].listeAdjacents:
                voisin = arete.arrive
                nouveau_temps = temps_courant + arete.poids

                if nouveau_temps < self.graphe.sommets[voisin].temps_de_parcours:
                    self.graphe.sommets[voisin].temps_de_parcours = nouveau_temps
                    self.graphe.sommets[voisin].previous = min_val
                    heapq.heappush(file_priorite, (nouveau_temps, voisin))

        # Reconstruction du chemin
        chemin = []
        current = fin
        while current is not None:
            chemin.insert(0, current)
            current = self.graphe.sommets[current].previous

        return chemin

class Interface :
    def __init__(self, root):
        self.root = root
        self.root.title("Djikstra Path Finder")

        self.image_path_label = tk.Label(root, text="Chemin de l'image :")
        self.image_path_label.pack()
        self.image_path_entry = tk.Entry(root, width=50)
        self.image_path_entry.pack()
        self.image_path_button = tk.Button(root, text="Parcourir", command=self.load_image)
        self.image_path_button.pack()

        self.start_label = tk.Label(root, text="Sommet de départ :")
        self.start_label.pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack()

        self.end_label = tk.Label(root, text="Sommet de fin : \n(Pour tester plusieurs points, fermez l'image générée, puis modifiez les données avant de relancer le calcul.)")
        self.end_label.pack()
        self.end_entry = tk.Entry(root)
        self.end_entry.pack()

        self.calculate_button = tk.Button(root, text="Calculer le chemin", command=self.calculate_path)
        self.calculate_button.pack()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.original_image = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)
            self.display_image(file_path)

    def display_image(self, file_path):
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (340, 500))
        self.original_image = ImageTk.PhotoImage(PilImage.fromarray(image))
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.original_image)

    def calculate_path(self):
        start_node = self.start_entry.get()
        end_node = self.end_entry.get()
        image_path = self.image_path_entry.get()

        if not start_node or not end_node or not image_path:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        image_processor = Image(image_path)
        image_processor.toGraphe()
        chemin = image_processor.dijkstra(int(start_node), int(end_node))
        image_processor.affichagePath(chemin)



if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

