"""
generate_qr_codes.py — Standalone Production QR Code Generator for AI Health Assistant
Generates high-resolution PNG QR codes for:
1. Android Google Play Store
2. iOS Apple App Store
3. Public Web Application
4. All-in-One Download & Install Landing Page
5. 1-Click Emergency SOS Ambulance Link
"""

import os
from pathlib import Path
try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[!] Installing required dependencies: qrcode, pillow...")
    os.system("pip install qrcode pillow")
    import qrcode
    from PIL import Image, ImageDraw, ImageFont

# Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Output directory for QR code images
OUTPUT_DIR = Path(__file__).resolve().parent / "static" / "qr_codes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configurable URLs (Reads from environment variables with production fallbacks)
PUBLIC_WEB_URL = os.getenv("PUBLIC_WEB_URL", "https://app.yourdomain.com").rstrip("/")
ANDROID_STORE_URL = os.getenv(
    "ANDROID_STORE_URL",
    "https://play.google.com/store/apps/details?id=com.health.aiassistant"
)
IOS_STORE_URL = os.getenv(
    "IOS_STORE_URL",
    "https://apps.apple.com/app/ai-health-assistant/id6739271845"
)
DOWNLOAD_PORTAL_URL = f"{PUBLIC_WEB_URL}/download"
EMERGENCY_SOS_URL = f"{PUBLIC_WEB_URL}/ambulance"

QR_TARGETS = [
    {
        "filename": "qr_android_playstore.png",
        "title": "Android App (Google Play)",
        "url": ANDROID_STORE_URL,
        "color_dark": "#0f766e",  # Stethoscope Teal
        "color_light": "#ffffff",
        "subtitle": "Scan with Android phone"
    },
    {
        "filename": "qr_ios_appstore.png",
        "title": "iPhone / iPad (App Store)",
        "url": IOS_STORE_URL,
        "color_dark": "#0284c7",  # Sky Blue
        "color_light": "#ffffff",
        "subtitle": "Scan with iPhone camera"
    },
    {
        "filename": "qr_web_public.png",
        "title": "Public Web App (Any Device)",
        "url": PUBLIC_WEB_URL,
        "color_dark": "#1e293b",  # Slate Dark
        "color_light": "#ffffff",
        "subtitle": "Open in any web browser"
    },
    {
        "filename": "qr_download_portal.png",
        "title": "All-in-One Download Portal",
        "url": DOWNLOAD_PORTAL_URL,
        "color_dark": "#0d9488",  # Medical Green
        "color_light": "#ffffff",
        "subtitle": "Android + iOS + Web Portal"
    },
    {
        "filename": "qr_emergency_sos.png",
        "title": "1-Click Emergency SOS (108)",
        "url": EMERGENCY_SOS_URL,
        "color_dark": "#dc2626",  # Emergency Red
        "color_light": "#ffffff",
        "subtitle": "Rapid Ambulance Dispatch"
    }
]

def generate_branded_qr(target_info):
    """Generate high-resolution styled QR code image with title and subtitle labels"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(target_info["url"])
    qr.make(fit=True)

    # Base QR Code image
    qr_img = qr.make_image(
        fill_color=target_info["color_dark"],
        back_color=target_info["color_light"]
    ).convert("RGB")

    # Create canvas with header and footer banner
    canvas_w = qr_img.width + 40
    canvas_h = qr_img.height + 90
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#ffffff")
    draw = ImageDraw.Draw(canvas)

    # Paste QR in center
    canvas.paste(qr_img, (20, 45))

    # Add rounded border
    draw.rectangle([(2, 2), (canvas_w - 3, canvas_h - 3)], outline="#e2e8f0", width=3)

    # Top banner color line
    draw.rectangle([(2, 2), (canvas_w - 3, 8)], fill=target_info["color_dark"])

    # Draw Text Labels
    try:
        font_title = ImageFont.truetype("arial.ttf", 16)
        font_sub = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Title text
    title_text = target_info["title"]
    bbox_t = draw.textbbox((0, 0), title_text, font=font_title)
    text_w = bbox_t[2] - bbox_t[0]
    draw.text(((canvas_w - text_w) / 2, 18), title_text, fill="#0f172a", font=font_title)

    # Subtitle text
    sub_text = target_info["subtitle"]
    bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = bbox_s[2] - bbox_s[0]
    draw.text(((canvas_w - sub_w) / 2, canvas_h - 32), sub_text, fill="#64748b", font=font_sub)

    # Save to disk
    out_path = OUTPUT_DIR / target_info["filename"]
    canvas.save(out_path, quality=95)
    return out_path

def main():
    print("\n" + "="*70)
    print("🏥 AI HEALTH ASSISTANT — QR CODE GENERATOR")
    print("="*70)
    print(f"Output Directory: {OUTPUT_DIR}\n")

    for target in QR_TARGETS:
        out_file = generate_branded_qr(target)
        print(f"✅ Generated: {target['filename']}")
        print(f"   Target URL: {target['url']}")
        print(f"   Saved at  : {out_file}\n")

    print("="*70)
    print("✨ ALL QR CODES GENERATED SUCCESSFULLY!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
