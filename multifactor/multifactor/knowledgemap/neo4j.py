from py2neo import Graph,Node,Relationship



from queue    import * 

a = Node('Person', name='Alice')
b = Node('Person', name='Bob')
r = Relationship(a, 'KNOWS', b)
print(a, b, r)



test_graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="neo4j"
)
test_node_1 = Node(label = "Person",name = "test_node_1")
test_node_2 = Node(label = "Person",name = "test_node_2")
test_graph.create(test_node_1)
test_graph.create(test_node_2)
