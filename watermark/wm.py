import os
from PIL import Image, ImageDraw, ImageFont

# ======================
# Konfigurasi Watermark
# ======================

input_folder = r'F:\MIWE DIGITAL STORE\input'
output_folder = r'F:\MIWE DIGITAL STORE\output'

# Pastikan output folder ada
os.makedirs(output_folder, exist_ok=True)

font_path = r'F:\MIWE DIGITAL STORE\watermark\Ahkio-W00-Bold.ttf'
font_size = 46
watermark_text = "@MIWEDIGITALSTORE"

total_lines = 4             # Total baris watermark
line_spacing = 80           # Jarak antar baris watermark
shadow_offset = (5, 5)      # Offset kecil bayangan

# Warna watermark
text_color = (0, 102, 204, 130)         # Biru tebel, alpha 130 (lebih tipis)
shadow_color = (204, 255, 0, 110)       # Hijau neon, alpha 110 (lebih tipis)

# Mulai dari ORDERAN19
orderan_number = 1

# ======================
# Proses Watermark
# ======================

font = ImageFont.truetype(font_path, font_size)

# List semua file input
input_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for filename in input_files:
    image_path = os.path.join(input_folder, filename)
    image = Image.open(image_path).convert('RGBA')

    # Buat layer watermark
    watermark_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Hitung ukuran teks
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    total_height = total_lines * text_height + (total_lines - 1) * line_spacing

    start_y = (image.height - total_height) // 2 + 50  # Geser ke bawah 50px

    # Tulis watermark berulang
    for i in range(total_lines):
        x = (image.width - text_width) // 2
        y = start_y + i * (text_height + line_spacing)

        # Draw shadow (bayangan hijau neon)
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), watermark_text, font=font, fill=shadow_color)

        # Draw main text (teks biru tebel)
        draw.text((x, y), watermark_text, font=font, fill=text_color)

    # Cek apakah file sudah ada, kalau ada, naikin orderan_number sampai kosong
    while True:
        output_filename = f"ORDERAN FORE {orderan_number} - MIWEDIGITALSTORE.jpg"
        output_path = os.path.join(output_folder, output_filename)
        if not os.path.exists(output_path):
            break
        orderan_number += 1  # Naikkan ORDERAN kalau file sudah ada

    # Gabungkan watermark dengan gambar asli
    watermarked_image = Image.alpha_composite(image, watermark_layer)

    # Simpan hasil
    watermarked_image.convert('RGB').save(output_path)

    print(f"Sukses buat watermark di {output_filename}")

    # Setelah save, lanjutkan ke nomor berikutnya
    orderan_number += 1

print("Semua gambar sudah diproses!")
