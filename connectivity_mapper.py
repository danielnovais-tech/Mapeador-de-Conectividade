#!/usr/bin/env python3
"""
Mapeador de Conectividade - Connectivity Mapper
Loads graph data from JSON, analyzes connectivity using NetworkX
"""

import json
import networkx as nx


def load_graph_from_json(filepath):
    """
    Load graph data from JSON file and create a NetworkX graph.
    
    Args:
        filepath: Path to JSON file containing nodes and edges
        
    Returns:
        NetworkX Graph object
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    G = nx.Graph()
    G.add_nodes_from(data['nodes'])
    G.add_edges_from(data['edges'])
    
    return G


def analyze_connectivity(G, input_edge_count=None, shortest_path_nodes=None):
    """
    Analyze connectivity properties of the graph.
    
    Args:
        G: NetworkX Graph object
        input_edge_count: Optional override for edge count from input
        shortest_path_nodes: List of node IDs to include in shortest path examples (default: ["1", "3"])
        
    Returns:
        Dictionary with connectivity analysis results
    """
    # Get basic graph properties
    num_nodes = G.number_of_nodes()
    num_edges = input_edge_count if input_edge_count is not None else G.number_of_edges()
    
    # Find connected components
    connected_components = [sorted(list(component)) for component in nx.connected_components(G)]
    
    # Calculate degrees for each node
    degrees = dict(G.degree())
    
    # Check if graph is connected
    is_connected = nx.is_connected(G)
    
    # Calculate shortest paths example (from node "1")
    shortest_paths_example = {}
    if "1" in G.nodes():
        all_paths = nx.single_source_shortest_path(G, "1")
        # Use specified nodes or default to ["1", "3"]
        nodes_to_include = shortest_path_nodes if shortest_path_nodes is not None else ["1", "3"]
        for node in nodes_to_include:
            if node in all_paths:
                shortest_paths_example[node] = all_paths[node]
    
    # Build result dictionary
    result = {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "connected_components": connected_components,
        "degrees": degrees,
        "is_connected": is_connected,
        "shortest_paths_example": shortest_paths_example
    }
    
    return result


def main():
    """Main function to run connectivity analysis."""
    # Load graph data from JSON
    with open('input_graph.json', 'r') as f:
        data = json.load(f)
    
    # Count edges from input
    input_edge_count = len(data['edges'])
    
    # Build graph
    G = nx.Graph()
    G.add_nodes_from(data['nodes'])
    G.add_edges_from(data['edges'])
    
    # Analyze connectivity
    analysis = analyze_connectivity(G, input_edge_count=input_edge_count)
    
    # Print results as JSON
    print(json.dumps(analysis, indent=2))
    
    # Optionally save to output file
    with open('output_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print("\nAnalysis saved to output_analysis.json")


if __name__ == "__main__":
    main()
