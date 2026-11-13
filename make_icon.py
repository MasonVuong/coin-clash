from PIL import Image

SRC = "assets/small_icon.png"
OUT = "assets/icon.ico"
sizes = [16, 32, 64, 128, 256]

src = Image.open(SRC).convert("RGBA")
imgs = [src.resize((s, s), Image.NEAREST) for s in sizes]
imgs[-1].save(OUT, sizes=[(s, s) for s in sizes], append_images=imgs[:-1])
print("Wrote", OUT)