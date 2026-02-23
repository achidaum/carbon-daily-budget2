import streamlit as st

# 1. ตั้งค่าหน้าตาเว็บ
st.set_page_config(page_title="Carbon Budget", page_icon="🌱")
st.title("🌱 My Daily Carbon Budget")
st.write("เป้าหมาย: ใช้ไม่เกิน **10.0 แต้ม** ต่อวัน")

# 2. ฐานข้อมูลค่าคาร์บอน (ปรับแก้ตัวเลขตรงนี้ได้เลย)
factors = {
    "🚗 ขับรถน้ำมัน (กม.)": 0.20,
    "🚆 รถไฟฟ้า (กม.)": 0.04,
    "🥩 เนื้อวัว (จาน)": 3.50,
    "🐷 เนื้อหมู/ไก่ (จาน)": 1.00,
    "❄️ เปิดแอร์ (ชม.)": 0.45
}

# 3. ระบบจำข้อมูลชั่วคราว (Session State)
if 'used' not in st.session_state:
    st.session_state.used = 0.0
if 'logs' not in st.session_state:
    st.session_state.logs = []

# 4. ส่วนคำนวณและแสดงผล
budget = 10.0
remaining = budget - st.session_state.used

# แสดงตัวเลขแบบ Dashboard
c1, c2 = st.columns(2)
c1.metric("แต้มคงเหลือ", f"{remaining:.2f}")
c2.metric("ใช้ไปแล้ว", f"{st.session_state.used:.2f}")

# แถบพลังงาน (Progress Bar)
progress_val = max(0.0, min(remaining / budget, 1.0))
st.progress(progress_val)

# 5. ฟอร์มกรอกข้อมูล
st.subheader("➕ บันทึกกิจกรรม")
with st.form("carbon_form"):
    act = st.selectbox("เลือกกิจกรรม", list(factors.keys()))
    num = st.number_input("จำนวน (กม./จาน/ชม.)", min_value=0.0)
    submit = st.form_submit_button("บันทึก")
    
    if submit and num > 0:
        p = factors[act] * num
        st.session_state.used += p
        st.session_state.logs.append(f"{act} {num} หน่วย: -{p:.2f} แต้ม")
        st.rerun()

# 6. ประวัติ
st.subheader("📜 ประวัติวันนี้")
for l in reversed(st.session_state.logs):
    st.text(l)

if st.button("ล้างข้อมูลวันใหม่"):
    st.session_state.used = 0.0
    st.session_state.logs = []
    st.rerun()
