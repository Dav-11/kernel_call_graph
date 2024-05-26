import os
import subprocess

# init visited array
visited = set()

def gen_db():
    subprocess.run(['cscope', '-b', '-q', '-k'], stdout=subprocess.PIPE, text=True)

def print_called_functions(function_name, dot_file):

    if function_name not in visited:
        
        visited.add(function_name)  # Union of visited and the current function
        print(function_name)

        result = subprocess.run(['cscope', '-d', '-L', '-2', function_name], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()

        # create array to avoid repeating the same link if func is called more than once
        called = set()

        for line in lines:
            
            parts = line.split()

            if len(parts) >= 4 and parts[1] not in called:
                called_function = parts[1]
                
                # Recursive call only if the called function has not been visited in this path
                dot_file.write(f'    "{function_name}" -> "{called_function}";\n')

                # add func to called
                called = called | {called_function}
                print_called_functions(called_function, dot_file)


def generate_opening(dot_file):
    dot_file.write("digraph G {\n")

def generate_closing(dot_file):
        dot_file.write("}\n")

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate call graph for a function using Cscope and Graphviz.')
    parser.add_argument('-f', '--function', type=str, default='bpf_int_jit_compile', help='The starting function name for generating the call graph (default: bpf_int_jit_compile).')
    args = parser.parse_args()

    function_name = args.function_name  # Replace with your starting function

    print("Generating cscope DB...")

    # gen DB
    gen_db()

    print(f'Generating Dot file for func {function_name}...')

    # open file
    with open("callgraph.dot", "w") as dot_file:
        
        # gen opening
        generate_opening(dot_file)

        # gen call graphs
        print_called_functions(function_name, dot_file)

        # gen closing
        generate_closing(dot_file)

    print("Generating SVG from the Dot file...")

    # Generate SVG from the Dot file
    subprocess.run(['dot', '-Tsvg', 'callgraph.dot', '-o', 'callgraph.svg'], stdout=subprocess.PIPE, text=True)

    print("SVG generated!")

if __name__ == '__main__':
    main()
