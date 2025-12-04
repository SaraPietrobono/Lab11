import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()



    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G.clear()
        lista_rifugi=DAO.leggi_rifugio(year)
        self.idMap={r.id: r for r in lista_rifugi}
        #prendo i nodi
        self.G.add_nodes_from(lista_rifugi)
        #creo gli archi
        lista_connessioni=DAO.leggi_connessione(year)
        for c in lista_connessioni:
            r1=self.idMap[c.id_rifugio1]
            r2=self.idMap[c.id_rifugio2]
            self.G.add_edge(r1, r2)


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        return list(self.G.nodes())


    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        return self.G.degree(node)



    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        return nx.number_connected_components(self.G)

    def get_reachable_bfs_tree(self,start):
        tree = nx.bfs_tree(self.G, start)
        return list(tree.nodes())[1:]
        # tolgo il nodo di partenza; perchè nel testo ci dice che il rifugio di partenza non deve comparire nella lista dei risultati
    def get_reachable_recursive(self,start):
        visited = set()
        def dfs(u):
            for v in self.G.neighbors(u):
                if v not in visited:
                    visited.add(v)
                    dfs(v)
        dfs(start)
        visited.discard(start) #serve per rimuovere il nodo di partenza dall'insieme dei nodi visitati
        return list(visited)




    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_recursive(start)
        #il risultato che ci restituiscono le due funzioni è lo stesso; portano allo stesso risultato

        return a



