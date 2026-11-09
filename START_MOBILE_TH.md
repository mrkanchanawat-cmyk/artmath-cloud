# เริ่ม ArtMath จากมือถือ

Repository ปลายทางคือ [mrkanchanawat-cmyk/artmath-cloud](https://github.com/mrkanchanawat-cmyk/artmath-cloud) ใช้ GitHub เป็นแหล่งโค้ดและคำสั่งหลัก ส่วนวัตถุดิบและผลลัพธ์ตอนจริงเก็บใน Drive

เชื่อม GitHub ด้วยบัญชีเจ้าของ `mrkanchanawat-cmyk` แล้ว และส่ง `main` ขึ้น repository สำเร็จ Repository นี้เป็น Public จึงเก็บเฉพาะโค้ด คู่มือ และตัวอย่างจำลอง ตรวจสถานะ branch งานและ PR บน GitHub ก่อนเริ่ม

1. เลือกหรือเพิ่ม repository `mrkanchanawat-cmyk/artmath-cloud` ใน environment คลาวด์ หากใช้ environment เดิม `maththewhat-hub1` ต้องเปลี่ยนหรือเพิ่ม repository นี้อย่างชัดเจน และตรวจว่าการเชื่อม GitHub เข้าถึงได้ ไม่ถือว่า repository จะตามมาจากแชตเดิม
2. ตรวจว่า remote มี branch `feat/mobile-cloud-foundation` ซึ่งรวม `AGENTS.md` และระบบ ArtMath ระหว่างรอ PR merge ให้เลือก branch นี้ เมื่อ PR merge แล้วจึงใช้ `main` พร้อมตรวจ branch/commit ทุกงาน
3. จากโฟลเดอร์ repository ในเครื่องคลาวด์ รัน `bash scripts/setup_cloud.sh` แล้ว `bash scripts/setup_cloud.sh --smoke-test` ตรวจผลลัพธ์ก่อนนำสื่อจริงเข้า
4. บันทึก/publish การตั้งค่า environment ตามหน้าจอที่บัญชีรองรับ แล้วเริ่ม task ใหม่จากมือถือโดยเลือก environment นี้ รัน `bash scripts/setup_cloud.sh --check` เพื่อยืนยันความพร้อม
5. ใช้ `AGENTS.md` เป็นคำสั่งหลัก และ `docs/MOBILE_WORKFLOW_TH.md` เป็นคู่มือประจำ เริ่มตอนจริงด้วย HANDOFF ส่วนตัวของตอนนั้น

ข้อความสำหรับเริ่ม task บนมือถือ:

> ใช้ repository mrkanchanawat-cmyk/artmath-cloud บน Codex Cloud เลือก feat/mobile-cloud-foundation หาก PR ยังไม่ merge หรือ main หลัง merge อ่าน AGENTS.md สเปก และคู่มือมือถือ ตรวจ environment ด้วย setup_cloud.sh --check ถ้าขาด dependency ให้รัน setup จากนั้นทดสอบสื่อจำลองก่อนรับงานจริง สรุป commit ผลตรวจ และจุดที่ยังต้องตั้งค่า ไม่ใช้ไฟล์จากคอมเครื่องเดิม

หากไม่พบ branch งาน ให้ตรวจสิทธิ์และสถานะ push/PR บน GitHub ก่อน ดู [สถานะการย้ายและการใช้ Git bundle](docs/SOURCE_AND_STATUS_TH.md) สำหรับการกู้คืนชุดส่งต่อ ไม่ force-push ทับประวัติที่มีอยู่

ไฟล์วัตถุดิบและผลลัพธ์จริงเก็บใน Drive ตามเดิม การเชื่อมรับ–ส่ง Drive อัตโนมัติยังเป็นขั้นถัดไป
