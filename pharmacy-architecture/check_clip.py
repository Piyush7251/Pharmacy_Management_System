import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'index.html', 'r', encoding='utf-8') as f:
    text = f.read()
# Confirm new code is present
for needle in ['clipId', 'cp-', 'createElementNS', 'trunc(', 'clip-path']:
    idx = text.find(needle)
    print(f'{needle}: {"FOUND at "+str(idx) if idx >= 0 else "NOT FOUND"}')
