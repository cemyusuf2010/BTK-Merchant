import os, sys, subprocess
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("GROQ_API_KEY", "")
if not key or "buraya" in key:
    print("\n❌ HATA: .env dosyasına GROQ_API_KEY'i yaz!\n")
    sys.exit(1)

print("\n✅ API key tamam!")
print("🚀 Uygulama başlıyor...")
print("🌐 Tarayıcıda aç: http://localhost:8000")
print("⛔ Durdurmak için: Ctrl+C\n")

subprocess.run([
    sys.executable, "-m", "uvicorn",
    "main:app", "--host", "0.0.0.0",
    "--port", "8000", "--reload"
])
