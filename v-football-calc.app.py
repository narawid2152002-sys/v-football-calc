import streamlit as st

# ตั้งค่าหน้าจอแสดงผลให้เหมาะกับเบราว์เซอร์บนมือถือ
st.set_page_config(page_title="V-Football 12 Min Calculator", layout="centered")

st.title("⚽ เครื่องคำนวณผลบอลสด 12 นาที")
st.write("ระบบวิเคราะห์สกอร์และสเกลเวลาสำหรับฟุตบอลจำลอง")

# ส่วนที่ 1: เลือกโหมดการกรอกเวลา
time_mode = st.radio("เลือกรูปแบบการกรอกเวลา:", ["นาทีแข่งขันจริงในระบบ (0-12 นาที)", "นาทีสเกลบอร์ดจำลอง (0-90 นาที)"])

# ส่วนที่ 2: ฟอร์มรับข้อมูลจากผู้ใช้
with st.form("calc_form"):
    col1, col2 = st.columns(2)
    with col1:
        home_score = st.number_input("สกอร์ทีมเหย้า", min_value=0, value=0, step=1)
    with col2:
        away_score = st.number_input("สกอร์ทีมเยือน", min_value=0, value=0, step=1)
        
    if time_mode == "นาทีแข่งขันจริงในระบบ (0-12 นาที)":
        current_time = st.number_input("เวลาปัจจุบันของเกม (นาที)", min_value=0.0, max_value=12.0, value=5.0, step=0.5)
        sim_time_90 = current_time * 7.5
    else:
        sim_time_90 = st.number_input("เวลาที่แสดงบนหน้าจอ (นาทีสเกล 90)", min_value=0.0, max_value=90.0, value=39.0, step=1.0)
        current_time = sim_time_90 / 7.5

    ou_line = st.number_input("ราคา สูง/ต่ำ (Over/Under) ปัจจุบัน", min_value=0.0, value=5.5, step=0.25)
    
    submit_btn = st.form_submit_with_categorical_labels = st.form_submit_button("คำนวณและวิเคราะห์ผล")

# ส่วนที่ 3: การประมวลผลและการแสดงสถิติ
if submit_btn:
    total_goals = home_score + away_score
    
    # คำนวณอัตราเฉลี่ยการเกิดประตูต่อนาที (อิงเวลาจริง 12 นาที)
    if current_time > 0:
        goals_per_minute = total_goals / current_time
        projected_final_goals = goals_per_minute * 12
    else:
        goals_per_minute = 0
        projected_final_goals = 0

    st.markdown("---")
    st.subheader("📊 ผลลัพธ์การวิเคราะห์")
    
    # แสดงค่าเปรียบเทียบเวลา
    st.metric(label="เวลาจริงของระบบจำลอง (จาก 12 นาที)", value=f"{current_time:.2f} นาที")
    st.metric(label="สเกลเวลาฟุตบอลปกติ (จาก 90 นาที)", value=f"{sim_time_90:.1f}'")
    st.metric(label="จำนวนสกอร์รวมปัจจุบัน", value=f"{total_goals} ประตู")
    
    # ส่วนวิเคราะห์จังหวะเกม
    st.subheader("📈 แนวโน้มการทำประตู")
    if current_time > 0:
        st.write(f"⏱️ **ความเร็วการทำประตู:** มีประตูเกิดขึ้นเฉลี่ยทุกๆ **{current_time / max(total_goals, 1):.2f} นาที** (เวลาวิ่งจริง)")
        st.write(f"🔮 **คาดการณ์สกอร์รวมเมื่อจบเกม (12 นาที):** ประมาณ **{projected_final_goals:.2f} ประตู**")
        
        # เปรียบเทียบกับราคา สูง/ต่ำ
        if projected_final_goals > ou_line:
            st.success(f"💡 แนวโน้มปัจจุบัน: **สูงกว่า (Over)** ราคาตั้งต้น {ou_line}")
        elif projected_final_goals < ou_line:
            st.warning(f"💡 แนวโน้มปัจจุบัน: **ต่ำกว่า (Under)** ราคาตั้งต้น {ou_line}")
        else:
            st.info(f"💡 แนวโน้มปัจจุบัน: **เสมอตัว** กับราคาตั้งต้น {ou_line}")
    else:
        st.info("เริ่มเกมการแข่งขัน ระบบกำลังรอข้อมูลสถิติเวลา")
      
