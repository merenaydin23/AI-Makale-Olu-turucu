import cohere
import os
import time
import unicodedata
import re

# ➤ BURAYA kendi Cohere API anahtarınızı girin
API_KEY = "lemZ7S1EkdoLWZ8ZRpMS9c1iOHEjyhVcIDpLHEhR"
client = cohere.Client(API_KEY)

# Türkçe karakterleri ASCII'ye çevirir (dosya adları için kullanılır)
def ascii_cevir(metin):
    return unicodedata.normalize('NFKD', metin).encode('ascii', 'ignore').decode('ascii')

# ➤ Verilen konuda akademik bir makale üretir, uzunluğu belirli bir karakter sayısına ulaşana kadar devam eder
def makale_uret(konu, min_karakter=8000):
    parcalar = []
    prompt = (
        f"Write a detailed academic research article in Turkish on the topic '{konu}'.\n"
        "Do not include tables, figures, visuals, or code.\n"
        "Write the article in continuous paragraphs without empty lines between paragraphs.\n"
        "Format must include:\n"
        "1. Title (single line)\n"
        "2. ABSTRACT:\n"
        "A short summary of the article\n"
        "3. ARTICLE:\n"
        "The full academic article text\n"
        "Ensure the writing is formal, academic, and uses proper research style.\n"
        "Start the article now."
    )

    response = client.chat(
        model="command-xlarge-nightly",
        message=prompt,
        max_tokens=1500,
        temperature=0.7
    )
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Yanıt içeriği alınamadı.")
    parcalar.append(text.strip())

    # Makale tamamlanana kadar yazmaya devam edilir
    while sum(len(p) for p in parcalar) < min_karakter:
        prompt_continue = (
            "Continue writing the academic article in Turkish on the same topic.\n"
            "Do not repeat previous parts.\n"
            "Write continuously without empty lines between paragraphs.\n"
            "Continue from where you left off."
        )
        response = client.chat(
            model="command-xlarge-nightly",
            message=prompt_continue,
            max_tokens=1500,
            temperature=0.7
        )
        text = getattr(response, "text", None)
        if not text or text.strip() == "":
            break
        parcalar.append(text.strip())
    return "".join(parcalar)

# Aynı konudan üretilmiş dosyalar varsa, yeni dosya numarasını belirler
def dosya_numarasi_al(klasor, konu_ascii):
    dosyalar = os.listdir(klasor)
    pattern = re.compile(rf"{re.escape(konu_ascii)}_(\d+)\.txt$")
    numaralar = [int(m.group(1)) for d in dosyalar if (m := pattern.match(d))]
    return max(numaralar) + 1 if numaralar else 1

def main():
    konu = input("Makalenin konusu: ").strip().lower()  # kullanıcıdan konu al
    adet = int(input("Kaç makale üretilecek?: ").strip())

    # ➤ BURAYA makalelerin kaydedileceği klasör yolunu girin (örneğin masaüstü)
    klasor = r"C:\Users\muham\OneDrive\Masaüstü\Aİ Makaleler"
    os.makedirs(klasor, exist_ok=True)

    konu_ascii = ascii_cevir(konu)
    bas_num = dosya_numarasi_al(klasor, konu_ascii)

    # Makaleleri sırayla üretir ve kaydeder
    for i in range(bas_num, bas_num + adet):
        print(f"{i}. makale üretiliyor...")
        try:
            metin = makale_uret(konu)
        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

        dosya_adi = f"{konu_ascii}_{i}.txt"
        dosya_yolu = os.path.join(klasor, dosya_adi)
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            f.write(metin)
        print(f"{i}. makale kaydedildi: {dosya_yolu}")
        time.sleep(1)

if __name__ == "__main__":
    main()
