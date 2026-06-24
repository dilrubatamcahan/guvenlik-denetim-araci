import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Türkçe font kaydı
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))

# JSON'dan veriyi oku
with open("denetim_raporu.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

# PDF dosyası
doc = SimpleDocTemplate(
    "guvenlik_denetim_raporu.pdf",
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

baslik_stili = ParagraphStyle("Baslik", fontSize=18, fontName="Arial-Bold",
                               textColor=colors.HexColor("#1a1a2e"), alignment=TA_CENTER, spaceAfter=6)
alt_baslik_stili = ParagraphStyle("AltBaslik", fontSize=11, fontName="Arial",
                                   textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=20)
bolum_stili = ParagraphStyle("Bolum", fontSize=13, fontName="Arial-Bold",
                              textColor=colors.HexColor("#16213e"), spaceBefore=15, spaceAfter=8)
normal_stili = ParagraphStyle("Normal", fontSize=10, fontName="Arial", spaceAfter=4)

RENKLER = {
    "KRITIK": colors.HexColor("#c0392b"),
    "YUKSEK": colors.HexColor("#e67e22"),
    "ORTA":   colors.HexColor("#f39c12"),
    "TEMIZ":  colors.HexColor("#27ae60"),
}

icerik = []

icerik.append(Spacer(1, 0.5*cm))
icerik.append(Paragraph("GÜVENLİK DENETİM RAPORU", baslik_stili))
icerik.append(Paragraph(f"Hedef Sistem: {veri['hedef']}  |  Tarih: {veri['tarih']}", alt_baslik_stili))
icerik.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e")))
icerik.append(Spacer(1, 0.4*cm))

ozet = veri["ozet"]
ozet_data = [
    ["KRİTİK", "YÜKSEK", "ORTA", "TEMİZ"],
    [str(ozet.get("KRITIK", 0)), str(ozet.get("YUKSEK", 0)),
     str(ozet.get("ORTA", 0)), str(ozet.get("TEMIZ", 0))]
]
ozet_tablo = Table(ozet_data, colWidths=[4*cm]*4)
ozet_tablo.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), colors.HexColor("#c0392b")),
    ("BACKGROUND", (1,0), (1,0), colors.HexColor("#e67e22")),
    ("BACKGROUND", (2,0), (2,0), colors.HexColor("#f39c12")),
    ("BACKGROUND", (3,0), (3,0), colors.HexColor("#27ae60")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,-1), "Arial-Bold"),
    ("FONTSIZE", (0,0), (-1,0), 11),
    ("FONTSIZE", (0,1), (-1,1), 22),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWHEIGHT", (0,0), (-1,0), 30),
    ("ROWHEIGHT", (0,1), (-1,1), 45),
    ("GRID", (0,0), (-1,-1), 1, colors.white),
    ("BACKGROUND", (0,1), (0,1), colors.HexColor("#fadbd8")),
    ("BACKGROUND", (1,1), (1,1), colors.HexColor("#fdebd0")),
    ("BACKGROUND", (2,1), (2,1), colors.HexColor("#fef9e7")),
    ("BACKGROUND", (3,1), (3,1), colors.HexColor("#d5f5e3")),
]))
icerik.append(Paragraph("ÖZET", bolum_stili))
icerik.append(ozet_tablo)
icerik.append(Spacer(1, 0.5*cm))

icerik.append(Paragraph("DENETİM BULGULARI", bolum_stili))
tablo_data = [["#", "Kontrol Adı", "Risk Seviyesi", "Detay"]]
for i, bulgu in enumerate(veri["bulgular"], 1):
    tablo_data.append([str(i), bulgu["kontrol"], bulgu["risk"], bulgu["detay"]])

tablo = Table(tablo_data, colWidths=[1*cm, 5*cm, 3*cm, 8*cm])
tablo_stili = [
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#16213e")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Arial-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Arial"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
    ("ALIGN", (2,0), (2,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ROWHEIGHT", (0,0), (-1,-1), 22),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
]
for i, bulgu in enumerate(veri["bulgular"], 1):
    renk = RENKLER.get(bulgu["risk"], colors.grey)
    tablo_stili.append(("TEXTCOLOR", (2,i), (2,i), renk))
    tablo_stili.append(("FONTNAME", (2,i), (2,i), "Arial-Bold"))

tablo.setStyle(TableStyle(tablo_stili))
icerik.append(tablo)

icerik.append(Spacer(1, 1*cm))
icerik.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
icerik.append(Spacer(1, 0.2*cm))
icerik.append(Paragraph(
    "Bu rapor Otomatik Güvenlik Denetim Aracı tarafından oluşturulmuştur. | Gizli",
    ParagraphStyle("AltNot", fontSize=8, fontName="Arial", textColor=colors.grey, alignment=TA_CENTER)
))

doc.build(icerik)
print("PDF rapor olusturuldu: guvenlik_denetim_raporu.pdf")