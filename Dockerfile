# Gunakan image Python sebagai dasar
FROM python:3.10

# Set direktori kerja
WORKDIR /app

# Copy semua file ke dalam container
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python", "bot.py"]
