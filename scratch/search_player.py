import glob
for p in glob.glob('decompile/script/strings/*.txt'):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if 'Globals' in text and 'player' in text:
        first = text.split('\n')[0]
        for line in text.split('\n'):
            parts = line.split('\t')
            if len(parts) >= 3 and parts[0] in ('name', 'const') and parts[2].strip("' ") == 'player':
                fn = parts[1]
                if any(k in first for k in ['Athlete', 'Hall', 'Login', 'ClientEntity', 'Scene']):
                    print(first, fn, line)
