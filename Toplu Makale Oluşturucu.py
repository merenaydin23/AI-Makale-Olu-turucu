import cohere
import os
import time
import unicodedata
import re

# ➤ Cohere API anahtarınızı buraya girin
API_KEY = "lemZ7S1EkdoLWZ8ZRpMS9c1iOHEjyhVcIDpLHEhR"
client = cohere.Client(API_KEY)

# Türkçe karakterleri ASCII'ye çevir (dosya/dizin adları için)
def ascii_cevir(metin):
    return unicodedata.normalize('NFKD', metin).encode('ascii', 'ignore').decode('ascii')

# ➤ Akademik makale üretimi yapan fonksiyon
def makale_uret(konu, min_karakter=8000):
    parcalar = []
    prompt = (
        f"Write a detailed academic research article in Turkish on the topic '{konu}'.\n"
        "Do not include tables, figures, visuals, or code.\n"
        "Write the article in continuous paragraphs without empty lines between paragraphs.\n"
        "Format must include:\n"
        "1. Title (must be unique and different each time, creative and relevant to the topic)\n"
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
        temperature=0.9  # Daha yaratıcı ve çeşitli metinler için
    )
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Yanıt içeriği alınamadı.")
    parcalar.append(text.strip())

    # Makale tamamlanana kadar devam edilir
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
            temperature=0.9
        )
        text = getattr(response, "text", None)
        if not text or text.strip() == "":
            break
        parcalar.append(text.strip())
    return "".join(parcalar)

# Aynı konudan varsa, yeni dosya numarasını belirler
def dosya_numarasi_al(klasor, konu_ascii):
    if not os.path.exists(klasor):
        return 1
    dosyalar = os.listdir(klasor)
    pattern = re.compile(rf"{re.escape(konu_ascii)}_(\d+)\.txt$")
    numaralar = [int(m.group(1)) for d in dosyalar if (m := pattern.match(d))]
    return max(numaralar) + 1 if numaralar else 1

