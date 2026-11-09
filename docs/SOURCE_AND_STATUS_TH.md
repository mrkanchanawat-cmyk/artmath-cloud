# ที่มาและสถานะการย้าย ArtMath

อัปเดต: 9 พฤศจิกายน 2026 (Asia/Bangkok)

- ชุดต้นทาง: ArtMath-20261107T201219Z-1-001 ใน Google Drive ที่ผู้ใช้ระบุ
- โค้ดฐาน: CLI, renderer และ story editor ที่นำมาปรับและทดสอบในงานก่อนหน้า; baseline commit 07e7d7709d5f9dadd9f0dd70a6e566ffdf4d11c7 ของ repository เดิม
- ชุดนี้แยกเป็น repository ใหม่ชื่อที่เสนอ `artmath-cloud` โดยมี main และ feat/mobile-cloud-foundation สำหรับเปิด PR
- AGENTS.md เป็นคำสั่งหลัก; สเปกและคู่มือมือถือเป็นฉบับสรุปตามพฤติกรรมโค้ดปัจจุบัน ไม่ได้คัดลอกเอกสารส่วนตัวหรือบทเดิมทั้งชุด
- มีโค้ด คู่มือ แม่แบบเปล่า สคริปต์ติดตั้ง และตัวสร้างสื่อจำลอง ไม่มีเสียง/วิดีโอส่วนตัว ไม่มี token หรือ credentials

## สิ่งที่ยังต้องเชื่อมต่อ

การสร้าง repository ใหม่ผ่าน GitHub API ใน session นี้ถูกปฏิเสธด้วย Forbidden จึงยังไม่มี URL repository ใหม่หรือ PR ใหม่บน GitHub ชุด main/branch ที่ส่งมอบเป็นประวัติ Git ที่เตรียมไว้เพื่อ push เมื่อมีปลายทางที่ได้รับสิทธิ์แล้ว

พบ saved cloud environment ชื่อ maththewhat-hub1 อยู่ในบัญชี แต่ยังไม่ได้เปลี่ยนให้ใช้ repository ใหม่นี้ และยังไม่ได้ทดสอบเริ่ม task ใหม่บน environment นั้น การทดสอบ setup/demo ใน session นี้ไม่ใช่หลักฐานว่า environment ที่บันทึกไว้อัปเดตแล้ว

ขั้นต่อไป: สร้าง repository ว่างแบบ Private ชื่อ artmath-cloud ในบัญชีที่ต้องการ ให้การเชื่อม GitHub ของ Codex เข้าถึง repository นี้ แล้วส่ง URL กลับมาเพื่อ push main/branch และเปิด PR จากนั้นเพิ่ม repository นี้ใน cloud environment และทดสอบรับงานจากมือถือ

## การเปิดชุด Git บนเครื่องคลาวด์

ไฟล์ artmath-cloud.bundle มีประวัติ main และ branch งาน ไม่มีสื่อส่วนตัว ใช้หลังดาวน์โหลด bundle เข้า workspace แล้ว:

```bash
git clone -b feat/mobile-cloud-foundation artmath-cloud.bundle artmath-cloud
cd artmath-cloud
git branch main origin/main
git remote rename origin bundle
# แทน OWNER ด้วยบัญชีเจ้าของจริง และตรวจสิทธิ์เข้าถึงก่อน push
git remote add origin https://github.com/OWNER/artmath-cloud.git
git push -u origin main feat/mobile-cloud-foundation
```

เปิด PR จาก feat/mobile-cloud-foundation เข้า main ไม่ force-push หากปลายทางไม่ว่าง ให้ตรวจประวัติและรวมงานอย่างชัดเจนก่อน
