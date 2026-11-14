import io
t = io.open(r"ru\RustBook-RU.md", encoding="utf-8").read()
print("=== HEAD (first 3000 chars) ===")
print(t[:3000])
print("...")
print("=== TAIL ===")
print(t[-700:])
