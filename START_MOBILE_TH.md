# เริ่ม ArtMath จากมือถือ

ชุดนี้เตรียมโค้ดและคำสั่งสำหรับ Codex Cloud แล้ว แต่ยังไม่ได้สร้าง repository ใหม่บน GitHub เพราะคำสั่งสร้างได้รับ Forbidden

1. สร้าง repository ว่างแบบ Private ชื่อ `artmath-cloud` ที่ https://github.com/new โดยไม่เพิ่ม README แล้วให้การเชื่อม GitHub ของ Codex เข้าถึง repo นี้
2. ส่ง URL repository ให้ผู้ช่วย push `main` และ `feat/mobile-cloud-foundation` จาก Git bundle ที่แนบ แล้วเปิด PR เข้า main
3. ในการตั้งค่า environment คลาวด์ เพิ่ม repository ใหม่นี้ เลือก branch งานระหว่างรอ PR merge แล้วติดตั้งด้วย `bash scripts/setup_cloud.sh`
4. ทดสอบ `bash scripts/setup_cloud.sh --smoke-test` และตรวจไฟล์ผลลัพธ์ก่อนนำสื่อจริงเข้า
5. ใช้ `AGENTS.md` เป็นคำสั่งหลัก และ `docs/MOBILE_WORKFLOW_TH.md` เป็นคู่มือประจำ

ข้อความสำหรับเริ่ม task บนมือถือ:

> ใช้ repository artmath-cloud และ branch ที่มี AGENTS.md อ่านคำสั่งหลัก สเปก และคู่มือมือถือ ตรวจ environment ด้วย setup_cloud.sh --check ถ้าขาด dependency ให้รัน setup จากนั้นทดสอบสื่อจำลองก่อนรับงานจริง สรุป commit ผลตรวจ และจุดที่ยังต้องตั้งค่า ไม่ใช้ไฟล์จากคอมเครื่องเดิม

ไฟล์วัตถุดิบและผลลัพธ์จริงเก็บใน Drive ตามเดิม การเชื่อมรับ–ส่ง Drive อัตโนมัติยังเป็นขั้นถัดไป
