import networkx as nx
import matplotlib.pyplot as plt
class classNode:
    def __init__(self):
        self.children = [None] * 26  # A node can have up to 26 children (one for each letter)
        self.is_end = False  # Flag to indicate the end of a class code
        self.vector = None  # To store the vector at the end of a class code

    def set_vector(self, vector):
        self.vector = vector
        self.is_end = True

    def get_child_index(self, char):
        return ord(char.upper()) - ord('A')  # Convert character to index (0-25)

    def has_child(self, char):
        return self.children[self.get_child_index(char)] is not None

    def get_child(self, char):
        return self.children[self.get_child_index(char)]

    def add_child(self, char):
        self.children[self.get_child_index(char)] = classNode()


class classTree:
    def __init__(self):
        self.root = classNode()

    def insert(self, class_code, vector):
        node = self.root
        for char in class_code:
            if not node.has_child(char):
                node.add_child(char)
            node = node.get_child(char)
        node.set_vector(vector)  # Set the vector at the final node

    def get_vector(self, class_code):
        node = self.root
        for char in class_code:
            if not node.has_child(char):
                return None  # Class code not found
            node = node.get_child(char)
        return node.vector if node.is_end else None  # Return the vector if this is the end of a class code
    
    def displayPreReqGraph(self, course, G=None, parent=None, draw=False):
        if G is None:
            G = nx.DiGraph()

        prereqs = self.get_vector(course)

        # Add the course as a node to the graph. If it has a parent, add an edge.
        if course not in G:
            G.add_node(course)
        if parent is not None:
            G.add_edge(parent, course)

        if not prereqs or prereqs == [None]:
            if draw:
                self.draw_graph(G)
            return G

        for prereq in prereqs:
            if prereq is not None:
                # Recursively add the current prerequisite as a node and connect it
                self.displayPreReqGraph(prereq, G, course)

        if draw:
            self.draw_graph(G)

        return G

    def draw_graph(self, G):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)  # or any other layout you prefer
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='black', node_size=2000, font_size=10)
        plt.title("Course Prerequisite Graph")
        plt.show()
    
    