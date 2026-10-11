{
    "name": "SIRITA Ma'had Gate Scan — Validator Pos Satpam",
    "version": "20.0.1.0",
    "category": "Education / Hostel Security",
    "summary": "Web Scanner Kamera QR Code Pos Satpam & Integrasi Kartu Perizinan Portal Mahasantri",
    "description": """
        Modul khusus Pos Satpam Ma'had Al-Jami'ah untuk:
        - Halaman Web Scanner Kamera Satpam (/mahad/satpam/scan)
        - Verifikasi otomatis status perizinan pesiar / bermalam
        - Pencatatan otomatis waktu keluar & kembali (Check-out / Check-in)
        - Penampilan Kartu QR Code resmi di Portal Mahasantri (/my/permits)
    """,
    "author": "sufyALDI / TIPD IAIN Parepare",
    "website": "https://tipd.iainpare.ac.id",
    "depends": [
        "base",
        "web",
        "portal",
        "sirita_mahad",
        "sirita_mahad_pembinaan",
        "sirita_mahad_portal"
    ],
    "data": [
        "security/satpam_security.xml",
        "views/satpam_scan_templates.xml",
        "views/portal_qr_templates.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
