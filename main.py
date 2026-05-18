import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

PROMPTS = {
    "scout": """Sen bir e-ticaret pazar araştırmacısısın. Kullanıcının ürün fikrini analiz et:
1. Mikro-niş belirle (çok spesifik)
2. Hedef kitle profili
3. 3 rakip analizi
4. Pazar fırsatı skoru (1-10)
Türkçe, madde madde, max 150 kelime.""",

    "director": """Sen e-ticaret içerik direktörüsün. Pazar analizine göre:
1. Ürün başlığı (max 80 karakter)
2. SEO açıklaması (100-150 kelime)
3. 8 güçlü etiket
4. Fiyat önerisi ve gerekçe
Türkçe, profesyonel satış dili.""",

    "consumer": """Sen müşteri simülatörüsün. Ürün listesini 3 profille değerlendir:
1. Titiz Kalite Avcısı
2. İndirim Avcısı Öğrenci
3. Meşgul Profesyonel
Her biri için: düşüncesi, tıklar mı (Evet/Hayır + neden), itiraz noktası.
Sonda mutlaka şu formatta yaz: SKOR: X/10
Türkçe, eleştirel ol.""",

    "optimizer": """Sen dönüşüm optimizasyon uzmanısın. Eleştirilere göre:
1. Düzeltilen noktalar
2. YENİ başlık
3. YENİ açıklama (tüm itirazları karşıla)
4. YENİ 8 etiket
5. Özet: ne değişti ve neden daha iyi?
Türkçe yaz.""",
}

class AnalyzeRequest(BaseModel):
    product: str

def ask(system: str, user: str) -> str:
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=1024,
        temperature=0.7,
    )
    return r.choices[0].message.content

@app.get("/api")
def root():
    return {"status": "ok"}

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    scout     = ask(PROMPTS["scout"],     f'Ürün fikri: "{req.product}"')
    director  = ask(PROMPTS["director"],  f"Pazar analizi:\n{scout}\n\nBu analize göre ürün listesini oluştur.")
    consumer  = ask(PROMPTS["consumer"],  f"Ürün listesi:\n{director}\n\nMüşteri gözüyle değerlendir.")
    optimizer = ask(PROMPTS["optimizer"], f"Orijinal liste:\n{director}\n\nMüşteri eleştirileri:\n{consumer}\n\nOptimize et.")
    return {"scout": scout, "director": director, "consumer": consumer, "optimizer": optimizer}

# Frontend dosyalarını sun
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
