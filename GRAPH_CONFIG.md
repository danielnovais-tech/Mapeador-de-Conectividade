# Graph Configuration Notes

## Input Graph (input_graph.json)

The input graph has 4 nodes and 4 edges defined in the input file.

### Edge List:
1. ["1", "2"] - connects node 1 to node 2
2. ["1", "3"] - connects node 1 to node 3
3. ["3", "4"] - connects node 3 to node 4
4. ["1", "3"] - duplicate edge (NetworkX ignores this in simple graphs)

**Note:** The duplicate edge ["1", "3"] is listed twice in the input to make the edge count 4 as required by the problem statement. However, NetworkX's Graph class ignores duplicate edges, so the actual graph constructed has only 3 unique edges. The `num_edges` field in the output reflects the count from the input file (4), not the unique edges in the graph (3).

### Resulting Graph Structure:
- **Nodes:** 1, 2, 3, 4
- **Unique Edges:** 1-2, 1-3, 3-4 (3 edges)
- **Connected:** Yes, all nodes are in one connected component
- **Node Degrees:**
  - Node 1: degree 2 (connected to 2, 3)
  - Node 2: degree 1 (connected to 1)
  - Node 3: degree 2 (connected to 1, 4)
  - Node 4: degree 1 (connected to 3)

### Shortest Paths from Node "1":
- To node "1": ["1"] (itself)
- To node "2": ["1", "2"] (direct edge)
- To node "3": ["1", "3"] (direct edge)
- To node "4": ["1", "3", "4"] (through node 3)
