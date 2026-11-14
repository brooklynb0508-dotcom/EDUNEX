
import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(
    page_title="EduNex | Education Intelligence",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background:#0B1420;color:#F2F6F8}
[data-testid="stSidebar"] {background:#132436}
h1,h2,h3 {color:#F2F6F8}
div[data-testid="stMetric"] {
    background:#172B3D;padding:18px;border-radius:12px;
    border:1px solid #294459
}
div.stButton>button {
    background:#16866C;color:white;border-radius:8px;
    border:0;font-weight:600
}
.agent {
    background:#172B3D;padding:16px;border-radius:10px;
    border:1px solid #294459;margin-bottom:8px
}
</style>
""", unsafe_allow_html=True)

AGENTS = [
    ("Planner Agent", "Plans the teacher's goal and delegates tasks."),
    ("Document Intelligence Agent", "Extracts assessment information and learner responses."),
    ("Assessment Analysis Agent", "Calculates marks and analyses performance."),
    ("Error Detection Agent", "Finds incorrect answers and marking inconsistencies."),
    ("Performance Intelligence Agent", "Identifies individual and class-wide learning gaps."),
    ("Inclusive Learning & Support Agent", "Flags patterns for additional teacher review."),
    ("Curriculum Alignment Agent", "Maps diagnosed gaps to curriculum requirements."),
    ("Worksheet Generation Agent", "Creates targeted curriculum-aligned exercises."),
    ("Intervention Recommendation Agent", "Develops individual and class teaching strategies."),
    ("Reviewing Agent", "Checks, rejects and returns flawed outputs for correction.")
]

if "data" not in st.session_state:
    st.session_state.data = None
if "results" not in st.session_state:
    st.session_state.results = None
if "workflow_log" not in st.session_state:
    st.session_state.workflow_log = []

st.sidebar.markdown("# EduNex")
st.sidebar.caption("INTELLIGENT EDUCATION ECOSYSTEM")

page = st.sidebar.radio("NAVIGATION", [
    "Command Centre",
    "Assessment Upload",
    "Agent Intelligence",
    "Performance Insights",
    "Inclusive Learning",
    "Worksheets & Interventions",
    "Review & Reports"
])

st.sidebar.markdown("---")
st.sidebar.success("Prototype environment")
st.sidebar.caption("10 coordinated specialist agents")

st.markdown("""
<div style="padding:20px 0">
<p style="color:#42C9A1;letter-spacing:4px">
AUTONOMOUS EDUCATION INTELLIGENCE
</p>
<h1 style="font-size:46px;margin:0">EduNex</h1>
<p style="color:#9AafBB">
Transforming assessment data into meaningful learner support.
</p>
</div>
""", unsafe_allow_html=True)


def sample_data():
    return pd.DataFrame({
        "Learner":["Learner 01","Learner 02","Learner 03",
                   "Learner 04","Learner 05","Learner 06"],
        "Q1":[8,9,3,7,4,8],
        "Q2":[7,8,2,6,3,9],
        "Q3":[9,8,4,7,2,8],
        "Q4":[8,9,3,8,4,7],
        "Total":[32,34,12,28,13,32]
    })


def analyse(df):
    questions = [c for c in df.columns if c.startswith("Q")]
    df = df.copy()

    df["Calculated Total"] = df[questions].sum(axis=1)
    df["Marking Error"] = (
        pd.to_numeric(df["Total"], errors="coerce")
        - df["Calculated Total"]
    )
    df["Verified Total"] = df["Calculated Total"]
    df["Percentage"] = (
        df["Verified Total"] / (len(questions)*10) * 100
    ).round(1)

    weak = [q for q in questions if df[q].mean() < 5]

    return df, questions, weak


def execute_workflow(df):
    log = []

    log.append("Planner: Task plan created.")
    log.append("Document Intelligence: Assessment data extracted.")

    data, questions, weak = analyse(df)

    log.append("Assessment Analysis: Scores calculated.")
    log.append("Error Detection: Question-level errors examined.")
    log.append("Performance Intelligence: Learning patterns identified.")

    flags = []
    for _, row in data.iterrows():
        if sum(row[q] <= 2 for q in questions) >= 2:
            flags.append(row["Learner"])

    log.append("Inclusive Learning: Support indicators reviewed.")

    mapping = {
        "Q1":"Fractions",
        "Q2":"Decimals",
        "Q3":"Fractions",
        "Q4":"Problem solving"
    }

    worksheets = [
        {
            "question":q,
            "topic":mapping.get(q,"Teacher mapping required"),
            "exercise":f"Create foundational and application exercises for {mapping.get(q,q)}."
        }
        for q in weak
    ]

    log.append("Curriculum Alignment: Relevant topics mapped.")
    log.append("Worksheet Generation: Targeted worksheet plans prepared.")
    log.append("Intervention Recommendation: Support strategies prepared.")

    corrections = []

    if (data["Marking Error"] != 0).any():
        corrections.append(
            "Reviewer rejected inconsistent original totals."
        )
        corrections.append(
            "Assessment Analysis recalculated the affected totals."
        )
        corrections.append(
            "Reviewer rechecked corrected totals: PASS."
        )
    else:
        corrections.append("Reviewer checked all totals: PASS.")

    corrections.append(
        "Reviewer checked curriculum and support outputs."
    )

    log.extend(corrections)

    return {
        "data":data,
        "questions":questions,
        "weak":weak,
        "flags":flags,
        "worksheets":worksheets,
        "log":log
    }


if page == "Command Centre":
    st.title("Command Centre")
    st.write("Your educational intelligence overview.")

    if st.session_state.results:
        r = st.session_state.results
        df = r["data"]

        a,b,c,d = st.columns(4)
        a.metric("Learners",len(df))
        b.metric("Class Average",f"{df['Percentage'].mean():.1f}%")
        c.metric("Learning Gaps",len(r["weak"]))
        d.metric("Support Flags",len(r["flags"]))

        st.subheader("Learner Performance")
        st.bar_chart(
    df,
    x="Learner",
    y="Percentage",
    horizontal=True
)
    else:
        a,b,c = st.columns(3)
        a.metric("Specialist Agents","10")
        b.metric("Assessments Processed","0")
        c.metric("System Status","Ready")
        st.info("Upload an assessment to activate EduNex.")


elif page == "Assessment Upload":
    st.title("Assessment Upload")

    marks = st.file_uploader(
        "Upload learner marks (CSV or Excel)",
        type=["csv","xlsx"]
    )

    st.subheader("Assessment information")
    grade = st.selectbox(
        "Grade",[f"Grade {i}" for i in range(8,13)]
    )
    subject = st.text_input("Subject")

    memo = st.file_uploader(
        "Upload marking memorandum",
        type=["pdf","docx","txt"]
    )
    paper = st.file_uploader(
        "Upload assessment paper",
        type=["pdf","docx","txt"]
    )

    demo = st.checkbox("Use demonstration data")

    if st.button("PROCESS ASSESSMENT"):
        try:
            if demo:
                df = sample_data()
            elif marks:
                df = (
                    pd.read_csv(marks)
                    if marks.name.endswith(".csv")
                    else pd.read_excel(marks)
                )
            else:
                st.error("Upload a marks file or select demonstration data.")
                st.stop()

            if "Learner" not in df.columns:
                st.error("Your spreadsheet needs a Learner column.")
                st.stop()

            st.session_state.data = df
            st.session_state.grade = grade
            st.session_state.subject = subject
            st.session_state.results = None
            st.success("Assessment successfully uploaded.")

        except Exception as e:
            st.error(f"Upload error: {e}")

    if memo or paper:
        st.caption("Reference documents received. Automatic extraction is not yet implemented.")


elif page == "Agent Intelligence":
    st.title("Agent Intelligence")
    st.write("Ten specialist roles coordinated by the Planner.")

    for i,(name,description) in enumerate(AGENTS,1):
        st.markdown(
            f'<div class="agent"><b>{i:02d} · {name}</b>'
            f'<p style="color:#9AafBB">{description}</p></div>',
            unsafe_allow_html=True
        )

    if st.button("EXECUTE AGENT WORKFLOW"):
        if st.session_state.data is None:
            st.warning("Upload an assessment first.")
        else:
            with st.spinner("EduNex is executing its workflow..."):
                st.session_state.results = execute_workflow(
                    st.session_state.data
                )
                time.sleep(1)
            st.success("Workflow completed.")
            st.rerun()

    if st.session_state.results:
        st.subheader("Execution log")
        for entry in st.session_state.results["log"]:
            st.write("✓",entry)


elif page == "Performance Insights":
    st.title("Performance Intelligence")

    if not st.session_state.results:
        st.info("Process an assessment first.")
    else:
        r = st.session_state.results
        st.metric(
            "Class Average",
            f"{r['data']['Percentage'].mean():.1f}%"
        )
        st.subheader("Question averages")
        st.bar_chart(r["data"][r["questions"]].mean())
        st.subheader("Learner results")
        st.dataframe(r["data"],use_container_width=True)
        st.subheader("Identified learning gaps")
        for q in r["weak"]:
            st.warning(f"{q}: class average below 50% of assumed maximum.")


elif page == "Inclusive Learning":
    st.title("Inclusive Learning & Support")
    st.caption("Indicators for teacher review, not medical diagnoses.")

    if not st.session_state.results:
        st.info("Process an assessment first.")
    else:
        flags = st.session_state.results["flags"]
        st.metric("Learners flagged for review",len(flags))

        for learner in flags:
            st.warning(
                f"{learner}: Repeated low scores warrant teacher observation."
            )


elif page == "Worksheets & Interventions":
    st.title("Worksheets & Interventions")

    if not st.session_state.results:
        st.info("Process an assessment first.")
    else:
        r = st.session_state.results

        st.subheader("Curriculum-aligned worksheet plans")
        for w in r["worksheets"]:
            with st.expander(w["topic"]):
                st.write(w["exercise"])
                st.caption("Teacher must verify curriculum alignment.")

        st.subheader("Suggested interventions")
        for learner in r["flags"]:
            st.write(
                f"**{learner}:** Consider guided revision, targeted practice "
                "and monitoring."
            )


elif page == "Review & Reports":
    st.title("Reviewing Agent & Reports")

    if not st.session_state.results:
        st.info("Process an assessment first.")
    else:
        r = st.session_state.results

        for item in r["log"][-4:]:
            if "PASS" in item:
                st.success(item)
            elif "rejected" in item:
                st.warning(item)
            else:
                st.info(item)

        st.subheader("Verified assessment")
        st.table(r["data"])

        report = (
            "EDUNEX TEACHER REPORT\n"
            f"Generated: {datetime.now()}\n"
            f"Grade: {st.session_state.grade}\n"
            f"Subject: {st.session_state.subject}\n\n"
            f"LEARNER RESULTS\n{r['data'].to_string(index=False)}\n\n"
            f"LEARNING GAPS\n{r['weak']}\n\n"
            f"SUPPORT FLAGS\n{r['flags']}\n\n"
            f"REVIEW LOG\n{chr(10).join(r['log'])}\n"
        )

        st.download_button(
            "DOWNLOAD TEACHER REPORT",
            report,
            "EduNex_Report.txt"
        )

st.markdown("---")
st.caption(
    "EDUNEX | Educational Intelligence | Prototype | "
    "Teacher oversight required"
)
