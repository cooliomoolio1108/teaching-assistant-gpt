import streamlit as st
from components.admin import CourseDetails

def render(datalist: list, embed: callable):
    if isinstance(datalist, list):
        for data in datalist:
            if isinstance(data, dict):
                with st.container():
                    cols = st.columns([3, 2, 2, 2, 1])
                    cols[0].markdown(f"📘 **{data['course_name']}**  \n`{data['course_code']}`")
                    cols[1].markdown(f"👤 {data['coordinator']}")
                    cols[2].markdown(f"📅 Sem: `{data['sem']}`")
                    cols[3].markdown(f"🕒 Created: `{data['created_at'][:29]}`")
                    if cols[4].button("Manage", key=f'course_{data}'):
                        st.query_params.update({"course_id":data['id']})
                        return data['id']
                st.markdown("---")
                st.markdown("<br>", unsafe_allow_html=True)  # ⬅ extra spacing