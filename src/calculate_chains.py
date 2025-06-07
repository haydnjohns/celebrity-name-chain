import json
from collections import defaultdict
from colorama import init, Fore, Style
import os
from config import OUTPUT_DIR

def load_names(filename):
    """Load celebrity names from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{filename}'.")
        return []

def parse_names(names_list):
    """Parse names into first and last name components"""
    parsed = []
    for name in names_list:
        parts = name.strip().split()
        if len(parts) >= 2:
            first_name = parts[0]
            last_name = parts[-1]  # Take last part as surname
            parsed.append((first_name, last_name, name))
    return parsed

def build_graph(parsed_names):
    """Build directed graph connecting names by matching last->first name"""
    by_first = defaultdict(list)
    by_last = defaultdict(list)

    for first, last, full_name in parsed_names:
        by_first[first].append((first, last, full_name))
        by_last[last].append((first, last, full_name))

    graph = defaultdict(list)
    for first, last, full_name in parsed_names:
        for next_first, next_last, next_full_name in by_first.get(last, []):
            if full_name != next_full_name:
                graph[full_name].append(next_full_name)

    return graph

def find_chains(graph, start_name, length, visited=None):
    """Recursively find chains of given length"""
    if visited is None:
        visited = []

    if len(visited) == length:
        return [visited]

    if start_name in visited:
        return []

    chains = []
    if start_name in graph:
        for next_name in graph[start_name]:
            chains.extend(find_chains(graph, next_name, length, visited + [start_name]))

    return chains

def find_loops(graph, start_name, length, visited=None, original_start=None):
    """Recursively find loops of given length"""
    if visited is None:
        visited = []
    if original_start is None:
        original_start = start_name

    if len(visited) == length:
        last_node = visited[-1]
        if last_node in graph and original_start in graph[last_node]:
            return [visited]
        return []

    if start_name in visited:
        return []

    loops = []
    if start_name in graph:
        for next_name in graph[start_name]:
            loops.extend(find_loops(graph, next_name, length, visited + [start_name], original_start))

    return loops

def calculate_node_connectivity(graph, parsed_names):
    """Calculate connectivity (in + out edges) for each node"""
    connectivity = {}

    for name in graph:
        connectivity[name] = connectivity.get(name, 0) + len(graph[name])

    for neighbors in graph.values():
        for neighbor in neighbors:
            connectivity[neighbor] = connectivity.get(neighbor, 0) + 1

    # Add nodes with zero connectivity
    for _, _, full_name in parsed_names:
        if full_name not in connectivity:
            connectivity[full_name] = 0

    return connectivity

def create_chain(length, chain_type, names_list, target_count=10):
    """Find chains or loops of given length and count"""
    if length < 2:
        print("Error: Length must be at least 2")
        return []
    if target_count < 1:
        print("Error: Target count must be at least 1")
        return []

    parsed_names = parse_names(names_list)
    graph = build_graph(parsed_names)

    connectivity = calculate_node_connectivity(graph, parsed_names)
    sorted_names = sorted(parsed_names, key=lambda x: connectivity[x[2]], reverse=True)

    results = []
    seen = set()

    if chain_type.lower() == "chain":
        for _, _, full_name in sorted_names:
            if connectivity[full_name] == 0:
                continue
            chains = find_chains(graph, full_name, length)
            for chain in chains:
                chain_tuple = tuple(chain)
                if chain_tuple not in seen:
                    seen.add(chain_tuple)
                    results.append(chain)
                    if len(results) >= target_count:
                        print(Fore.YELLOW + f"Found {len(results)} chains")
                        return results
    elif chain_type.lower() == "loop":
        for _, _, full_name in sorted_names:
            if connectivity[full_name] == 0:
                continue
            loops = find_loops(graph, full_name, length)
            for loop in loops:
                # Normalize loop to start with lex smallest name
                min_idx = loop.index(min(loop))
                normalized_loop = loop[min_idx:] + loop[:min_idx]
                loop_tuple = tuple(normalized_loop)
                if loop_tuple not in seen:
                    seen.add(loop_tuple)
                    results.append(normalized_loop)
                    if len(results) >= target_count:
                        print(Fore.YELLOW + f"Found {len(results)} loops")
                        return results
    else:
        print("Error: chain_type must be 'chain' or 'loop'")
        return []

    print(Fore.YELLOW + f"Found {len(results)} {chain_type}s")
    return results

def create_name_chains(celebrity_list_path, chain_type, min_length, max_length, max_chains_per_length):
    init(autoreset=True)
    celebrity_names = load_names(celebrity_list_path)

    if not celebrity_names:
        print("No celebrity names loaded, aborting.")
        return

    print(f"Loaded {len(celebrity_names)} celebrity names")

    for length in range(min_length, max_length + 1):
        print(Fore.GREEN + f"\n=== Finding {chain_type}s of length {length} ===")
        results = create_chain(length, chain_type, celebrity_names, max_chains_per_length)
        for i, chain in enumerate(results):
            if chain_type.lower() == "loop":
                print(f"{chain_type.capitalize()} {i + 1}: {' → '.join(chain + [chain[0]])}")
            else:
                print(f"{chain_type.capitalize()} {i + 1}: {' → '.join(chain)}")

    parsed_names = parse_names(celebrity_names)
    graph = build_graph(parsed_names)
    total_connections = sum(len(neighbors) for neighbors in graph.values())

    print(Fore.GREEN + f"\nStatistics:")
    print(f"Total names: {len(celebrity_names)}")
    print(f"Names with connections: {len(graph)}")
    print(f"Total connections: {total_connections}")

if __name__ == "__main__":
    celebrity_list_path = os.path.join(OUTPUT_DIR, "celebrity_list_long_cleaned.json")
    chain_type = "loop"  # or 'chain'
    min_length = 2
    max_length = 10
    max_chains_per_length = 10

    create_name_chains(celebrity_list_path, chain_type, min_length, max_length, max_chains_per_length)