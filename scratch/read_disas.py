import opcode

# Let's decode the disassembly from step 5266
# Read the task log where step 5266 output was written
with open(r'C:\Users\Lufy\.gemini\antigravity\brain\13d441ce-2f48-4aec-aea9-19220eb4e736\.system_generated\steps\5266\output.txt', 'r', errors='ignore') as f:
    text = f.read()

print("File size:", len(text))
for line in text.splitlines()[600:750]:
    print(line)
