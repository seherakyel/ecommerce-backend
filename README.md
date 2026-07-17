# ecommerce-backend

## Proje yapısı

```
backend/
├── main.py           # Sunucu giriş noktası
├── database.py       # PostgreSQL bağlantısı
├── models.py         # Veritabanı tabloları
├── schemas.py        # API veri şekilleri
├── crud.py           # Veritabanı işlemleri
├── routers/
│   ├── products.py   # Ürün API
│   ├── cart.py       # Sepet API
│   └── orders.py     # Sipariş API
└── requirements.txt
```

## Çalıştırma

```bash
cd backend
source ../venv/bin/activate
python main.py
```

API dokümantasyonu: http://127.0.0.1:8000/docs
