\# Otomatik Güvenlik Denetim Aracı



Python ile geliştirilmiş, SSH üzerinden uzak Linux sistemlere bağlanarak otomatik güvenlik denetimi yapan ve sonuçları PDF raporu olarak sunan bir araç.



\## Özellikler



\- SSH ile uzak sisteme otomatik bağlantı (Paramiko)

\- 6 kritik güvenlik kontrolü:

&#x20; - SSH Root Login yapılandırması

&#x20; - Telnet servisi kontrolü

&#x20; - Açık port sayısı

&#x20; - Disk doluluk oranı

&#x20; - Bekleyen sistem güncellemeleri

&#x20; - Aktif kullanıcı sayısı

\- Otomatik risk skorlama (KRİTİK / YÜKSEK / ORTA / TEMİZ)

\- JSON formatında makine okunabilir rapor

\- ReportLab ile profesyonel PDF raporu



\## Kullanılan Teknolojiler



\- Python 3

\- Paramiko (SSH bağlantısı)

\- ReportLab (PDF üretimi)



\## Kurulum



```bash

pip install paramiko reportlab

```



\## Kullanım



`guvenlik\_denetim.py` dosyasında bağlantı bilgilerini girin:



```python

HOST = "hedef\_ip"

PORT = 22

USER = "kullanici\_adi"

PASS = "sifre"

```



Çalıştırın:



```bash

python guvenlik\_denetim.py

python pdf\_rapor.py

```



\## Çıktılar



\- `denetim\_raporu.json` — ham denetim verisi

\- `guvenlik\_denetim\_raporu.pdf` — görsel PDF raporu



\## Geliştirme Planı



\- \[ ] Netmiko ile Cisco router desteği

\- \[ ] 15 Cisco güvenlik kontrolü (ACL, NTP, banner vb.)

\- \[ ] GNS3 topoloji entegrasyonu

