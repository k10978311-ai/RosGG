import re

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"

with open(so_path, "rb") as f:
    data = f.read()

target = b"LoginHandler::onLoginReply"
idx = 0
found = []
while True:
    pos = data.find(target, idx)
    if pos == -1:
        break
    found.append(pos)
    idx = pos + 1

print(f"Found string '{target.decode()}' at offsets: {[hex(x) for x in found]}")

for pos in found:
    # Print surrounding string
    start = max(0, pos - 50)
    end = min(len(data), pos + 150)
    print("Context:", data[pos:end])
