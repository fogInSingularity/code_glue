import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: script.py <output_file> <prepend_file> <list_file>")
        sys.exit(1)

    output_file, prepend_file, list_file = sys.argv[1:4]

    try:
        # Read prepend content
        with open(prepend_file, 'r') as f:
            prepend_content = f.read()
        
        # Read list of paths
        with open(list_file, 'r') as f:
            paths = [line.strip() for line in f if line.strip()]
        
        # Process output
        with open(output_file, 'w') as out:
            out.write(prepend_content)
            
            for path in paths:
                if os.path.isfile(path):
                    try:
                        with open(path, 'r') as infile:
                            content = infile.read()
                        out.write(f"\n[file name:]\n{path}\n[file content:]\n{content}")
                    except Exception as e:
                        print(f"Warning: Could not read file {path}: {e}", file=sys.stderr)
                elif os.path.isdir(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r') as infile:
                                    content = infile.read()
                                out.write(f"\n[file name:]\n{file_path}\n[file content:]\n\n{content}")
                            except Exception as e:
                                print(f"Warning: Could not read file {file_path}: {e}", file=sys.stderr)
                else:
                    print(f"Warning: {path} is not a file or directory.", file=sys.stderr)
    
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
