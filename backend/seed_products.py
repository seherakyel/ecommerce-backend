import requests

BASE = "http://127.0.0.1:8000"

categories = [
    "Mobilya",
    "Beyaz Eşya",
    "Klima",
    "Halı",
    "Perde",
    "Küçük Ev Aletleri",
    "Nevresim Takımları",
    "Çeyiz Setleri",
]

category_ids = {}

for name in categories:
    response = requests.post(f"{BASE}/categories/", json={"name": name})
    if response.status_code == 200:
        data = response.json()
        category_ids[name] = data["id"]
        print(f"✓ Kategori eklendi: {name} (id: {data['id']})")
    else:
        print(f"✗ Kategori hatası: {name} - {response.text}")

# Sonra ürünleri kategorileriyle ekle
products = [
    {"name": "Üçlü Koltuk Takımı", "description": "Modern tasarım, gri kumaş", "price": 18999, "stock": 10, "category": "Mobilya", "image_url": "https://picsum.photos/seed/sofa/400/400"},
    {"name": "Yemek Masası", "description": "6 kişilik, ahşap", "price": 8499, "stock": 15, "category": "Mobilya", "image_url": "https://picsum.photos/seed/table/400/400"},
    {"name": "Çamaşır Makinesi", "description": "9 kg, A+++ enerji", "price": 14999, "stock": 20, "category": "Beyaz Eşya", "image_url": "https://picsum.photos/seed/washer/400/400"},
    {"name": "Buzdolabı", "description": "No-Frost, 500L", "price": 22999, "stock": 12, "category": "Beyaz Eşya", "image_url": "https://picsum.photos/seed/fridge/400/400"},
    {"name": "Split Klima", "description": "12000 BTU, inverter", "price": 16499, "stock": 18, "category": "Klima", "image_url": "https://picsum.photos/seed/ac/400/400"},
    {"name": "Salon Halısı", "description": "160x230, yumuşak doku", "price": 2499, "stock": 30, "category": "Halı", "image_url": "https://picsum.photos/seed/carpet/400/400"},
    {"name": "Fon Perde", "description": "Kadife, koyu yeşil", "price": 899, "stock": 40, "category": "Perde", "image_url": "https://picsum.photos/seed/curtain/400/400"},
    {"name": "Blender Seti", "description": "1000W, 5 parça", "price": 1299, "stock": 35, "category": "Küçük Ev Aletleri", "image_url": "https://picsum.photos/seed/blender/400/400"},
    {"name": "Elektrikli Süpürge", "description": "Kablosuz, güçlü emiş", "price": 3799, "stock": 25, "category": "Küçük Ev Aletleri", "image_url": "https://picsum.photos/seed/vacuum/400/400"},
    {"name": "Çift Kişilik Nevresim", "description": "Pamuk saten, 4 parça", "price": 749, "stock": 50, "category": "Nevresim Takımları", "image_url": "https://picsum.photos/seed/bedding/400/400"},
    {"name": "40 Parça Çeyiz Seti", "description": "Havlu ve nevresim dahil", "price": 4999, "stock": 15, "category": "Çeyiz Setleri", "image_url": "https://picsum.photos/seed/dowry/400/400"},
]

for product in products:
    category_name = product.pop("category")
    product["category_id"] = category_ids.get(category_name)
    response = requests.post(f"{BASE}/products/", json=product)
    if response.status_code == 200:
        print(f"✓ Ürün eklendi: {product['name']}")
    else:
        print(f"✗ Ürün hatası: {product['name']} - {response.text}")

print("Bitti!")