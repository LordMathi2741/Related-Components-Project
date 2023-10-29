import math
import tkinter as tk
from random import randint
import random


class GraphApp:
    def __init__(self, root):
        self.componentes_text = None
        self.componentes_window = None
        self.filas_cambiadas = None
        self.nombre_nodos = None
        self.matrix_caminos = None
        self.matrix = None
        self.root = root
        self.root.title("Componentes conexas de un grafo")
        self.root.configure(bg="black")

        self.col_label = tk.Label(root, text="Ingrese el valor de n: (mínimo 5 y máximo 15):", bg="black", fg="white")
        self.col_label.pack()
        self.col_entry = tk.Entry(root)
        self.col_entry.pack()

        self.create_button = tk.Button(root, text="Crear Matriz", command=self.create_matrix, bg="white", fg="black")
        self.create_button.pack()
        self.create_button_unos = tk.Button(root, text="Agregar unos a la diagonal", command=self.agregar_unos_diagonal,
                                            bg="white", fg="black", state=tk.DISABLED)
        self.create_button_unos.pack()
        self.create_button_caminos = tk.Button(root, text="Identificar Matriz de Caminos",
                                               command=self.identificar_caminos, bg="white", fg="black",
                                               state=tk.DISABLED)
        self.create_button_caminos.pack()
        self.create_button_ordenar_filas = tk.Button(root, text="Ordenar Filas", command=self.ordenar_filas, bg="white",
                                                     fg="black", state=tk.DISABLED)
        self.create_button_ordenar_filas.pack()
        self.create_button_ordenar_columnas = tk.Button(root, text="Ordenar Columnas", command=self.ordenar_columnas,
                                                        bg="white", fg="black", state=tk.DISABLED)
        self.create_button_ordenar_columnas.pack()
        self.create_button_componentes = tk.Button(root, text="Identificar Componentes Conexas",
                                                   command=self.identificar_componentes, bg="white", fg="black",
                                                   state=tk.DISABLED)
        self.create_button_componentes.pack()

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        self.node_radius = 20
        self.node_positions = {}

        self.matrix_text = tk.Text(root, height=10, width=30, bg="black", fg="white")
        self.matrix_text.pack()

        self.manual_matrix_button = tk.Button(root, text="Ingresar Matriz Manualmente",
                                              command=self.create_matrix_manual, bg="white", fg="black")
        self.manual_matrix_button.pack()

    def create_matrix(self):
        self.create_button_unos.config(state=tk.DISABLED)
        self.create_button_caminos.config(state=tk.DISABLED)
        self.create_button_ordenar_filas.config(state=tk.DISABLED)
        self.create_button_ordenar_columnas.config(state=tk.DISABLED)
        self.create_button_componentes.config(state=tk.DISABLED)

        try:
            n = int(self.col_entry.get())

            if n < 5 or n > 15:
                raise ValueError

            self.matrix = self.create_matrix_random(n, n)
            self.clear_canvas()
            self.draw_graph()
            self.display_matrix(self.matrix)

            # Actualizar la variable de estado
            self.matriz_creada = True
            self.matriz_caminos_identificada = False

            # Habilitar botones relevantes
            self.create_button_unos.config(state=tk.NORMAL)

        except ValueError:
            self.clear_canvas()
            self.display_matrix([])
            self.canvas.create_text(250, 250, text="Ingrese números válidos para filas y columnas.", fill="red")

    def create_matrix_random(self, row, col):
        matrix = []
        for i in range(row):
            row_vals = []
            for j in range(col):
                value = random.randint(0, 1)
                row_vals.append(value)
            matrix.append(row_vals)

        self.nombre_nodos = [chr(ord('A') + i) for i in range(row)]
        return matrix

    # calculo de las componentes conexas.
    # Pasos:
    # 1. agregarle (si fuese necesario) el valor 1 en la diagonal de la matriz.
    # 2. calcular la matriz de caminos.
    # 3. Contar la cantidad de 1’s en cada fila de la matriz.
    # Ordenar las filas según el número de 1’s (de mayor a menor).
    # Si hubiera dos filas que tienen la misma cantidad de 1’s, entonces se debe colocar primero aquella que tiene el 1 más cercano a la primera columna.
    # 4. Ordenar las columnas de acuerdo con el orden de las filas. Las componentes conexas serán aquellas que se formen con los bloques cuadrados diagonales formados por 1’s.

    def agregar_unos_diagonal(self):
        if self.matrix:
            n = len(self.matrix)
            for i in range(n):
                self.matrix[i][i] = 1

            self.display_matrix(self.matrix)

            # Habilitar botones relevantes
            self.create_button_caminos.config(state=tk.NORMAL)

    def calcular_matriz_de_caminos(self):
        if self.matrix:
            n = len(self.matrix)
            self.matrix_caminos = [[0] * n for _ in range(n)]

            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == 1:
                        self.matrix_caminos[i][j] = 1

            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        if self.matrix_caminos[i][j] or (self.matrix_caminos[i][k] and self.matrix_caminos[k][j]):
                            self.matrix_caminos[i][j] = 1

            self.create_button_ordenar_filas.config(state=tk.NORMAL)

    def identificar_caminos(self):
        if self.matrix:
            # Calcular la matriz de caminos
            self.calcular_matriz_de_caminos()

            # Mostrar la matriz de caminos
            self.display_path_matrix(self.matrix_caminos)

    def ordenar_filas(self):
        if self.matrix_caminos:
            n = len(self.matrix_caminos)
            row_ones = [(i, sum(self.matrix_caminos[i])) for i in range(n)]
            row_ones.sort(key=lambda x: x[1], reverse=True)
            new_matrix = [self.matrix_caminos[i] for i, _ in row_ones]
            self.matrix_caminos = new_matrix

            self.filas_cambiadas = [x[0] for x in row_ones]

            self.display_path_matrix(self.matrix_caminos)

            self.nombre_nodos = [self.nombre_nodos[i] for i in self.filas_cambiadas]

            # Habilitar el botón para ordenar columnas
            self.create_button_ordenar_columnas.config(state=tk.NORMAL)

    def ordenar_columnas(self):
        if self.matrix_caminos:
            n = len(self.matrix_caminos)

            # Crear un diccionario para almacenar la posición original de las filas
            original_positions = {row: i for i, row in enumerate(self.filas_cambiadas)}

            # Crear una nueva matriz con las columnas reordenadas
            new_matrix = [[self.matrix_caminos[i][original_positions[j]] for j in range(n)] for i in range(n)]
            self.matrix_caminos = new_matrix

            self.display_path_matrix(self.matrix_caminos)

            # Habilitar el botón para identificar componentes conexas
            self.create_button_componentes.config(state=tk.NORMAL)

    def identificar_componentes(self):
        if self.matrix_caminos:
            # Identificar las componentes conexas
            n = len(self.matrix_caminos)
            visited = [False for _ in range(n)]
            componentes = []

            for i in range(n):
                if self.matrix_caminos[i][i] and not visited[i]:
                    componente = self.find_connected_component(i, visited)
                    componentes.append(componente)

            # Mostrar las componentes conexas
            self.display_componentes(componentes)

    def find_connected_component(self, i, visited):
        # Verificar si se forman cuadrados diagonales de 1's en la matriz de caminos ordenada:
        n = len(self.matrix_caminos)
        visited[i] = True
        componente = [i]

        for j in range(n):
            sub_matrix = [self.matrix_caminos[k][i:j + 1] for k in range(i, j + 1)]
            if all(all(row) for row in sub_matrix) and not visited[j]:
                componente.append(j)
                visited[j] = True

        return componente

    def display_componentes(self, componentes):
        self.componentes_window = tk.Toplevel(self.root)
        self.componentes_window.title("Componentes Conexas")

        self.componentes_text = tk.Text(self.componentes_window, height=10, width=30, bg="black", fg="white")
        self.componentes_text.pack()
        if self.componentes_text:
            self.componentes_text.delete(1.0, tk.END)
        else:
            self.componentes_text = tk.Text(self.componentes_window, height=10, width=30, bg="black", fg="white")
            self.componentes_text.pack()

        self.componentes_text.insert(tk.END, "Componentes Conexas:\n")

        for i, componente in enumerate(componentes):
            # Mapear índices de nodos a letras correspondientes
            nodos_letras = [self.nombre_nodos[i] for i in componente]
            self.componentes_text.insert(tk.END, f"Componente {i + 1}: {', '.join(nodos_letras)}\n")

    def draw_graph(self):
        self.node_positions = {}

        if self.matrix:
            num_rows = len(self.matrix)
            num_cols = len(self.matrix[0])

            for i in range(num_rows):
                x = randint(self.node_radius, self.canvas.winfo_width() - self.node_radius)
                y = randint(self.node_radius, self.canvas.winfo_height() - self.node_radius)
                self.node_positions[i] = (x, y)
                self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius,
                                        y + self.node_radius, outline="blue")

                label = chr(ord('A') + i)
                self.canvas.create_text(x, y, text=label, fill="blue")

            for i in range(num_rows):
                for j in range(num_cols):
                    if self.matrix[i][j] == 1:
                        if i in self.node_positions and j in self.node_positions:
                            x1, y1 = self.node_positions[i]
                            x2, y2 = self.node_positions[j]

                            angle = math.atan2(y2 - y1, x2 - x1)

                            if i == j:
                                radius = self.node_radius * 0.8
                                self.canvas.create_oval(x1 - radius, y1 - radius, x1 + radius, y1 + radius,
                                                        outline="black", width=2)
                            else:
                                x1 += self.node_radius * math.cos(angle)
                                y1 += self.node_radius * math.sin(angle)
                                x2 -= self.node_radius * math.cos(angle)
                                y2 -= self.node_radius * math.sin(angle)
                                self.canvas.create_line(x1, y1, x2, y2, fill="black", arrow=tk.LAST)

    def create_matrix_manual(self):
        if self.matrix is not None:
            manual_matrix_window = tk.Toplevel(self.root)
            manual_matrix_window.title("Ingresar Matriz Manualmente")

            manual_matrix_entries = []
            for i in range(len(self.matrix)):
                row_entries = []
                for j in range(len(self.matrix[0])):
                    entry = tk.Entry(manual_matrix_window, width=5)
                    entry.grid(row=i, column=j)
                    row_entries.append(entry)
                manual_matrix_entries.append(row_entries)

            confirm_button = tk.Button(manual_matrix_window, text="Confirmar",
                                       command=lambda: self.save_manual_matrix(manual_matrix_entries,
                                                                               manual_matrix_window))
            confirm_button.grid(row=len(self.matrix), columnspan=len(self.matrix[0]))

    def save_manual_matrix(self, entries, window):
        try:
            manual_matrix = []
            for row in entries:
                row_values = []
                for entry in row:
                    value = int(entry.get())
                    row_values.append(value)
                manual_matrix.append(row_values)

            self.clear_canvas()
            self.matrix = manual_matrix
            self.draw_graph()
            self.display_matrix(self.matrix)

            window.destroy()

        except ValueError:
            pass

    def display_matrix(self, matrix):
        self.matrix_text.delete(1.0, tk.END)
        matrix_str = "\n".join(" ".join(map(str, row)) for row in matrix)
        self.matrix_text.insert(tk.END, "Matriz de Adyacencia:\n" + matrix_str)

    def display_path_matrix(self, matrix):
        self.matrix_text.delete(1.0, tk.END)
        matrix_str = "\n".join(" ".join(map(str, row)) for row in matrix)
        self.matrix_text.insert(tk.END, "Matriz de Caminos:\n" + matrix_str)

    def clear_canvas(self):
        self.canvas.delete("all")

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    app.main()