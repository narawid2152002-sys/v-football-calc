import streamlit as st

# 1. ตั้งค่าหน้าจอแสดงผล
st.set_page_config(page_title="V-Football Calculator", layout="centered")

st.title("⚽ เครื่องคำนวณผลบอลสด 12 นาที")
st.write("ระบบวิเคราะห์สกอร์และสเกลเวลาสำหรับฟุตบอลจำลอง")

# 2. เลือกโหมดเวลา
time_mode = st.radio("เลือกรูปแบบการกรอกเวลา:", ["นาทีแข่งขันจริงในระบบ (0-12 นาที)", "นาทีสเกลบอร์ดจำลอง (0-90 นาที)"])

# 3. สร้างฟอร์มรับข้อมูล
with st.form(key="calc_form"):
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
    
    # ปุ่มกดส่งข้อมูลที่ถูกต้องตามโครงสร้าง Streamlit
    submit_btn = st.form_submit_button(label="คำนวณและวิเคราะห์ผล")

# 4. ประมวลผลเมื่อกดปุ่ม
if submit_btn:
    total_goals = home_score + away_score
    
    if current_time > 0:
        goals_per_minute = total_goals / current_time
        projected_final_goals = goals_per_minute * 12
    else:
        goals_per_minute = 0
        projected_final_goals = 0

    st.markdown("---")
    st.subheader("📊 ผลลัพธ์การวิเคราะห์")
    
    st.metric(label="เวลาจริงของระบบจำลอง (จาก 12 นาที)", value=f"{current_time:.2f} นาที")
    st.metric(label="สเกลเวลาฟุตบอลปกติ (จาก 90 นาที)", value=f"{sim_time_90:.1f}'")
    st.metric(label="จำนวนสกอร์รวมปัจจุบัน", value=f"{total_goals} ประตู")
    
    st.subheader("📈 แนวโน้มการทำประตู")
    if current_time > 0:
        st.write(f"⏱️ **ความเร็วการทำประตู:** มีประตูเกิดขึ้นเฉลี่ยทุกๆ **{current_time / max(total_goals, 1):.2f} นาที** (เวลาวิ่งจริง)")
        st.write(f"🔮 **คาดการณ์สกอร์รวมเมื่อจบเกม (12 นาที):** ประมาณ **{projected_final_goals:.2f} ประตู**")
        
        if projected_final_goals > ou_line:
            st.success(f"💡 แนวโน้มปัจจุบัน: **สูงกว่า (Over)** ราคาตั้งต้น {ou_line}")
        elif projected_final_goals < ou_line:
            st.warning(f"💡 แนวโน้มปัจจุบัน: **ต่ำกว่า (Under)** ราคาตั้งต้น {ou_line}")
        else:
            st.info(f"💡 แนวโน้มปัจจุบัน: **เสมอตัว** กับราคาตั้งต้น {ou_line}")
    else:
        st.info("เริ่มเกมการแข่งขัน ระบบกำลังรอข้อมูลสถิติเวลา")
        
