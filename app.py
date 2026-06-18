import os
import sys

# 1. Path safety injection block
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from core.database import init_db, SessionLocal, User, CandidateProfile
from core.auth import init_session_state, authenticate_user, hash_password
from services.parser import extract_text_from_pdf
from services.ats_engine import analyze_resume_vs_jd
from services.interview import generate_interview_questions, evaluate_interview_performance

# Import BI and reporting utilities up top
from services.bi_analytics import render_bi_dashboard
from utils.reporter import generate_pdf_report

# Page configuration standard parameters
st.set_page_config(
    page_title="JobGenie Workspace",
    page_icon="🧞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database and State trackers
init_db()
init_session_state()

# Initialize authentication sub-view state if not present
if "reg_view" not in st.session_state:
    st.session_state.reg_view = False

# Seed default credentials if new database
def seed_admin():
    db = SessionLocal()
    if db.query(User).count() == 0:
        admin_user = User(
            username="admin",
            email="admin@jobgenie.ai",
            password_hash=hash_password("admin123"),
            role="Admin"
        )
        db.add(admin_user)
        db.commit()
    db.close()
seed_admin()

# ==============================================================================
# VIEW 1: UNAUTHENTICATED STATE (CLEAN LOGIN / REGISTRATION GATEWAY)
# ==============================================================================
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.write("## ")  # Spacer layout alignment 
        st.title("🧞 JobGenie")
        
        # --- SUB-VIEW: REGISTRATION PAGE ---
        if st.session_state.reg_view:
            with st.form("registration_form", clear_on_submit=True):
                st.subheader("Create Your JobGenie Account")
                new_username = st.text_input("Username")
                new_email = st.text_input("Email Address")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Select Workspace Role", options=["Recruiter", "Admin", "Interviewer"])
                
                submit_reg = st.form_submit_button("Grant Account Access", use_container_width=True)
                
                if submit_reg:
                    if new_username and new_email and new_password:
                        db = SessionLocal()
                        exists = db.query(User).filter((User.username == new_username) | (User.email == new_email)).first()
                        if exists:
                            st.error("Username or Email address already registered.")
                            db.close()
                        else:
                            try:
                                new_user = User(
                                    username=new_username,
                                    email=new_email,
                                    password_hash=hash_password(new_password),
                                    role=new_role
                                )
                                db.add(new_user)
                                db.commit()
                                st.success("Account summoned successfully! Please sign in.")
                                st.session_state.reg_view = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error saving to database: {e}")
                            finally:
                                db.close()
                    else:
                        st.warning("Please populate all requested input parameters.")
            
            if st.button("Already have an account? Sign In here"):
                st.session_state.reg_view = False
                st.rerun()

        # --- SUB-VIEW: LOGIN PAGE ---
        else:
            with st.form("login_form", clear_on_submit=False):
                st.subheader("Login to your Workspace")
                username = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Enter JobGenie Hub", use_container_width=True)
                
                if submit:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.username = user.username
                        st.session_state.user_role = user.role
                        st.success(f"Welcome back, {user.username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password credentials configuration.")
            
            if st.button("New around here? Create a new account workspace"):
                st.session_state.reg_view = True
                st.rerun()

# ==============================================================================
# VIEW 2: AUTHENTICATED STATE (THE SECURE DASHBOARD ECOSYSTEM)
# ==============================================================================
else:
    # Sidebar control desk management layout
    st.sidebar.title("Genie Control Center")
    st.sidebar.write(f"**Current Operator:** `{st.session_state.username}`")
    st.sidebar.write(f"**Access Privilege:** :blue[{st.session_state.user_role}]")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Exit Platform (Log Out)", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.session_state.interview_started = False
        st.session_state.interview_complete = False
        st.rerun()

    # Consolidated central navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Analytics Matrix", 
        "📈 BI Analytics Dashboard",
        "📄 AI Resume Processing Engine", 
        "🎭 Live Interview Simulator",
        "📁 Document Reporting Terminal"
    ])
    
    # --------------------------------------------------------------------------
    # TAB 1: EXECUTIVE ANALYTICS MATRIX OVERVIEW
    # --------------------------------------------------------------------------
    with tab1:
        st.title("🚀 AI Talent Acquisition Matrix")
        st.markdown("---")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Resumes Parsed", "1,248", "+12% this week")
        m2.metric("Interviews Evaluated", "342", "+5% this week")
        m3.metric("Avg. ATS Fit Match", "74%", "+2% overall")
        m4.metric("Pending Audits", "14", "-3 open actions")
        
        st.info("💡 **Dashboard Notification Hub:** Use the upper workspace layout tabs to run complex resume analysis algorithms or start structural role mock testing sessions.")

    # --------------------------------------------------------------------------
    # TAB 2: BI ANALYTICS DASHBOARD
    # --------------------------------------------------------------------------
    with tab2:
        st.header("Business Intelligence & Performance Analytics")
        st.markdown("---")
        render_bi_dashboard()

    # --------------------------------------------------------------------------
    # TAB 3: AI RESUME PROCESSING ENGINE
    # --------------------------------------------------------------------------
    with tab3:
        st.header("Resume Analyzer Engine Pipeline")
        st.markdown("---")
        
        jd_input = st.text_area("Target Job Profile / Role Requirements Description", height=150)
        uploaded_file = st.file_uploader("Upload Applicant Profile (PDF Format)", type=["pdf"])
        
        if st.button("Execute Semantic Match Analysis") and uploaded_file and jd_input:
            with st.spinner("Executing structural parser and extraction pipeline..."):
                file_bytes = uploaded_file.read()
                raw_text = extract_text_from_pdf(file_bytes)
                analysis = analyze_resume_vs_jd(raw_text, jd_input)
                
                db = SessionLocal()
                new_candidate = CandidateProfile(
                    name=uploaded_file.name.replace(".pdf", ""),
                    email="parsed_extracted_identity@jobgenie.ai",
                    resume_text=raw_text[:2000],
                    ats_score=analysis["ats_score"],
                    status="Applied"
                )
                db.add(new_candidate)
                db.commit()
                db.close()
                
                st.success("Analysis pipeline calculations completed successfully!")
                
                col_metric, col_details = st.columns([1, 2])
                with col_metric:
                    st.metric(label="Overall Match Score", value=f"{analysis['ats_score']}%")
                with col_details:
                    st.write("**Matched Core Skill Vectors:**")
                    st.json(analysis["skills_matched"])
                    st.write("**Identified Capability/Skill Matrix Gaps:**")
                    st.json(analysis["skills_missing"])
                    st.info(f"**Strategic Assessment Critique:**\n\n{analysis['summary_critique']}")

    # --------------------------------------------------------------------------
    # TAB 4: LIVE INTERVIEW SIMULATOR
    # --------------------------------------------------------------------------
    with tab4:
        if "interview_started" not in st.session_state:
            st.session_state.interview_started = False
        if "questions" not in st.session_state:
            st.session_state.questions = []
        if "current_q_index" not in st.session_state:
            st.session_state.current_q_index = 0
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "interview_complete" not in st.session_state:
            st.session_state.interview_complete = False

        st.header("Conversational AI Interview Simulator")
        st.markdown("---")

        if not st.session_state.interview_started and not st.session_state.interview_complete:
            st.subheader("Configure Simulator Parameters")
            role_context = st.text_input("Target Role Name (e.g., Senior Backend Engineer)", key="role_ctx")
            jd_context = st.text_area("Paste Job Requirements Summary", key="jd_ctx")
            
            if st.button("Initialize Live Interview Session"):
                if role_context and jd_context:
                    with st.spinner("Compiling tailored evaluation vectors..."):
                        st.session_state.questions = generate_interview_questions("Candidate profile context parameters summary", jd_context)
                        st.session_state.interview_started = True
                        st.session_state.current_q_index = 0
                        st.session_state.chat_history = [{"role": "ai", "content": st.session_state.questions[0]}]
                        st.rerun()
                else:
                    st.warning("Please specify structural requirement conditions.")

        elif st.session_state.interview_started and not st.session_state.interview_complete:
            idx = st.session_state.current_q_index
            total_q = len(st.session_state.questions)
            
            st.progress((idx + 1) / total_q, text=f"Evaluating Verification Query Sequence Stage {idx + 1} of {total_q}")
            
            for msg in st.session_state.chat_history:
                if msg["role"] == "ai":
                    st.chat_message("assistant", avatar="🤖").write(msg["content"])
                else:
                    st.chat_message("user").write(msg["content"])
                    
            user_answer = st.chat_input("Type your performance answer parameter metrics here...")
            if user_answer:
                st.session_state.chat_history.append({"role": "candidate", "content": user_answer})
                
                if idx + 1 < total_q:
                    st.session_state.current_q_index += 1
                    next_q = st.session_state.questions[st.session_state.current_q_index]
                    st.session_state.chat_history.append({"role": "ai", "content": next_q})
                    st.rerun()
                else:
                    st.session_state.interview_started = False
                    st.session_state.interview_complete = True
                    st.rerun()

        elif st.session_state.interview_complete:
            st.success("Interview execution trace finished completely.")
            with st.spinner("Synthesizing transcript metrics..."):
                evaluation = evaluate_interview_performance(st.session_state.chat_history)
                
            st.subheader("Performance Evaluation Summary")
            st.metric("Calculated Technical Interview Score", f"{evaluation['interview_score']}/100")
            st.info(f"**Structural Performance Feedback:**\n\n{evaluation['critique']}")
            
            if st.button("Reset Simulator Framework Engine"):
                st.session_state.interview_started = False
                st.session_state.interview_complete = False
                st.session_state.questions = []
                st.session_state.chat_history = []
                st.rerun()

    # --------------------------------------------------------------------------
    # TAB 5: DOCUMENT REPORTING TERMINAL
    # --------------------------------------------------------------------------
    with tab5:
        st.header("Executive Audit Reporting Terminal")
        st.markdown("---")
        st.write("Generate and download legal compliance documentation or offline performance portfolios here.")
        
        db = SessionLocal()
        candidates_list = db.query(CandidateProfile).all()
        db.close()
        
        if candidates_list:
            candidate_map = {c.name: c for c in candidates_list}
            selected_name = st.selectbox("Select Target Evaluation Record for Compilation", options=list(candidate_map.keys()))
            
            if selected_name:
                target_record = candidate_map[selected_name]
                
                st.write(f"**Target Candidate Profile ID:** `{target_record.id}`")
                st.write(f"**Logged Pipeline Score Matrix:** `{target_record.ats_score}%`")
                
                sample_critique = f"The candidate profile tracking matrix under identifier {target_record.name} generated an analytical match coefficient score of {target_record.ats_score}% against active parameters."
                pdf_data = generate_pdf_report(target_record.name, target_record.ats_score or 0, sample_critique)
                
                st.download_button(
                    label="📥 Export Document Audit Log to PDF",
                    data=pdf_data,
                    file_name=f"Audit_Report_{target_record.name}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("No active records available. Run a file processing transaction to populate the document matrix.")