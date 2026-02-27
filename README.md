# Filo Yönetim Web Uygulaması

Modüler Flask + SQLite tabanlı filo yönetim sistemi.

## Özellikler
- Araç yönetimi (CRUD)
- Şoför yönetimi + işe gelmediği günler (CRUD)
- Birim yönetimi (CRUD)
- Trafik cezaları yönetimi
- Çek yönetimi
- FullCalendar ile tüm tarihli verilerin tek takvimde gösterimi
- Bugün görevleri ekranı (renk kodlamalı)
- JSON API endpointleri (`/api/events`, `/api/today-tasks`, `/api/vehicles`)

## Çalıştırma Talimatları
1. Python 3.11+ kurulu olmalı.
2. Sanal ortam oluşturun ve aktif edin:
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Windows: `.venv\\Scripts\\activate`)
3. Bağımlılıkları kurun:
   - `pip install -r requirements.txt`
4. Uygulamayı başlatın:
   - `python run.py`
5. Tarayıcıdan açın:
   - `http://localhost:5000`
