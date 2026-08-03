import requests

BASE = "http://127.0.0.1:8000"

category_tree = {
    "Mobilya": {
        "Yatak Odası": ["Karyola & Yatak", "Gardırop", "Komodin", "Şifonyer", "Makyaj Masası"],
        "Oturma Grubu": ["Koltuk Takımı", "Köşe Koltuk", "Berjer", "Orta & Yan Sehpa"],
        "Yemek Odası": ["Yemek Masası", "Sandalye", "Konsol", "Vitrin"],
        "TV Ünitesi": [],
        "Genç Odası": ["Çalışma Masası", "Ranza & Yatak", "Gardırop"]
    },
    "Beyaz Eşya": {
        "Buzdolabı": ["Gardırop Tipi", "Çift Kapılı", "Büro Tipi"],
        "Çamaşır Makinesi": [],
        "Kurutma Makinesi": [],
        "Bulaşık Makinesi": [],
        "Pişirme Grubu": ["Ankastre Set", "Ankastre Fırın", "Ankastre Ocak", "Davlumbaz", "Mikrodalga Fırın", "Masaüstü Fırın"],
        "Klima & Isıtma": ["Inverter Klima", "Vantilatör"]
    },
    "Halı": {
        "Salon Halısı": ["Akrilik Halı", "Modern Halı"],
        "Yolluk & Koridor": ["Kesme Yolluk", "Kaymaz Taban Yolluk"],
        "Mutfak Halısı": []
    },
    "Perde": {
        "Fon Perde": [],
        "Tül Perde": [],
        "Stor & Zebra Perde": [],
        "Güneşlik": []
    },
    "Küçük Ev Aletleri": {
        "Süpürge": ["Dikey Süpürge", "Yatay Süpürge", "Robot Süpürge"],
        "Ütü": ["Buhar Kazanlı Ütü", "El Ütüsü", "Buharlı Ütü"],
        "Çay Makinesi": [],
        "Blender": ["El Blenderi", "Blender Seti", "Personal Blender"],
        "Semaver": [],
        "Mikser": ["El Mikseri", "Stand Mikser"],
        "Tost Makinesi": [],
        "Elektrikli Cezve": [],
        "Su Isıtıcı & Kettle": [],
        "Kahve Makinesi": ["Türk Kahvesi Makinesi", "Filtre Kahve Makinesi", "Espresso Makinesi"]
    },
    "Pişirme": {
        "Tencere & Tencere Setleri": ["Çelik Tencere Seti", "Granit Tencere Seti", "Döküm Tencere", "Düdüklü Tencere", "Tek Tencere"],
        "Tava & Tava Setleri": ["Granit Tava", "Döküm Tava", "Wok Tava", "Krep Tavası", "Sahan"],
        "Çaydanlıklar & Cezveler": ["Çelik Çaydanlık", "Granit Çaydanlık", "Cezve Seti"],
        "Fırın & Pişirme Kapları": ["Kek Kalıpları", "Döküm Kek Kalıbı", "Borcam & Cam Fırın Kabı"],
        "Hiper Setler": ["Çelik Tencere & Çaydanlık & Cezve Kombin Setleri"]
    },
    "Sofra": {
        "Yemek Takımları": ["12 Kişilik Yemek Takımı", "6 Kişilik Yemek Takımı", "Kahvaltı Takımı", "Pasta Takımı"],
        "Tabaklar & Sunum": ["Servis Tabağı", "Yemek Tabağı", "Çorba Kasesi", "Tatlı Tabağı", "Kayık Tabak", "Sunumluk & İkramlık"],
        "Çatal Bıçak Kaşık": ["12 Kişilik Takım", "6 Kişilik Takım", "Servis Setleri", "Tekli Çatal Bıçak"],
        "Bardak & Kadehler": ["Su Bardağı Seti", "Meşrubat Bardağı", "Kadeh Seti", "Çay Bardağı & Tabağı"],
        "Sofra Aksesuarları": ["Tuzluk & Biberlik", "Amerikan Servis & Supla", "Yağlık & Sirkelik", "Ekmeklik & Peçetelik"]
    },
    "Banyo": {
        "Havlular": ["El & Yüz Havlusu", "Banyo Havlusu", "Misafir Havlusu", "Ayak Havlusu", "Plaj Havlusu"],
        "Bornozlar": ["Bornoz Seti", "Kadın Bornoz", "Erkek Bornoz", "Çocuk Bornoz"],
        "Banyo Aksesuarları": ["Sabunluk & Fırçalık", "Çöp Kovası", "Çamaşır Sepeti"],
        "Banyo Paspasları": ["2'li Paspas Takımı", "Tekli Paspas"]
    },
    "Yatak Odası & Ev Tekstili": {
        "Nevresim Takımları": ["Çift Kişilik", "Tek Kişilik", "Battal Boy", "Bebek & Çocuk"],
        "Yatak Örtüsü & Pike": ["Yatak Örtüsü Seti", "Pike Seti", "Yatak Pedleri"],
        "Yorgan & Yastık": ["Silikon Yorgan", "Kaz Tüyü Yorgan", "Ortopedik Yastık", "Pamuk Yastık"]
    },
    "Ev & Yaşam": {
        "Oda Kokuları & Mumlar": ["Çubuklu Oda Kokusu", "Oda Spreyi", "Kokulu Mumlar", "Buhurdanlık"],
        "Kozmetik & Kişisel Bakım": ["Sıvı Sabun", "Kolonya", "El & Vücut Losyonu"],
        "Dekorasyon": ["Vazo", "Tablo", "Şamdan & Mumluk", "Dekoratif Objeler"]
    },
    "Çeyiz Setleri": {
        "Elektrikli Çeyiz Setleri": ["3'lü Mutfak Seti", "4'lü Mutfak Seti"],
        "Pişirme Çeyiz Setleri": ["Granit & Çelik Tencere Karma Setler"],
        "Yemek & Sofra Çeyiz Setleri": ["12 Kişilik Yemek Takımı & Çatal Bıçak Seti"],
        "Komple Evlilik Paketleri": ["Süper Evlilik Paketi", "Mini Çeyiz Seti"]
    }
}

