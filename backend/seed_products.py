import requests

BASE = "http://127.0.0.1:8000"

# Ana kategoriler ve alt kategorileri
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