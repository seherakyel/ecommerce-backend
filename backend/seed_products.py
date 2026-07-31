import requests

API_URL = "http://127.0.0.1:8000/products/"

products = [
    {"name": "Kablosuz Kulaklık", "description": "Bluetooth 5.0, gürültü engelleme", "price": 1299, "stock": 50, "image_url": "https://picsum.photos/seed/headphone/400/400"},
    {"name": "Akıllı Saat", "description": "Nabız ve uyku takibi, su geçirmez", "price": 2499, "stock": 30, "image_url": "https://picsum.photos/seed/watch/400/400"},
    {"name": "Dizüstü Bilgisayar", "description": "16GB RAM, 512GB SSD", "price": 24999, "stock": 15, "image_url": "https://picsum.photos/seed/laptop/400/400"},
    {"name": "Kahve Makinesi", "description": "Otomatik espresso, 15 bar", "price": 3799, "stock": 20, "image_url": "https://picsum.photos/seed/coffee/400/400"},
    {"name": "Spor Ayakkabı", "description": "Hafif, nefes alan kumaş", "price": 1599, "stock": 60, "image_url": "https://picsum.photos/seed/shoe/400/400"},
    {"name": "Sırt Çantası", "description": "Laptop bölmeli, su geçirmez", "price": 899, "stock": 40, "image_url": "https://picsum.photos/seed/backpack/400/400"},
    {"name": "Bluetooth Hoparlör", "description": "Taşınabilir, 20 saat pil", "price": 1099, "stock": 35, "image_url": "https://picsum.photos/seed/speaker/400/400"},
    {"name": "Mekanik Klavye", "description": "RGB ışıklı, mavi switch", "price": 1799, "stock": 25, "image_url": "https://picsum.photos/seed/keyboard/400/400"},
    {"name": "Oyuncu Faresi", "description": "16000 DPI, ergonomik", "price": 749, "stock": 45, "image_url": "https://picsum.photos/seed/mouse/400/400"},
    {"name": "Tablet", "description": "10 inç ekran, 128GB", "price": 8999, "stock": 18, "image_url": "https://picsum.photos/seed/tablet/400/400"},
    {"name": "Güneş Gözlüğü", "description": "UV400 koruma, polarize", "price": 649, "stock": 55, "image_url": "https://picsum.photos/seed/sunglasses/400/400"},
    {"name": "Termos", "description": "500ml, 12 saat sıcak tutar", "price": 399, "stock": 70, "image_url": "https://picsum.photos/seed/thermos/400/400"},
    {"name": "Powerbank", "description": "20000mAh, hızlı şarj", "price": 899, "stock": 50, "image_url": "https://picsum.photos/seed/powerbank/400/400"},
    {"name": "Masa Lambası", "description": "LED, ayarlanabilir parlaklık", "price": 549, "stock": 40, "image_url": "https://picsum.photos/seed/lamp/400/400"},
    {"name": "Yoga Matı", "description": "Kaymaz, 6mm kalınlık", "price": 459, "stock": 65, "image_url": "https://picsum.photos/seed/yoga/400/400"},
]

for product in products:
    response = requests.post(API_URL, json=product)
    if response.status_code == 200:
        print(f"✓ Eklendi: {product['name']}")
    else:
        print(f"✗ Hata ({response.status_code}): {product['name']} - {response.text}")

print("Bitti!")