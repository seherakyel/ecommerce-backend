import requests

BASE = "http://127.0.0.1:8000"

# Ana kategoriler ve alt kategorileri
category_tree = {
    "Mobilya": ["Yatak Odası", "Oturma Odası", "Yemek Odası"],
    "Beyaz Eşya": ["Buzdolabı", "Çamaşır Makinesi", "Bulaşık Makinesi"],
    "Klima": ["Split Klima", "Salon Tipi Klima"],
    "Halı": ["Salon Halısı", "Yolluk"],
    "Perde": ["Fon Perde", "Tül Perde"],
    "Küçük Ev Aletleri": ["Blender", "Süpürge"],
    "Nevresim Takımları": ["Çift Kişilik", "Tek Kişilik"],
    "Çeyiz Setleri": ["Havlu Seti", "Komple Set"],
}

sub_ids = {}

for main_name, subs in category_tree.items():
    res = requests.post(f"{BASE}/categories/", json={"name": main_name})
    main_id = res.json()["id"]
    print(f"✓ Ana kategori: {main_name} (id: {main_id})")

    for sub_name in subs:
        res = requests.post(f"{BASE}/categories/", json={"name": sub_name, "parent_id": main_id})
        sub_id = res.json()["id"]
        sub_ids[sub_name] = sub_id
        print(f"   ✓ Alt kategori: {sub_name} (id: {sub_id})")

products = [
    {"name": "Çift Kişilik Karyola", "description": "Başlıklı, depolu", "price": 8999, "stock": 10, "sub": "Yatak Odası", "image_url": "https://picsum.photos/seed/bed/400/400"},
    {"name": "Üçlü Koltuk", "description": "Gri kumaş, modern", "price": 18999, "stock": 8, "sub": "Oturma Odası", "image_url": "https://picsum.photos/seed/sofa/400/400"},
    {"name": "6 Kişilik Yemek Masası", "description": "Ahşap, açılır", "price": 8499, "stock": 12, "sub": "Yemek Odası", "image_url": "https://picsum.photos/seed/diningtable/400/400"},
    {"name": "No-Frost Buzdolabı", "description": "500L, A+++", "price": 22999, "stock": 15, "sub": "Buzdolabı", "image_url": "https://picsum.photos/seed/fridge/400/400"},
    {"name": "9 kg Çamaşır Makinesi", "description": "A+++ enerji", "price": 14999, "stock": 20, "sub": "Çamaşır Makinesi", "image_url": "https://picsum.photos/seed/washer/400/400"},
    {"name": "12000 BTU Split Klima", "description": "Inverter, sessiz", "price": 16499, "stock": 18, "sub": "Split Klima", "image_url": "https://picsum.photos/seed/ac/400/400"},
    {"name": "Salon Halısı 160x230", "description": "Yumuşak doku", "price": 2499, "stock": 30, "sub": "Salon Halısı", "image_url": "https://picsum.photos/seed/carpet/400/400"},
    {"name": "Kadife Fon Perde", "description": "Koyu yeşil", "price": 899, "stock": 40, "sub": "Fon Perde", "image_url": "https://picsum.photos/seed/curtain/400/400"},
    {"name": "1000W Blender Seti", "description": "5 parça", "price": 1299, "stock": 35, "sub": "Blender", "image_url": "https://picsum.photos/seed/blender/400/400"},
    {"name": "Kablosuz Süpürge", "description": "Güçlü emiş", "price": 3799, "stock": 25, "sub": "Süpürge", "image_url": "https://picsum.photos/seed/vacuum/400/400"},
    {"name": "Pamuk Saten Nevresim", "description": "Çift kişilik, 4 parça", "price": 749, "stock": 50, "sub": "Çift Kişilik", "image_url": "https://picsum.photos/seed/bedding/400/400"},
    {"name": "40 Parça Çeyiz Seti", "description": "Komple", "price": 4999, "stock": 15, "sub": "Komple Set", "image_url": "https://picsum.photos/seed/dowry/400/400"},
]

for product in products:
    sub_name = product.pop("sub")
    product["category_id"] = sub_ids.get(sub_name)
    res = requests.post(f"{BASE}/products/", json=product)
    if res.status_code == 200:
        print(f"✓ Ürün: {product['name']}")
    else:
        print(f"✗ Hata: {product['name']} - {res.text}")

print("Bitti!")