# En alt seviye kategori adı -> id (ürünleri bağlamak için)
leaf_ids = {}

for main_name, subs in category_tree.items():
    res = requests.post(f"{BASE}/categories/", json={"name": main_name})
    main_id = res.json()["id"]
    print(f"✓ Ana: {main_name} (id: {main_id})")

    for sub_name, leaves in subs.items():
        res = requests.post(f"{BASE}/categories/", json={"name": sub_name, "parent_id": main_id})
        sub_id = res.json()["id"]
        leaf_ids[sub_name] = sub_id
        print(f"   ✓ Alt: {sub_name} (id: {sub_id})")

        for leaf_name in leaves:
            res = requests.post(f"{BASE}/categories/", json={"name": leaf_name, "parent_id": sub_id})
            leaf_id = res.json()["id"]
            leaf_ids[leaf_name] = leaf_id
            print(f"      ✓ Alt-alt: {leaf_name} (id: {leaf_id})")

# Ürünler (en alt seviyeye bağlı)
products = [
    {"name": "Başlıklı Çift Kişilik Karyola", "description": "Depolu, modern", "price": 8999, "stock": 10, "leaf": "Karyola & Yatak", "image_url": "https://picsum.photos/seed/bed/400/400"},
    {"name": "4 Kapılı Gardırop", "description": "Aynalı", "price": 6499, "stock": 12, "leaf": "Gardırop", "image_url": "https://picsum.photos/seed/wardrobe/400/400"},
    {"name": "Üçlü Koltuk Takımı", "description": "Gri kumaş", "price": 18999, "stock": 8, "leaf": "Koltuk Takımı", "image_url": "https://picsum.photos/seed/sofa/400/400"},
    {"name": "6 Kişilik Yemek Masası", "description": "Ahşap, açılır", "price": 8499, "stock": 12, "leaf": "Yemek Masası", "image_url": "https://picsum.photos/seed/diningtable/400/400"},
    {"name": "Çift Kapılı Buzdolabı", "description": "500L, No-Frost", "price": 22999, "stock": 15, "leaf": "Çift Kapılı", "image_url": "https://picsum.photos/seed/fridge/400/400"},
    {"name": "Inverter Klima 12000 BTU", "description": "Sessiz, A++", "price": 16499, "stock": 18, "leaf": "Inverter Klima", "image_url": "https://picsum.photos/seed/ac/400/400"},
    {"name": "Akrilik Salon Halısı", "description": "160x230", "price": 2499, "stock": 30, "leaf": "Akrilik Halı", "image_url": "https://picsum.photos/seed/carpet/400/400"},
    {"name": "Robot Süpürge", "description": "Akıllı haritalama", "price": 7999, "stock": 20, "leaf": "Robot Süpürge", "image_url": "https://picsum.photos/seed/robot/400/400"},
    {"name": "Blender Seti 1000W", "description": "5 parça", "price": 1299, "stock": 35, "leaf": "Blender Seti", "image_url": "https://picsum.photos/seed/blender/400/400"},
    {"name": "Türk Kahvesi Makinesi", "description": "Otomatik", "price": 1499, "stock": 40, "leaf": "Türk Kahvesi Makinesi", "image_url": "https://picsum.photos/seed/coffee/400/400"},
    {"name": "Granit Tencere Seti", "description": "7 parça", "price": 3299, "stock": 25, "leaf": "Granit Tencere Seti", "image_url": "https://picsum.photos/seed/pot/400/400"},
    {"name": "12 Kişilik Yemek Takımı", "description": "Porselen", "price": 2799, "stock": 30, "leaf": "12 Kişilik Yemek Takımı", "image_url": "https://picsum.photos/seed/plates/400/400"},
    {"name": "Banyo Havlusu Seti", "description": "4 parça, pamuk", "price": 649, "stock": 50, "leaf": "Banyo Havlusu", "image_url": "https://picsum.photos/seed/towel/400/400"},
    {"name": "Çift Kişilik Nevresim", "description": "Saten, 4 parça", "price": 749, "stock": 50, "leaf": "Çift Kişilik", "image_url": "https://picsum.photos/seed/bedding/400/400"},
    {"name": "Süper Evlilik Paketi", "description": "Komple çeyiz", "price": 24999, "stock": 5, "leaf": "Süper Evlilik Paketi", "image_url": "https://picsum.photos/seed/dowry/400/400"},
]

for product in products:
    leaf_name = product.pop("leaf")
    product["category_id"] = leaf_ids.get(leaf_name)
    res = requests.post(f"{BASE}/products/", json=product)
    if res.status_code == 200:
        print(f"✓ Ürün: {product['name']}")
    else:
        print(f"✗ Hata: {product['name']} - {res.text}")

print("Bitti!")