import os
import subprocess

def gen_db():
    subprocess.run(['cscope', '-b', '-q', '-k'], stdout=subprocess.PIPE, text=True)

def print_called_functions(function_name, dot_file, visited=set()):

    # Create a local set for the current call
    local_visited = visited #| {function_name}  # Union of visited and the current function
    print(function_name)

    result = subprocess.run(['cscope', '-d', '-L', '-2', function_name], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()

    for line in lines:
        # Assuming cscope output format: <function> <filename> <line> <text>
        parts = line.split()
        if len(parts) >= 4:
            called_function = parts[1]
            
            # Recursive call only if the called function has not been visited in this path
            if called_function not in local_visited:
                dot_file.write(f'    "{function_name}" -> "{called_function}";\n')
                local_visited = local_visited | {called_function}  # Union of visited and the current function
                print_called_functions(called_function, dot_file, local_visited)
            

def generate_opening(dot_file):
    dot_file.write("digraph G {\n")

def generate_closing(dot_file):
        dot_file.write("}\n")

function_name = "bpf_int_jit_compile"  # Replace with your starting function

# gen DB
gen_db()

# open file
with open("callgraph.dot", "w") as dot_file:
    
    # gen opening
    generate_opening(dot_file)
    
    # gen call graphs
    print_called_functions(function_name, dot_file)

    # gen closing
    generate_closing(dot_file)
