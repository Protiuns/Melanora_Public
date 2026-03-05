from pathlib import Path
import os

p = Path("test.txt")
p.write_text("hello")
t = p.with_suffix(".tmp")
t.write_text("world")

try:
    print(f"Testing replace on {type(t)}")
    t.replace(p)
    print("Success")
except Exception as e:
    print(f"Failed: {e}")

if p.exists(): os.remove("test.txt")
if t.exists(): os.remove("test.txt.tmp")
