# kernel_call_graph

This Repository creates a call graph of a given function inside the Linux kernel.

## Requirements
- cscope
- python3

## How to use
1. Download the kernel source
    ```shell
    make "$(pwd)"/linux
    ```
2. Creates `cscope.files` with list of files to scan
    ```shell
    make cscope.files
    ```
3. Creates cscope DB
    ```shell
    make cscope.out
    ```
4. Creates `callgraph.dot` file
    ```shell
    python3 gen_dot.py
    ```
5. Generate png from `callgraph.dot` file