def main():
    konular = [
        "Yapay Zeka", "İklim Değişikliği", "Dijital Pazarlama", "Veri Analizi", "Nöro Bilim",
        "Genetik Mühendislik", "Sosyal Medya", "Küresel Isınma", "Siber Güvenlik", "İnsan Hakları",
        "Enerji Verimliliği", "Robotik Sistemler", "Uzay Teknolojisi", "Biyoçeşitlilik Koruma", "Blockchain Teknolojisi",
        "Ekonomik Kalkınma", "Kanser Tedavisi", "Tarım Teknolojisi", "Sürdürülebilir Kalkınma", "Elektrik Enerjisi",
        "Oyun Tasarımı", "Dil Öğrenimi", "Psikolojik Sağlık", "Güneş Enerjisi", "Mobil Uygulamalar",
        "Eğitim Teknolojileri", "İnovasyon Yönetimi", "Finansal Analiz", "İklim Politikası", "İnsan Beyni",
        "Su Kirliliği", "Genetik Kodlama", "Yapay Sinir", "Kültür Politikası", "Ekosistem Hizmeti",
        "Veri Madenciliği", "Nanoteknoloji Uygulamaları", "Medya Etiği", "Siyasi İletişim", "Toplum Sağlığı",
        "Enerji Depolama", "Hava Kirliliği", "Yazılım Mühendisliği", "İnsan Kaynakları", "Organik Tarım",
        "Uzaktan Eğitim", "Elektronik Ticaret", "Yapay Zekâ", "Ağ Güvenliği", "Alternatif Enerji",
        "Veri Gizliliği", "Büyük Veri", "Mikroorganizma Etkisi", "Sürdürülebilir Tarım", "Yenilenebilir Enerji",
        "Sinyal İşleme", "Etik Değerler", "Sosyal Adalet", "Psikolojik Direnç", "İnsansız Araçlar",
        "İklim Modelleri", "Bilişsel Bilim", "Çevre Kirliliği", "Enerji Politikası", "Veri Güvenliği",
        "Dijital Dönüşüm", "Sosyal Ağlar", "Endüstri 4.0", "Tarım Biyoteknolojisi", "Ekonomik Kriz",
        "Kanser Genetiği", "Yapay Organlar", "Siyasi İdeolojiler", "Eğitim Reformu", "Gıda Teknolojisi",
        "Uygulamalı Matematik", "Bilgisayar Grafiği", "İlaç Endüstrisi", "İnsan Davranışı", "Enerji Verimliliği",
        "Akıllı Şehirler", "Su Kaynakları", "Mühendislik Tasarımı", "Dijital Medya", "Kültürel Miras",
        "Sosyal Psikoloji", "Finans Teknolojisi", "Yapay Öğrenme", "Biyomedikal Mühendislik", "Okyanus Bilimi",
        "Kentsel Dönüşüm", "Veri Bilimi", "Çevre Politikası", "Nükleer Enerji", "Elektrik Elektronik",
        "İnsansız Sistemler", "Endüstriyel Otomasyon", "İnsan Hakları", "Biyoenerji Teknolojisi", "Gelişmiş Malzemeler",
        "Kültürel Kimlik", "Veri Madenciliği", "İklim Adaptasyonu", "Sürdürülebilir Enerji", "Psikolojik Etkiler",
        "Tarım Ekonomisi", "Yapay Zekâ", "Bilişim Güvenliği", "Nöroloji Araştırmaları", "Bilgi Yönetimi",
        "Enerji Sistemleri", "Yazılım Geliştirme", "Akıllı Sistemler", "Kentsel Planlama", "Genetik Araştırmalar",
        "Yenilenebilir Kaynaklar", "Gıda Güvenliği", "Siyasi Ekonomi", "Dijital Pazarlama", "Endüstri Tasarımı",
        "Sosyal Sorumluluk", "Yapay Sinir", "Ekosistem Yönetimi", "Veri Analitiği", "Biyoteknoloji Uygulamaları",
        "Eğitim Politikası", "Elektrik Şebekesi", "Hava Kalitesi", "İnsansız Hava", "Ekonomik Politika",
        "İnsan Sağlığı", "Akıllı Ağlar", "Çevre Yönetimi", "Dijital Eğitim", "Nano Teknoloji",
        "Sosyal Medya", "Güneş Panelleri", "Uzay Araştırmaları", "Finansal Teknolojiler", "Yapay Zekâ Uygulamaları",
        "Tarım Politikası", "Sürdürülebilir Kalkınma", "Psikolojik Destek", "Bilişim Teknolojileri", "Enerji Kaynakları",
        "İnsan Davranışları", "Kentsel Ekoloji", "Veri Yönetimi", "Ekonomik Analiz", "İklim Değişikliği",
        "Dijital Platformlar", "Çevre Teknolojileri", "Yapay Organlar", "Robotik Teknolojisi", "Sosyal Etkileşim",
        "Yenilenebilir Enerji", "Biyolojik Çeşitlilik", "Eğitim Sistemleri", "Elektronik Cihazlar", "Akıllı Robotlar",
        "Genetik Bilim", "Tarım Teknolojileri", "Enerji Verimliliği", "Psikolojik Araştırma", "Dijital Güvenlik",
        "Sürdürülebilir Tarım", "İnsan Kaynakları", "Kentsel Dönüşüm", "Veri Güvenliği", "Ekosistem Bilimi",
        "Yapay Öğrenme", "Bilişim Sistemleri", "Hava Kirliliği", "Elektrik Enerjisi", "İnsan Hakları",
        "Dijital İletişim", "Siyasi Bilim", "Yenilenebilir Kaynaklar", "Genetik Mühendislik", "Tarım Ekonomisi",
        "Enerji Politikası", "Psikolojik Sağlık", "Sosyal Medya", "Yapay Zekâ", "Biyoçeşitlilik",
        "Eğitim Teknolojileri", "Elektronik Ticaret", "Akıllı Sistemler", "Küresel Isınma", "Nöro Bilim",
        "Robotik Sistemler", "İnsan Davranışı", "Veri Bilimi", "Finansal Analiz", "Kültür Politikası"
    ]

    makale_adet = 5
    klasor = r"C:\Users\muham\OneDrive\Masaüstü\Aİ Makaleler"
    os.makedirs(klasor, exist_ok=True)

    for konu in konular:
        konu_ascii = ascii_cevir(konu)
        bas_num = dosya_numarasi_al(klasor, konu_ascii)

        for i in range(bas_num, bas_num + makale_adet):
            print(f"'{konu}' konusu için {i}. makale üretiliyor...")
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

            time.sleep(1)  # API aşırı yüklenmesini önlemek için bekleme

if __name__ == "__main__":
    main()
