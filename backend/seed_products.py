import requests

API_URL = "http://127.0.0.1:8000/products/"

products = [
    {"name": "Kablosuz Kulaklık", "description": "Bluetooth 5.0, gürültü engelleme", "price": 1299, "stock": 50, "image_url": "https://images.migrosone.com/sanalmarket/product/39280107/39280107-7dfa72-1650x1650.jpg"},
    {"name": "Akıllı Saat", "description": "Nabız ve uyku takibi, su geçirmez", "price": 2499, "stock": 30, "image_url": "https://cdn.dsmcdn.com/mnresize/400/-/ty1689/prod/QC_PREP/20250606/14/7a9a878e-6a40-3b93-93c2-9decd3d696c2/1_org_zoom.jpg"},
    {"name": "Dizüstü Bilgisayar", "description": "16GB RAM, 512GB SSD", "price": 24999, "stock": 15, "image_url": "https://www.casper.com.tr/uploads/2025/02/buyuk_op.webp"},
    {"name": "Kahve Makinesi", "description": "Otomatik espresso, 15 bar", "price": 3799, "stock": 20, "image_url": "https://www.egemende.com/uploads/urun/b/20262312_tp517r03_stp-d_def.webp"},
    {"name": "Bilgisayar Kasası", "description": "Tamperli ön ve yan cam paneller ile benzersiz bi görüntü", "price": 1599, "stock": 60, "image_url": "https://www.casper.com.tr/uploads/2024/09/Excalibur-E650-Masaustu-Oyun-Bilgisayari_op.webp"},
    {"name": "Sırt Çantası", "description": "Laptop bölmeli, su geçirmez", "price": 899, "stock": 40, "image_url": "https://productimages.hepsiburada.net/s/540/375-375/110000600339847.jpg"},
    {"name": "Bluetooth Hoparlör", "description": "Taşınabilir, 20 saat pil", "price": 1099, "stock": 35, "image_url": "https://cdn.akakce.com/z/jbl/jbl-charge-5.jpg"},
    {"name": "Mekanik Klavye", "description": "RGB ışıklı, mavi switch", "price": 1799, "stock": 25, "image_url": "https://m.media-amazon.com/images/I/71KyO5pXMCL._AC_UF1000,1000_QL80_.jpg"},
    {"name": "Oyuncu Faresi", "description": "16000 DPI, ergonomik", "price": 749, "stock": 45, "image_url": "https://productimages.hepsiburada.net/s/100/375-375/110000042920004.jpg"},
    {"name": "Tablet", "description": "10 inç ekran, 128GB", "price": 8999, "stock": 18, "image_url": "https://cdn.dsmcdn.com/mnresize/420/620/ty1743/product/media/images/prod/PIM/20250903/14/4da4f5f6-8c16-4557-9020-316ab6c81c67/1_org_zoom.jpg"},
    {"name": "Telefon", "description": "İphone 17 pro 128 GB ", "price": 80000, "stock": 55, "image_url": "https://wp.oggusto.com/wp-content/uploads/2026/02/iphone-17-mavi.webp"},
    {"name": "Termos", "description": "500ml, 12 saat sıcak tutar", "price": 399, "stock": 70, "image_url": "https://www.ersinoutdoor.com/idea/ac/42/myassets/products/480/b7cc571a5a2145a298025047592b628d.png?revision=1784377534"},
    {"name": "Powerbank", "description": "20000mAh, hızlı şarj", "price": 899, "stock": 50, "image_url": "https://m.media-amazon.com/images/I/614OfiBkyZL._AC_UF1000,1000_QL80_.jpg"},
    {"name": "Masa Lambası", "description": "LED, ayarlanabilir parlaklık", "price": 549, "stock": 40, "image_url": "https://m.media-amazon.com/images/I/51h1lunMgTL.jpg"},
    {"name": "Şarj Aleti", "description": "İphone hızlı şarj aleti", "price": 459, "stock": 65, "image_url": "https://cdn.myikas.com/images/3f3b3708-17e3-4747-9384-f938f367f8de/ce367a90-0fac-4ad1-b085-81d033225a39/1080/iphone-hizli-sarj-aleti-seti-20w-adaptor-usb-c-kablo.jpg"},
    {"name": "Televizyon", "description": "Son teknoloji harikası", "price": 55000, "stock": 65, "image_url": "https://img-s3.onedio.com/id-63f5ccb0398389c651d54698/rev-0/w-600/h-409/f-jpg/s-12098f1cd81a73313d4f2dc1976748a14f21f437.jpg"},
]

for product in products:
    response = requests.post(API_URL, json=product)
    if response.status_code == 200:
        print(f"✓ Eklendi: {product['name']}")
    else:
        print(f"✗ Hata ({response.status_code}): {product['name']} - {response.text}")

print("Bitti!")