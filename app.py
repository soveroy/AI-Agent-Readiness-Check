import streamlit as st

from pyairtable import Table

# Airtable Config
AIRTABLE_TOKEN = "pat99Yyq9j6bNWw45.063e5bbfd1a8296913a8e5162fd24810058d8ae387dd687a8fba251a35583f21"
BASE_ID = "appghcVhoG9XovxDz"
TABLE_NAME = "Leads"

table = Table(AIRTABLE_TOKEN, BASE_ID, TABLE_NAME)


# --- CONFIGURATION ---
st.set_page_config(page_title="AI Agent Suitability Calculator", page_icon="🤖", layout="centered")

# --- HEADER / INTRO ---
st.title("🤖 AI Agent Suitability Calculator")
st.markdown("""
This calculator helps you find out whether your business is ready to adopt an AI agent.

You'll answer a few questions about how your team operates. At the end, we'll provide a score and recommendation — then you can request a free report.
""")

# --- QUESTIONS + OPTIONS ---
questions = [
    {
        "question": "How are your team’s daily workflows documented or standardized?",
        "options": {
            "We don’t really document anything": 5,
            "Basic SOPs in shared folders": 4,
            "Mix of spreadsheets and some automation tools": 3,
            "Mostly handled through an internal system or CRM": 2,
            "Fully systematized using automated workflows": 1
        },
        "weight": 2
    },
    {
        "question": "How do you assign and track tasks across your team?",
        "options": {
            "We pass tasks around via WhatsApp/Slack/email": 5,
            "We have a shared Excel or Google Sheet": 4,
            "We use a task tracking tool like Trello or Asana": 3,
            "We use a project management platform linked to SOPs": 2,
            "All tasks are assigned and tracked automatically through a central system": 1
        },
        "weight": 2
    },
    {
        "question": "What happens when a new employee joins your team?",
        "options": {
            "We train them manually from scratch": 5,
            "We send them docs or slide decks to read": 4,
            "We pair them with a buddy or manager for OJT": 3,
            "We have a structured onboarding process with some automation": 2,
            "The system handles most onboarding via guided flows or bots": 1
        },
        "weight": 1
    },
    {
        "question": "How are client/customer queries handled?",
        "options": {
            "Team replies manually each time": 5,
            "We use email templates or canned replies": 4,
            "We have a shared FAQ document or portal": 3,
            "We use a chatbot or helpdesk to handle basic queries": 2,
            "Most queries are self-served or AI-automated": 1
        },
        "weight": 2
    },
    {
        "question": "How do you schedule meetings or appointments?",
        "options": {
            "We email/WhatsApp back and forth to find time": 5,
            "We ask them to fill in a form or respond to an email": 4,
            "We use a shared calendar or Google Calendar invites": 3,
            "We use Calendly or booking software": 2,
            "Scheduling is fully automated or integrated with our system": 1
        },
        "weight": 1
    },
    {
        "question": "How often do team members repeat the same task/process?",
        "options": {
            "All the time": 5,
            "Very often": 4,
            "Sometimes": 3,
            "Rarely": 2,
            "Almost never": 1
        },
        "weight": 2
    },
    {
        "question": "What is your monthly customer or task volume like?",
        "options": {
            "We’re overwhelmed — hundreds or thousands per week": 5,
            "We handle a few hundred a month": 4,
            "Low to moderate — a few dozen per week": 3,
            "Manageable volume, not too intense": 2,
            "Very low volume, not a concern": 1
        },
        "weight": 1
    },
    {
        "question": "Do you track and measure team productivity today?",
        "options": {
            "No tracking at all": 5,
            "We look at ad hoc reports sometimes": 4,
            "We use Excel or basic reporting tools": 3,
            "We use dashboards for some KPIs": 2,
            "We track almost everything in real-time": 1
        },
        "weight": 1
    }
]

# --- FORM SECTION 1: Scoring ---
with st.form("ai_agent_survey"):
    st.subheader("🧠 Step 1: Describe your current workflow")

    total_score = 0
    for i, q in enumerate(questions):
        answer = st.selectbox(
            f"{i+1}. {q['question']}",
            options=list(q["options"].keys()),
            key=f"dropdown_{i}"
        )
        total_score += q["options"][answer] * q["weight"]

    submitted = st.form_submit_button("See My AI Suitability Score")

if submitted:
    st.session_state["score"] = total_score
    st.rerun()

# --- RESULT / SCORE ---
if "score" in st.session_state and not submitted:
    score = st.session_state["score"]
    st.subheader("📊 Step 2: Your Results")
    st.markdown(f"**Your Total Score:** `{score}` (Max possible: 40)")

    if score >= 30:
        st.success("✅ Strong Match: Your team will benefit from using an AI agent.")
        st.markdown("You’re spending significant time on manual, repetitive tasks. Automating them will boost productivity and reduce errors.")
        recommendation = "Strong Match"
    elif 20 <= score < 30:
        st.warning("⚠️ Partial Match: Some areas of your work may benefit from AI.")
        st.markdown("You’re somewhat systematized, but still have room for automation in task handling or communication.")
        recommendation = "Partial Match"
    else:
        st.info("❌ Low Need: Your team may not urgently need AI support.")
        st.markdown("Your processes are streamlined and low-friction — AI may be helpful but not critical.")
        recommendation = "Low Need"

    # --- FORM SECTION 2: Lead Capture ---
    st.divider()
    st.subheader("📧 Step 3: Request Your Free Report")

    with st.form("lead_capture"):
        user_name = st.text_input("Your Name")
        company_name = st.text_input("Company Name")
        email = st.text_input("Work Email")
        company_size = st.selectbox("Company Size", ["1-10", "11-50", "51-200", "201-500", "500+"])

        send = st.form_submit_button("Submit & Get Report")

    if send:
        if not user_name or not company_name or not email:
            st.warning("Please fill in all required fields.")
        else:
            try:
                table.create({
                    "Name": user_name,
                    "Company": company_name,
                    "Email": email,
                    "Company Size": company_size,
                    "Score": score,
                    "Recommendation": recommendation
                })
                st.success("🎉 Thank you! Your report will be sent to your email shortly.")
                st.markdown(f"**Name:** {user_name}  \n**Company:** {company_name}  \n**Email:** {email}  \n**Size:** {company_size}  \n**Score:** {score}  \n**Recommendation:** {recommendation}")
            except Exception as e:
                st.error(f"Failed to save to Airtable: {e}")
