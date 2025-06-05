# 🤖 AI Makale Oluşturucu

Merhaba! 👋  
Bu proje, **Cohere API** kullanarak verdiğiniz konuda **uzun ve detaylı akademik makaleler** üreten bir Python uygulamasıdır.  
Yani tek seferde yüzlerce hatta binlerce kelimelik Türkçe makaleler oluşturabilirsiniz! 📚✨

---

## 🚀 Projenin Özellikleri

- 🔍 **Türkçe akademik makaleler** oluşturur  
- ✍️ Makaleler; **başlık, özet ve tam metin** şeklinde yazılır  
- 🔄 Aynı başlık veya içerik tekrar etmez, orijinal metinler üretir  
- 💾 Üretilen makaleler istediğiniz klasöre otomatik kaydedilir  
- 📝 Kullanıcıdan **konu ve kaç makale** isteneceği bilgisi alınır

---

## 📂 Dosya Yapısı & İsimlendirme

- Ana Python dosyası: `makale_olusturucu.py`

- Üretilen makaleler, sizin girdiğiniz konu başlığının ASCII’ye çevrilmiş haliyle ve artan sayılarla kaydedilir. Örnek dosya isimleri:

ekonomi_1.txt
ekonomi_2.txt
teknoloji_1.txt


---

## 🛠️ Gereksinimler & Kurulum

- Python 3.x  
- `cohere` kütüphanesi

Kurmak için terminalde şunu çalıştırabilirsiniz:

```bash
pip install cohere
