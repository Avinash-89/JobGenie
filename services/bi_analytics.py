# services/bi_analytics.py
import pandas as pd
import plotly.express as px
import streamlit as st
from core.database import SessionLocal, CandidateProfile

def render_bi_dashboard():
    """
    Queries database state, aggregates talent metrics, and outputs interactive operational charts.
    """
    db = SessionLocal()
    candidates = db.query(CandidateProfile).all()
    db.close()
    
    if not candidates:
        st.warning("📊 No candidate dataset metrics found inside storage. Run a few resumes through the processing pipeline first!")
        return

    # Convert SQLAlchemy results to Pandas DataFrame
    data = [{
        "Name": c.name,
        "ATS Score": c.ats_score if c.ats_score else 0,
        "Status": c.status,
        "Date": c.updated_at
    } for c in candidates]
    
    df = pd.DataFrame(data)
    
    # Structural KPI Matrix Rows
    st.subheader("Talent Funnel KPI Metrics Matrix")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Processed Profiles", len(df))
    kpi2.metric("Mean System ATS Alignment", f"{int(df['ATS Score'].mean())}%")
    kpi3.metric("Active Pipeline Openings", len(df[df["Status"] == "Applied"]))
    
    st.markdown("---")
    
    # Layout Distribution Plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### ATS Score Evaluation Distribution Spectrum")
        fig_hist = px.histogram(df, x="ATS Score", nbins=10, color_discrete_sequence=['#0083B0'], template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        st.write("#### Candidate Acquisition Pipeline Status Allocation")
        # FIX: Replaced px.colors.sequential.Plotlysh with px.colors.qualitative.Plotly
        fig_pie = px.pie(df, names="Status", hole=0.4, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig_pie, use_container_width=True)