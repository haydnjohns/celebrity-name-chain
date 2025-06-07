import json
from collections import defaultdict
from colorama import init, Fore
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
    """Parse names into first and last name components."""
    parsed = []
    for name in names_list:
        parts = name.strip().split()
        if len(parts) >= 2:
            # Taking the first part as first name and last part as last name
            parsed.append((parts[0], parts[-1], name))
    return parsed


def build_graph_and_connectivity(parsed_names):
    """
    Builds a directed graph and tracks in/out-degree for each name.
    Now returns:
    - graph: outgoing connections (edges)
    - in_degree: how many times a name is targeted
    - out_degree: how many times a name points to others
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    by_first = defaultdict(list)

    # Group names by first name
    for first, _, full_name in parsed_names:
        by_first[first].append(full_name)

    # Build the graph and count degrees
    for _, last, full_name in parsed_names:
        if last in by_first:
            for successor_full_name in by_first[last]:
                if full_name != successor_full_name:
                    graph[full_name].append(successor_full_name)
                    out_degree[full_name] += 1
                    in_degree[successor_full_name] += 1

    return graph, in_degree, out_degree


def _find_paths_recursive(graph, node, length, path, visited, results, target_count, is_loop=False,
                          original_start=None):
    """
    Efficient recursive helper for finding chains and loops using backtracking.
    OPTIMIZATION: Uses append/pop on a single path list and a visited set for O(1) lookups,
    avoiding slow list concatenation and searching.
    """
    # Early exit if we have already found enough results.
    if len(results) >= target_count:
        return

    # Add current node to the path
    path.append(node)
    visited.add(node)

    # If the path has reached the desired length
    if len(path) == length:
        if is_loop:
            # For a loop, check if the last node connects back to the original start
            if original_start in graph.get(node, []):
                results.append(list(path))  # Add a copy of the path
        else:
            # For a chain, any path of the correct length is a valid result
            results.append(list(path))
    else:
        # Continue searching deeper
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _find_paths_recursive(graph, neighbor, length, path, visited, results, target_count, is_loop,
                                      original_start)

    # Backtrack: remove the current node to explore other branches
    path.pop()
    visited.remove(node)


def find_results(graph, sorted_names, length, chain_type, target_count):
    """
    Finds chains or loops of a specific length.
    This function now acts as a wrapper for the efficient recursive helper.
    """
    results = []
    seen = set()
    is_loop = chain_type.lower() == "loop"

    for _, _, start_node in sorted_names:
        if len(results) >= target_count:
            break

        path = []
        visited = set()

        if is_loop:
            _find_paths_recursive(graph, start_node, length, path, visited, results, target_count, is_loop=True,
                                  original_start=start_node)
        else:
            _find_paths_recursive(graph, start_node, length, path, visited, results, target_count, is_loop=False)

    # Deduplicate and normalize loops
    final_results = []
    for res in results:
        if is_loop:
            # Normalize the loop to start with the lexicographically smallest name to handle rotational duplicates
            min_idx = res.index(min(res))
            normalized = tuple(res[min_idx:] + res[:min_idx])
            if normalized not in seen:
                seen.add(normalized)
                final_results.append(list(normalized))
        else:
            res_tuple = tuple(res)
            if res_tuple not in seen:
                seen.add(res_tuple)
                final_results.append(res)

    return final_results[:target_count]


def create_name_chains(celebrity_list_path, chain_type, min_length, max_length, max_chains_per_length):
    """Main function to generate name chains or loops."""
    init(autoreset=True)
    celebrity_names = load_names(celebrity_list_path)

    if not celebrity_names:
        print("No celebrity names loaded, aborting.")
        return

    print(f"Loaded {len(celebrity_names)} celebrity names")

    parsed_names = parse_names(celebrity_names)
    graph, in_degree, out_degree = build_graph_and_connectivity(parsed_names)

    # TRIM: Keep only names that have at least one incoming and one outgoing connection
    connected_names = [
        entry for entry in parsed_names
        if in_degree.get(entry[2], 0) > 0 and out_degree.get(entry[2], 0) > 0
    ]

    # Sort by total connectivity (in + out)
    sorted_names = sorted(
        connected_names,
        key=lambda x: in_degree.get(x[2], 0) + out_degree.get(x[2], 0),
        reverse=True
    )

    print(Fore.GREEN + f"\nGraph has been built. Starting search...")

    for length in range(min_length, max_length + 1):
        print(Fore.GREEN + f"\n=== Finding {chain_type}s of length {length} ===")
        if length < 2:
            print("Error: Length must be at least 2")
            continue

        results = find_results(graph, sorted_names, length, chain_type, max_chains_per_length)

        print(Fore.YELLOW + f"Found {len(results)} {chain_type}s")
        for i, chain in enumerate(results):
            if chain_type.lower() == "loop":
                print(f"{chain_type.capitalize()} {i + 1}: {' → '.join(chain + [chain[0]])}")
            else:
                print(f"{chain_type.capitalize()} {i + 1}: {' → '.join(chain)}")

    total_connections = sum(len(neighbors) for neighbors in graph.values())
    print(Fore.GREEN + f"\n--- Statistics ---")
    print(f"Total names processed: {len(parsed_names)}")
    print(f"Names with connections (nodes in graph): {len(graph)}")
    print(f"Total connections (edges in graph): {total_connections}")


if __name__ == "__main__":
    celebrity_list_path = os.path.join(OUTPUT_DIR, "celebrity_list_long_cleaned.json")
    chain_type = "loop"  # or 'chain'
    min_length = 2
    max_length = 10
    max_chains_per_length = 10

    create_name_chains(celebrity_list_path, chain_type, min_length, max_length, max_chains_per_length)