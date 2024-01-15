import re


def remove_blank_lines(file_pth:str) -> None:  # Born @ Jan 15, 2024

    with open(file_pth, 'r') as f:
        text = f.read()

    parts = text.split('\n')

    for idx, line in enumerate(parts):
        
        res = re.match(r'^[ ]*$', line)
        if res is not None:
            parts[idx] = None
    
    parts = [p for p in parts if (p is not None)]

    with open(file_pth, 'w') as f:
        f.write('\n'.join(parts))
