import paramiko
import json
from datetime import datetime

HOST = "127.0.0.1"
PORT = 2222
USER = "dilruba"
PASS = "buraya_vm_sifren"

def komut_calistir(ssh, komut):
    stdin, stdout, stderr = ssh.exec_command(komut)
    return stdout.read().decode().strip()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS)

print("=" * 55)
print("  OTOMATIK GUVENLIK DENETIM ARACI")
print(f"  Hedef: {HOST} | Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 55)

bulgular = []

# --- KONTROL 1: SSH Root Login ---
cikti = komut_calistir(ssh, "grep PermitRootLogin /etc/ssh/sshd_config")
if "yes" in cikti.lower():
    risk = "KRITIK"
elif "prohibit-password" in cikti.lower():
    risk = "ORTA"
else:
    risk = "TEMIZ"
bulgular.append({"kontrol": "SSH Root Login", "risk": risk, "detay": cikti})

# --- KONTROL 2: Telnet ---
cikti = komut_calistir(ssh, "ss -tlnp | grep ':23'")
risk = "KRITIK" if cikti else "TEMIZ"
bulgular.append({"kontrol": "Telnet Servisi", "risk": risk, "detay": "Telnet ACIK" if cikti else "Telnet kapali"})

# --- KONTROL 3: Acik port sayisi ---
cikti = komut_calistir(ssh, "ss -tlnp | grep LISTEN | wc -l")
sayi = int(cikti) if cikti.isdigit() else 0
risk = "YUKSEK" if sayi > 10 else "ORTA" if sayi > 5 else "TEMIZ"
bulgular.append({"kontrol": "Acik Port Sayisi", "risk": risk, "detay": f"{sayi} port dinleniyor"})

# --- KONTROL 4: Disk dolulugu ---
cikti = komut_calistir(ssh, "df / | tail -1 | awk '{print $5}'")
yuzde = int(cikti.replace("%", "")) if "%" in cikti else 0
risk = "KRITIK" if yuzde > 90 else "YUKSEK" if yuzde > 80 else "ORTA" if yuzde > 70 else "TEMIZ"
bulgular.append({"kontrol": "Disk Dolulugu", "risk": risk, "detay": f"Disk kullanimi: {yuzde}%"})

# --- KONTROL 5: Guncel sistem ---
cikti = komut_calistir(ssh, "apt list --upgradable 2>/dev/null | wc -l")
sayi = int(cikti) - 1 if cikti.isdigit() else 0
risk = "YUKSEK" if sayi > 20 else "ORTA" if sayi > 5 else "TEMIZ"
bulgular.append({"kontrol": "Bekleyen Guncellemeler", "risk": risk, "detay": f"{sayi} guncelleme bekliyor"})

# --- KONTROL 6: Aktif kullanici ---
cikti = komut_calistir(ssh, "who | wc -l")
sayi = int(cikti) if cikti.isdigit() else 0
risk = "ORTA" if sayi > 2 else "TEMIZ"
bulgular.append({"kontrol": "Aktif Kullanici Sayisi", "risk": risk, "detay": f"{sayi} kullanici aktif"})

ssh.close()

# --- RAPORU YAZDIR ---
sayac = {"KRITIK": 0, "YUKSEK": 0, "ORTA": 0, "TEMIZ": 0}
print("\nDENETIM SONUCLARI:")
print("-" * 55)
for b in bulgular:
    r = b["risk"]
    sayac[r] = sayac.get(r, 0) + 1
    print(f"  [{r:8}] {b['kontrol']}")
    print(f"             {b['detay']}\n")

print("=" * 55)
print(f"  OZET: KRITIK:{sayac['KRITIK']}  YUKSEK:{sayac['YUKSEK']}  ORTA:{sayac['ORTA']}  TEMIZ:{sayac['TEMIZ']}")
print("=" * 55)

# --- JSON RAPOR ---
rapor = {
    "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "hedef": HOST,
    "ozet": sayac,
    "bulgular": bulgular
}
with open("denetim_raporu.json", "w") as f:
    json.dump(rapor, f, indent=4, ensure_ascii=False)

print("\nRapor denetim_raporu.json dosyasina kaydedildi.")