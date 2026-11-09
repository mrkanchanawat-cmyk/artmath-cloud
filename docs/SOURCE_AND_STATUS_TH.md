# ที่มาและสถานะการย้าย ArtMath

อัปเดต: 9 พฤศจิกายน 2026 (Asia/Bangkok)

- ชุดต้นทาง: ArtMath-20261107T201219Z-1-001 ใน Google Drive ที่ผู้ใช้ระบุ
- โค้ดฐาน: CLI, renderer และ story editor ที่นำมาปรับและทดสอบในงานก่อนหน้า; baseline commit 07e7d7709d5f9dadd9f0dd70a6e566ffdf4d11c7 ของ repository เดิม
- Repository ปลายทางที่ผู้ใช้ระบุ: [mrkanchanawat-cmyk/artmath-cloud](https://github.com/mrkanchanawat-cmyk/artmath-cloud) โดยมี `main` เป็นฐาน และ `feat/mobile-cloud-foundation` เป็น branch ชุดงานสำหรับเปิด PR
- AGENTS.md เป็นคำสั่งหลัก; สเปกและคู่มือมือถือเป็นฉบับสรุปตามพฤติกรรมโค้ดปัจจุบัน ไม่ได้คัดลอกเอกสารส่วนตัวหรือบทเดิมทั้งชุด
- มีโค้ด คู่มือ แม่แบบเปล่า สคริปต์ติดตั้ง และตัวสร้างสื่อจำลอง ไม่มีเสียง/วิดีโอส่วนตัว ไม่มี token หรือ credentials

## สิ่งที่ยังต้องเชื่อมต่อ

ผู้ใช้สร้าง repository ปลายทางและส่ง URL แล้ว ตรวจพบว่า repository เป็น **Public และยังว่าง** การสร้างผ่าน API ที่เคยได้รับ Forbidden เป็นข้อจำกัดในขั้นก่อนหน้า ไม่ต้องสร้าง repository ซ้ำ

การ push `main` ได้รับ **403: permission denied to kissxsis57100-cpu** บัญชีที่เชื่อมอยู่มี `push=false` จึงยังไม่มี remote branch หรือ PR ใหม่ ชุด `main` และ `feat/mobile-cloud-foundation` พร้อมอยู่ใน Git bundle/พื้นที่ทำงานเท่านั้น

เพื่อดำเนินการต่อ ให้เชื่อม GitHub ของ Codex ด้วยบัญชีเจ้าของ `mrkanchanawat-cmyk` หรือให้สิทธิ์ Write แก่ `kissxsis57100-cpu` และตรวจว่า GitHub App เข้าถึง repository นี้ได้ จากนั้นตรวจสิทธิ์อีกครั้งก่อน push ไม่มีสื่อส่วนตัวหรือ credentials รวมอยู่ในชุดที่จะส่งขึ้น repository Public นี้

พบ saved cloud environment ชื่อ maththewhat-hub1 อยู่ในบัญชี แต่ยังไม่ได้เปลี่ยนให้ใช้ repository ใหม่นี้ และยังไม่ได้ทดสอบเริ่ม task ใหม่บน environment นั้น การทดสอบ setup/demo ใน session นี้ไม่ใช่หลักฐานว่า environment ที่บันทึกไว้อัปเดตแล้ว

ขั้นต่อไป: ให้การเชื่อม GitHub ของ Codex เข้าถึง repository นี้ ส่ง `main` และ branch งานขึ้น GitHub แล้วเปิด PR เข้า `main` จากนั้นเพิ่มหรือเปลี่ยน repository ใน cloud environment เป็น `mrkanchanawat-cmyk/artmath-cloud` ระหว่างรอ merge เลือก `feat/mobile-cloud-foundation`; หลัง merge ใช้ `main` แล้วทดสอบเริ่ม task จากมือถือด้วย setup --check และ --smoke-test

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
