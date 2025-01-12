import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allAirports = DAO.getAllAirports()
        self._idMap ={} #vedi DAO
        for a in self._allAirports:
            self._idMap[a.ID]=a
        self._grafo = nx.Graph() #grafo non orientato


    def buildGraph(self, nMin):
        self._nodi = DAO.getAllNodes(nMin, self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdgesV1()
        #self._addEdgesV2()

    def _addEdgesV1(self):
        allConnessioni = DAO.getAllEdgesV1(self._idMap)
        for c in allConnessioni:
            v0 = c.VO
            v1 = c.V1
            peso = c.N

            if v0 in self._grafo and v1 in self._grafo:
                if self._grafo.has_edge(v0,v1):
                    self._grafo[v0][v1]["weight"] += peso
                else:
                    self._grafo.add_edge(v0, v1, weight=peso)

    def addEdgesV2(self):
        allConnessioni = DAO.getAllEdgesV2(self._idMap)
        for c in allConnessioni:
            v0 = c.v0
            v1 = c.v1
            peso = c.N
            if v0 in self._grafo and v1 in self._grafo:
                self._grafo.add_edge(v0, v1, weight=peso)

    def getSortedVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))
        viciniTuple.sort(key=lambda x : x[1], reverse=True) #in ordine decrescente di voli
        return viciniTuple

    def esistePercorso(self, v0, v1):
        connessa = nx.node_connected_component(self._grafo, v0) #restituisce la componente connessa del grafo a partire da v0
        if v1 in connessa:
            return True
        else:
            return False

    def trovaCamminoDijkstra(self, v0, v1):
        return nx.dijkstra_path(self._grafo, v0, v1)
    #mi da cammino ottimo, che minimizza il peso degli archi

    #garantisce il minor numero di archi
    #(ma non cammino ottimo, archi possono avere peso maggiore)
    def trovaCamminoBFS(self, v0, v1):
        tree = nx.bfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di visita BFS")
        path = [v1]
        while path[-1] != v0:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse() #perchè quando costruisco albero vado dalla foglia alla radice, da targhet a source allora devo fare reverse
        return path

    #è il più lungo
    def trovaCamminoDFS(self, v0, v1):
        tree = nx.dfs_tree(self._grafo, v0)
        if v1 in tree:
            print(f"{v1} è presente nell'albero di visita BFS")
        path = [v1]
        while path[-1] != v0:
            path.append(list(tree.predecessors(path[-1]))[0])
        path.reverse()
        return path

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getAllNodes(self):
        return self._nodi

    def printGraphDetails(self):
        print(f"Il grafo ha {len(self._grafo.nodes)} nodi")
        print(f"Il grafo ha {len(self._grafo.edges)} archi")

