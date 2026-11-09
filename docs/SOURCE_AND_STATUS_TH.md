# ที่มาและสถานะการย้าย ArtMath

อัปเดต: 9 พฤศจิกายน 2026 (Asia/Bangkok)

- ชุดต้นทาง: ArtMath-20261107T201219Z-1-001 ใน Google Drive ที่ผู้ใช้ระบุ
- โค้ดฐาน: CLI, renderer และ story editor ที่นำมาปรับและทดสอบในงานก่อนหน้า; baseline commit 07e7d7709d5f9dadd9f0dd70a6e566ffdf4d11c7 ของ repository เดิม
- Repository ปลายทางที่ผู้ใช้ระบุ: [mrkanchanawat-cmyk/artmath-cloud](https://github.com/mrkanchanawat-cmyk/artmath-cloud) โดยมี `main` เป็นฐาน และ `feat/mobile-cloud-foundation` เป็น branch ชุดงานสำหรับเปิด PR
- AGENTS.md เป็นคำสั่งหลัก; สเปกและคู่มือมือถือเป็นฉบับสรุปตามพฤติกรรมโค้ดปัจจุบัน ไม่ได้คัดลอกเอกสารส่วนตัวหรือบทเดิมทั้งชุด
- มีโค้ด คู่มือ แม่แบบเปล่า สคริปต์ติดตั้ง และตัวสร้างสื่อจำลอง ไม่มีเสียง/วิดีโอส่วนตัว ไม่มี token หรือ credentials

## สิ่งที่ยังต้องเชื่อมต่อ

เชื่อม GitHub ด้วยบัญชีเจ้าของ `mrkanchanawat-cmyk` แล้ว และ push `main` สำเร็จ Repository เป็น **Public** ชุดโค้ดที่จะส่งไม่มีสื่อส่วนตัวหรือ credentials

`main` เป็นฐานเริ่มต้น ส่วน `feat/mobile-cloud-foundation` รวมระบบและคู่มือสำหรับ PR เข้า `main` ตรวจ branch และสถานะ PR บน GitHub ก่อนเลือกใช้งาน ไม่ถือว่า `main` มีระบบครบจนกว่า PR จะ merge

พบ saved cloud environment ชื่อ maththewhat-hub1 อยู่ในบัญชี แต่ยังไม่ได้เปลี่ยนให้ใช้ repository ใหม่นี้ และยังไม่ได้ทดสอบเริ่ม task ใหม่บน environment นั้น การทดสอบ setup/demo ใน session นี้ไม่ใช่หลักฐานว่า environment ที่บันทึกไว้อัปเดตแล้ว

ขั้นเปิดใช้งาน: ตรวจ branch งานและ PR แล้วเพิ่มหรือเปลี่ยน repository ใน cloud environment เป็น `mrkanchanawat-cmyk/artmath-cloud` ระหว่างรอ merge เลือก `feat/mobile-cloud-foundation`; หลัง merge ใช้ `main` จากนั้นทดสอบเริ่ม task จากมือถือด้วย `setup_cloud.sh --check` และ `setup_cloud.sh --smoke-test`

## การใช้ GitHub และชุด Git สำรองบนเครื่องคลาวด์

เมื่อ remote มี branch งานแล้ว ให้ checkout จาก GitHub เป็นทางหลัก:

```bash
git clone -b feat/mobile-cloud-foundation https://github.com/mrkanchanawat-cmyk/artmath-cloud.git
cd artmath-cloud
bash scripts/setup_cloud.sh --check
```

หากเป็น workspace ใหม่และยังไม่มี `.venv` ให้รัน `bash scripts/setup_cloud.sh` ก่อนตรวจ ใช้ bundle ด้านล่างเฉพาะเมื่อต้องนำเข้าหรือกู้คืนประวัติที่เตรียมไว้

ไฟล์ artmath-cloud.bundle มีประวัติ main และ branch งาน ไม่มีสื่อส่วนตัว ใช้หลังดาวน์โหลด bundle เข้า workspace แล้ว:

```bash
git clone -b feat/mobile-cloud-foundation artmath-cloud.bundle artmath-cloud
cd artmath-cloud
git branch main origin/main
git remote rename origin bundle
# ตรวจสิทธิ์เข้าถึงและประวัติปลายทางก่อน push
git remote add origin https://github.com/mrkanchanawat-cmyk/artmath-cloud.git
git push -u origin main feat/mobile-cloud-foundation
```

เปิด PR จาก feat/mobile-cloud-foundation เข้า main ไม่ force-push หากปลายทางไม่ว่าง ให้ตรวจประวัติและรวมงานอย่างชัดเจนก่อน
