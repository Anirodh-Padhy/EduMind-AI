import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

from src.auth import (

    register_user,

    login_user,

    get_pending_users,

    approve_user,

    get_all_users,

    delete_user,

    block_user,

    update_user_role
)

from src.chatbot import (
    generate_ai_response
)

from src.memory import (

    initialize_memory,

    add_message,

    get_conversation_context
)

from src.pdf_loader import (
    extract_pdf_text
)

from src.embeddings import (

    create_vector_store,

    search_documents
)

from src.quiz_parser import (
    parse_quiz
)

from src.teacher import (

    create_course,

    get_courses,

    get_student_count,

    get_teacher_count
)

from src.voice_assistant import (
    recognize_speech
)


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(

    page_title="EduMind AI",

    layout="wide"
)

# ===================================================
# SESSION STATE
# ===================================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False

if "username" not in st.session_state:

    st.session_state.username = ""

if "role" not in st.session_state:

    st.session_state.role = ""

if "chat_memory" not in st.session_state:

    st.session_state.chat_memory = (
        initialize_memory()
    )

if "document_text" not in st.session_state:

    st.session_state.document_text = ""

if "vector_index" not in st.session_state:

    st.session_state.vector_index = None

if "document_chunks" not in st.session_state:

    st.session_state.document_chunks = []

if "quiz_data" not in st.session_state:

    st.session_state.quiz_data = []

if "quiz_score" not in st.session_state:

    st.session_state.quiz_score = 0

if "quiz_history" not in st.session_state:

    st.session_state.quiz_history = []

if "study_hours" not in st.session_state:

    st.session_state.study_hours = 0

if "courses" not in st.session_state:

    st.session_state.courses = []

if "study_plan" not in st.session_state:

    st.session_state.study_plan = ""

if "study_sessions" not in st.session_state:

    st.session_state.study_sessions = []

if "achievements" not in st.session_state:

    st.session_state.achievements = []
# ===================================================
# CUSTOM CSS
# ===================================================

st.markdown("""

<style>

.main {

    background-color: #0E1117;
}

.stButton>button {

    width: 100%;
    border-radius: 10px;
    height: 3em;
}

</style>

""", unsafe_allow_html=True)

# ===================================================
# AUTH PAGE
# ===================================================

if not st.session_state.authenticated:

    st.title(
        "🚀 EduMind AI"
    )

    st.markdown(
        "## Enterprise AI Education Platform"
    )

    auth_mode = st.sidebar.selectbox(

        "Authentication",

        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    # ---------------------------------------------------
    # LOGIN
    # ---------------------------------------------------

    if auth_mode == "Login":

        if st.button("Login"):

            success, message, role = login_user(

                username,

                password
            )

            if success:

                st.session_state[
                    "authenticated"
                ] = True

                st.session_state[
                    "username"
                ] = username

                st.session_state[
                    "role"
                ] = role

                st.success(message)

                st.rerun()

            else:

                st.error(message)

    # ---------------------------------------------------
    # REGISTER
    # ---------------------------------------------------

    else:

        role = st.selectbox(

            "Select Role",

            [
                "student",
                "teacher"
            ]
        )

        if st.button("Register"):

            success, message = register_user(

                username,

                password,

                role
            )

            if success:

                st.success(message)

            else:

                st.error(message)

# ===================================================
# MAIN APP
# ===================================================

else:

    st.sidebar.success(
        f"Logged in as: {st.session_state.username}"
    )

    st.sidebar.info(
        f"Role: {st.session_state.role}"
    )

    # ---------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------

    if st.sidebar.button("Logout"):

        st.session_state.authenticated = False

        st.session_state.username = ""

        st.session_state.role = ""

        st.rerun()

    # ---------------------------------------------------
    # MENU
    # ---------------------------------------------------

    menu_items = [

        "Dashboard",

        "AI Tutor",

        "Study Materials",

        "Quiz Generator",

        "Voice Assistant",

        "AI Study Planner",

        "Progress Analytics"
    ]

    # ADMIN MENU

    if st.session_state.role == "admin":

        menu_items.append(
            "Admin Dashboard"
        )

    # TEACHER MENU

    if st.session_state.role == "teacher":

        menu_items.append(
            "Teacher Dashboard"
        )

    menu = st.sidebar.radio(

        "Navigation",

        menu_items
    )

    # ===================================================
    # DASHBOARD
    # ===================================================

    if menu == "Dashboard":

        st.title(
            "🎓 EduMind AI Dashboard"
        )

        st.markdown(
            "### Personalized Learning Analytics"
        )

        # ---------------------------------------------------
        # KPI METRICS
        # ---------------------------------------------------

        total_quizzes = len(

            st.session_state[
                "quiz_history"
            ]
        )

        avg_score = 0

        if total_quizzes > 0:

            avg_score = sum(

                q["percentage"]

                for q in st.session_state[
                    "quiz_history"
                ]

            ) / total_quizzes

        study_hours = st.session_state[
            "study_hours"
        ]

        uploaded_notes = 0

        if st.session_state[
            "document_text"
        ]:

            uploaded_notes = 1

        # ---------------------------------------------------
        # KPI CARDS
        # ---------------------------------------------------

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Quizzes Attempted",
                total_quizzes
            )

        with col2:

            st.metric(
                "Average Score",
                f"{avg_score:.2f}%"
            )

        with col3:

            st.metric(
                "Study Sessions",
                study_hours
            )

        with col4:

            st.metric(
                "Uploaded Notes",
                uploaded_notes
            )

        st.markdown("---")

        # ---------------------------------------------------
        # QUIZ PERFORMANCE CHART
        # ---------------------------------------------------

        if total_quizzes > 0:

            st.subheader(
                "📊 Quiz Performance"
            )

            df = pd.DataFrame(

                st.session_state[
                    "quiz_history"
                ]
            )

            df["Quiz"] = range(
                1,
                len(df) + 1
            )

            fig = px.line(

                df,

                x="Quiz",

                y="percentage",

                title="Quiz Performance Trend",

                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ---------------------------------------------------
            # DIFFICULTY ANALYTICS
            # ---------------------------------------------------

            st.subheader(
                "📈 Difficulty Analytics"
            )

            difficulty_chart = px.histogram(

                df,

                x="difficulty",

                color="difficulty",

                title="Quiz Difficulty Distribution"
            )

            st.plotly_chart(
                difficulty_chart,
                use_container_width=True
            )

        else:

            st.info(
                "No quiz analytics available yet."
            )

        st.markdown("---")

        # ---------------------------------------------------
        # AI LEARNING INSIGHTS
        # ---------------------------------------------------

        st.subheader(
            "🧠 AI Learning Insights"
        )

        if avg_score >= 80:

            st.success(
                """
                Excellent progress.
                You are performing very well.
                """
            )

        elif avg_score >= 50:

            st.warning(
                """
                Good progress.
                Focus more on revision.
                """
            )

        else:

            st.error(
                """
                Performance needs improvement.
                Practice quizzes regularly.
                """
            )

        # ---------------------------------------------------
        # STUDY RECOMMENDATIONS
        # ---------------------------------------------------

        st.subheader(
            "📚 Personalized Study Recommendations"
        )

        recommendations = [

            "Revise weak topics regularly",

            "Practice quizzes daily",

            "Upload more study materials",

            "Use AI tutor for difficult concepts",

            "Track learning progress weekly"
        ]

        for rec in recommendations:

            st.write(
                f"✅ {rec}"
            )

    # ===================================================
    # AI TUTOR CHATBOT
    # ===================================================

    elif menu == "AI Tutor":

        st.title(
            "🤖 EduMind AI Tutor"
        )

        st.markdown(
            "### Personalized AI Learning Assistant"
        )

        # ---------------------------------------------------
        # DISPLAY CHAT HISTORY
        # ---------------------------------------------------

        for message in st.session_state[
            "chat_memory"
        ]:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

        # ---------------------------------------------------
        # USER INPUT
        # ---------------------------------------------------

        user_input = st.chat_input(
            "Ask your study question..."
        )

        if user_input:

            # ---------------------------------------------------
            # SHOW USER MESSAGE
            # ---------------------------------------------------

            with st.chat_message("user"):

                st.write(user_input)

            # ---------------------------------------------------
            # SAVE USER MESSAGE
            # ---------------------------------------------------

            add_message(

                st.session_state[
                    "chat_memory"
                ],

                "user",

                user_input
            )

            # ---------------------------------------------------
            # GET CONTEXT
            # ---------------------------------------------------

            conversation_context = (
                get_conversation_context(

                    st.session_state[
                        "chat_memory"
                    ]
                )
            )

            # ---------------------------------------------------
            # AI RESPONSE
            # ---------------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "EduMind AI is teaching..."
                ):

                    response = generate_ai_response(

                        user_input,

                        conversation_context
                    )

                    st.write(response)

            # ---------------------------------------------------
            # SAVE AI RESPONSE
            # ---------------------------------------------------

            add_message(

                st.session_state[
                    "chat_memory"
                ],

                "assistant",

                response
            )

    # ===================================================
    # STUDY MATERIALS
    # ===================================================

    elif menu == "Study Materials":

        st.title(
            "📄 AI Notes Analyzer"
        )

        uploaded_file = st.file_uploader(

            "Upload Study Notes/PDF",

            type=["pdf", "txt"]
        )

        if uploaded_file:

            # ---------------------------------------------------
            # PDF EXTRACTION
            # ---------------------------------------------------

            if uploaded_file.type == "application/pdf":

                document_text = extract_pdf_text(
                    uploaded_file
                )

            else:

                document_text = str(
                    uploaded_file.read(),
                    "utf-8"
                )

            # ---------------------------------------------------
            # SAVE TEXT
            # ---------------------------------------------------

            st.session_state[
                "document_text"
            ] = document_text

            # ---------------------------------------------------
            # CREATE VECTOR STORE
            # ---------------------------------------------------

            index, chunks = create_vector_store(
                document_text
            )

            st.session_state[
                "vector_index"
            ] = index

            st.session_state[
                "document_chunks"
            ] = chunks

            st.success(
                f"Uploaded: {uploaded_file.name}"
            )

            st.success(
                "✅ AI Knowledge Base Created"
            )

            st.info(
                f"📦 Chunks Indexed: {len(chunks)}"
            )

            st.markdown("---")

            st.subheader(
                "📚 Notes Preview"
            )

            st.text_area(

                "Extracted Notes",

                document_text[:6000],

                height=300
            )

            # ---------------------------------------------------
            # NOTES ANALYSIS
            # ---------------------------------------------------

            st.markdown("---")

            analysis_type = st.selectbox(

                "Select AI Analysis",

                [
                    "Summarize Notes",
                    "Explain Difficult Concepts",
                    "Generate Key Points",
                    "Ask Questions from Notes"
                ]
            )

            custom_question = ""

            if (
                analysis_type
                == "Ask Questions from Notes"
            ):

                custom_question = st.text_input(
                    "Ask Question"
                )

            # ---------------------------------------------------
            # ANALYZE BUTTON
            # ---------------------------------------------------

            if st.button("Analyze Notes"):

                with st.spinner(
                    "EduMind AI is analyzing..."
                ):

                    # ---------------------------------------------------
                    # SUMMARIZE
                    # ---------------------------------------------------

                    if (
                        analysis_type
                        == "Summarize Notes"
                    ):

                        prompt = f"""

                        Summarize these study notes clearly.

                        NOTES:
                        {document_text[:3000]}
                        """

                    # ---------------------------------------------------
                    # EXPLAIN CONCEPTS
                    # ---------------------------------------------------

                    elif (
                        analysis_type
                        == "Explain Difficult Concepts"
                    ):

                        prompt = f"""

                        Explain difficult concepts
                        from these notes simply.

                        NOTES:
                        {document_text[:3000]}
                        """

                    # ---------------------------------------------------
                    # KEY POINTS
                    # ---------------------------------------------------

                    elif (
                        analysis_type
                        == "Generate Key Points"
                    ):

                        prompt = f"""

                        Generate important study points
                        from these notes.

                        NOTES:
                        {document_text[:3000]}
                        """

                    # ---------------------------------------------------
                    # RAG QUESTION ANSWERING
                    # ---------------------------------------------------

                    else:

                        retrieved_chunks = (
                            search_documents(

                                custom_question,

                                st.session_state[
                                    "vector_index"
                                ],

                                st.session_state[
                                    "document_chunks"
                                ]
                            )
                        )

                        context = "\n\n".join(
                            retrieved_chunks
                        )

                        prompt = f"""

                        You are EduMind AI.

                        Answer using ONLY the study notes.

                        CONTEXT:
                        {context}

                        QUESTION:
                        {custom_question}

                        Explain clearly for students.
                        """

                    # ---------------------------------------------------
                    # AI RESPONSE
                    # ---------------------------------------------------

                    response = generate_ai_response(
                        prompt
                    )

                st.success(
                    "Analysis Complete"
                )

                st.write(response)

    # ===================================================
    # QUIZ GENERATOR
    # ===================================================

    elif menu == "Quiz Generator":

        st.title(
            "📝 AI Quiz Generator"
        )

        if not st.session_state[
            "document_text"
        ]:

            st.warning(
                "Please upload study notes first."
            )

        else:

            difficulty = st.selectbox(

                "Select Difficulty",

                [
                    "Easy",
                    "Medium",
                    "Hard"
                ]
            )

            num_questions = st.slider(

                "Number of Questions",

                3,
                10,
                5
            )

            # ---------------------------------------------------
            # GENERATE QUIZ
            # ---------------------------------------------------

            if st.button(
                "Generate AI Quiz"
            ):

                with st.spinner(
                    "Generating quiz..."
                ):

                    prompt = f"""

                    Generate {num_questions}
                    multiple choice questions
                    from these study notes.

                    Difficulty: {difficulty}

                    Format EXACTLY like this:

                    Q: Question here

                    A) Option 1
                    B) Option 2
                    C) Option 3
                    D) Option 4

                    Answer: Correct Option

                    ---------------------------------------------------

                    NOTES:
                    {st.session_state['document_text'][:3000]}
                    """

                    quiz_response = (
                        generate_ai_response(
                            prompt
                        )
                    )

                    quiz_data = parse_quiz(
                        quiz_response
                    )

                    st.session_state[
                        "quiz_data"
                    ] = quiz_data

                    st.success(
                        "Quiz generated successfully."
                    )

            # ---------------------------------------------------
            # DISPLAY QUIZ
            # ---------------------------------------------------

            if st.session_state[
                "quiz_data"
            ]:

                st.markdown("---")

                st.subheader(
                    "📚 Generated Quiz"
                )

                user_answers = []

                for i, question in enumerate(

                    st.session_state[
                        "quiz_data"
                    ]
                ):

                    st.markdown(
                        f"""
                        ### Q{i+1}.
                        {question['question']}
                        """
                    )

                    answer = st.radio(

                        "Select Answer",

                        question["options"],

                        key=f"quiz_{i}"
                    )

                    user_answers.append(answer)

                # ---------------------------------------------------
                # SUBMIT QUIZ
                # ---------------------------------------------------

                if st.button(
                    "Submit Quiz"
                ):

                    score = 0

                    st.markdown("---")

                    st.subheader(
                        "📊 Quiz Results"
                    )

                    for i, question in enumerate(

                        st.session_state[
                            "quiz_data"
                        ]
                    ):

                        correct_answer = (
                            question["answer"]
                        )

                        selected = (
                            user_answers[i]
                        )

                        if correct_answer in selected:

                            score += 1

                            st.success(
                                f"""
                                Q{i+1}: Correct
                                """
                            )

                        else:

                            st.error(
                                f"""
                                Q{i+1}: Incorrect

                                Correct Answer:
                                {correct_answer}
                                """
                            )

                    # ---------------------------------------------------
                    # FINAL SCORE
                    # ---------------------------------------------------

                    st.session_state[
                        "quiz_score"
                    ] = score

                    percentage = (
                        score
                        /
                        len(
                            st.session_state[
                                "quiz_data"
                            ]
                        )
                    ) * 100

                    st.markdown("---")

                    st.metric(
                        "Final Score",

                        f"""
                        {score}/
                        {len(st.session_state['quiz_data'])}
                        """
                    )

                    st.metric(
                        "Percentage",

                        f"{percentage:.2f}%"
                    )

                    # ---------------------------------------------------
                    # SAVE QUIZ HISTORY
                    # ---------------------------------------------------

                    st.session_state[
                        "quiz_history"
                    ].append({
                    
                        "score": score,

                        "percentage": percentage,

                        "difficulty": difficulty
                    })

                    # ---------------------------------------------------
                    # UPDATE STUDY HOURS
                    # ---------------------------------------------------

                    st.session_state[
                        "study_hours"
                    ] += 1

                    # ---------------------------------------------------
                    # PERFORMANCE MESSAGE
                    # ---------------------------------------------------

                    if percentage >= 80:

                        st.success(
                            "Excellent performance!"
                        )

                        if "Quiz Master" not in st.session_state[
                            "achievements"
                        ]:

                            st.session_state[
                                "achievements"
                            ].append(
                                "Quiz Master"
                            )

                    elif percentage >= 50:
                    
                        st.warning(
                            "Good attempt. Keep practicing."
                        )

                    else:
                    
                        st.error(
                            "Needs improvement. Revise notes again."
                        )
    # ===================================================
    # PROGRESS ANALYTICS
    # ===================================================
    
    elif menu == "Progress Analytics":
    
        st.title(
            "📊 Advanced Learning Analytics"
        )
    
        st.markdown(
            "### AI-Powered Student Performance Intelligence"
        )
    
        # ---------------------------------------------------
        # KPI METRICS
        # ---------------------------------------------------
    
        total_quizzes = len(
        
            st.session_state[
                "quiz_history"
            ]
        )
    
        avg_score = 0
    
        highest_score = 0
    
        lowest_score = 0
    
        if total_quizzes > 0:
        
            scores = [
            
                q["percentage"]
    
                for q in st.session_state[
                    "quiz_history"
                ]
            ]
    
            avg_score = np.mean(scores)
    
            highest_score = np.max(scores)
    
            lowest_score = np.min(scores)
    
        total_study_sessions = len(
        
            st.session_state[
                "study_sessions"
            ]
        )
    
        total_achievements = len(
        
            st.session_state[
                "achievements"
            ]
        )
    
        # ---------------------------------------------------
        # KPI CARDS
        # ---------------------------------------------------
    
        col1, col2, col3, col4 = (
            st.columns(4)
        )
    
        with col1:
        
            st.metric(
                "Quizzes Completed",
                total_quizzes
            )
    
        with col2:
        
            st.metric(
                "Average Score",
                f"{avg_score:.2f}%"
            )
    
        with col3:
        
            st.metric(
                "Best Score",
                f"{highest_score:.2f}%"
            )
    
        with col4:
        
            st.metric(
                "Achievements",
                total_achievements
            )
    
        st.markdown("---")
    
        # ---------------------------------------------------
        # QUIZ PERFORMANCE TREND
        # ---------------------------------------------------
    
        if total_quizzes > 0:
        
            st.subheader(
                "📈 Quiz Performance Trend"
            )
    
            df = pd.DataFrame(
            
                st.session_state[
                    "quiz_history"
                ]
            )
    
            df["Quiz Number"] = range(
                1,
                len(df) + 1
            )
    
            trend_chart = px.line(
            
                df,
    
                x="Quiz Number",
    
                y="percentage",
    
                markers=True,
    
                title="Quiz Improvement Trend"
            )
    
            st.plotly_chart(
                trend_chart,
                use_container_width=True
            )
    
            # ---------------------------------------------------
            # SCORE DISTRIBUTION
            # ---------------------------------------------------
    
            st.subheader(
                "📊 Score Distribution"
            )
    
            score_chart = px.histogram(
            
                df,
    
                x="percentage",
    
                nbins=10,
    
                title="Quiz Score Distribution"
            )
    
            st.plotly_chart(
                score_chart,
                use_container_width=True
            )
    
            # ---------------------------------------------------
            # DIFFICULTY ANALYTICS
            # ---------------------------------------------------
    
            st.subheader(
                "📚 Difficulty-Level Analytics"
            )
    
            difficulty_chart = px.box(
            
                df,
    
                x="difficulty",
    
                y="percentage",
    
                color="difficulty",
    
                title="Difficulty Performance Analysis"
            )
    
            st.plotly_chart(
                difficulty_chart,
                use_container_width=True
            )
    
        else:
        
            st.info(
                "No quiz data available yet."
            )
    
        st.markdown("---")
    
        # ---------------------------------------------------
        # STUDY ACTIVITY ANALYTICS
        # ---------------------------------------------------
    
        st.subheader(
            "⏱️ Study Activity Analytics"
        )
    
        if total_study_sessions > 0:
        
            session_df = pd.DataFrame(
            
                st.session_state[
                    "study_sessions"
                ]
            )
    
            activity_chart = px.pie(
            
                session_df,
    
                names="activity",
    
                title="Learning Activity Distribution"
            )
    
            st.plotly_chart(
                activity_chart,
                use_container_width=True
            )
    
        else:
        
            st.info(
                "No study activity recorded yet."
            )
    
        st.markdown("---")
    
        # ---------------------------------------------------
        # AI LEARNING INSIGHTS
        # ---------------------------------------------------
    
        st.subheader(
            "🧠 AI Learning Insights"
        )
    
        if avg_score >= 80:
        
            st.success(
                """
                Excellent learning performance.
                You are mastering concepts effectively.
                """
            )
    
        elif avg_score >= 50:
        
            st.warning(
                """
                Good learning progress.
                Focus more on revision and quizzes.
                """
            )
    
        else:
        
            st.error(
                """
                Learning performance needs improvement.
                Practice regularly with AI tutor.
                """
            )
    
        # ---------------------------------------------------
        # ACHIEVEMENTS
        # ---------------------------------------------------
    
        st.subheader(
            "🏆 Achievements"
        )
    
        if st.session_state[
            "achievements"
        ]:
    
            for achievement in st.session_state[
                "achievements"
            ]:
    
                st.success(
                    f"🏅 {achievement}"
                )
    
        else:
        
            st.info(
                "No achievements unlocked yet."
            )
    
        st.markdown("---")
    
        # ---------------------------------------------------
        # PERSONALIZED RECOMMENDATIONS
        # ---------------------------------------------------
    
        st.subheader(
            "📚 Personalized Recommendations"
        )
    
        recommendations = [
        
            "Practice quizzes daily",
    
            "Use AI tutor for weak topics",
    
            "Upload more study materials",
    
            "Revise difficult concepts weekly",
    
            "Track progress regularly"
        ]
    
        for rec in recommendations:
        
            st.write(
                f"✅ {rec}"
            )
    
    # ===================================================
    # AI STUDY PLANNER
    # ===================================================

    elif menu == "AI Study Planner":

        st.title(
            "🧠 Personalized AI Study Planner"
        )

        st.markdown(
            "### Adaptive Learning Roadmap Generator"
        )

        # ---------------------------------------------------
        # USER INPUTS
        # ---------------------------------------------------

        study_goal = st.text_input(
            "Enter Your Learning Goal"
        )

        study_hours = st.slider(

            "Daily Study Hours",

            1,
            12,
            3
        )

        learning_duration = st.selectbox(

            "Study Duration",

            [
                "1 Week",
                "2 Weeks",
                "1 Month",
                "3 Months"
            ]
        )

        weak_subjects = st.text_area(
            "Weak Topics / Subjects"
        )

        # ---------------------------------------------------
        # GENERATE PLAN
        # ---------------------------------------------------

        if st.button(
            "Generate AI Study Plan"
        ):

            with st.spinner(
                "EduMind AI is creating your personalized roadmap..."
            ):

                # ---------------------------------------------------
                # QUIZ ANALYTICS
                # ---------------------------------------------------

                avg_score = 0

                total_quizzes = len(

                    st.session_state[
                        "quiz_history"
                    ]
                )

                if total_quizzes > 0:

                    avg_score = sum(

                        q["percentage"]

                        for q in st.session_state[
                            "quiz_history"
                        ]

                    ) / total_quizzes

                # ---------------------------------------------------
                # PERFORMANCE LEVEL
                # ---------------------------------------------------

                if avg_score >= 80:

                    performance_level = (
                        "Advanced Learner"
                    )

                elif avg_score >= 50:

                    performance_level = (
                        "Intermediate Learner"
                    )

                else:

                    performance_level = (
                        "Beginner Learner"
                    )

                # ---------------------------------------------------
                # AI PROMPT
                # ---------------------------------------------------

                prompt = f"""

                You are EduMind AI,
                an advanced AI study planner.

                Create a personalized study roadmap.

                STUDENT DETAILS:

                Learning Goal:
                {study_goal}

                Daily Study Hours:
                {study_hours}

                Study Duration:
                {learning_duration}

                Weak Topics:
                {weak_subjects}

                Student Performance:
                {performance_level}

                Average Quiz Score:
                {avg_score:.2f}%

                ---------------------------------------------------

                Create:

                1. Daily study schedule
                2. Weekly learning roadmap
                3. Smart revision plan
                4. Weak-topic improvement strategy
                5. Productivity recommendations
                6. AI learning tips

                Make the plan:
                - structured
                - motivational
                - practical
                - student friendly
                """

                # ---------------------------------------------------
                # AI RESPONSE
                # ---------------------------------------------------

                study_plan = generate_ai_response(
                    prompt
                )

                st.session_state[
                    "study_plan"
                ] = study_plan

            st.success(
                "AI Study Plan Generated Successfully"
            )

        # ---------------------------------------------------
        # DISPLAY STUDY PLAN
        # ---------------------------------------------------

        if st.session_state[
            "study_plan"
        ]:

            st.markdown("---")

            st.subheader(
                "📚 Your Personalized AI Study Plan"
            )

            st.write(

                st.session_state[
                    "study_plan"
                ]
            )

            st.markdown("---")

            # ---------------------------------------------------
            # AI PRODUCTIVITY TIPS
            # ---------------------------------------------------

            st.subheader(
                "⚡ Smart Productivity Tips"
            )

            tips = [

                "Use active recall while studying",

                "Practice quizzes daily",

                "Revise weak concepts regularly",

                "Take short study breaks",

                "Use AI tutor for difficult topics"
            ]

            for tip in tips:

                st.write(
                    f"✅ {tip}"
                )


    # ===================================================
    # VOICE LEARNING ASSISTANT
    # ===================================================
    
    elif menu == "Voice Assistant":
    
        st.title(
            "🎤 Voice Learning Assistant"
        )
    
        st.markdown(
            "### Talk directly with EduMind AI"
        )
    
        st.info(
            """
            Click the button and speak your question.
            """
        )
    
        # ---------------------------------------------------
        # START VOICE INPUT
        # ---------------------------------------------------
    
        if st.button(
            "🎙️ Start Voice Assistant"
        ):
    
            with st.spinner(
                "Listening..."
            ):
    
                speech_text = recognize_speech()
    
            # ---------------------------------------------------
            # DISPLAY USER SPEECH
            # ---------------------------------------------------
    
            st.subheader(
                "🗣️ Your Question"
            )
    
            st.write(speech_text)
    
            # ---------------------------------------------------
            # AI RESPONSE
            # ---------------------------------------------------
    
            if not speech_text.startswith(
                "Error"
            ):
    
                with st.spinner(
                    "EduMind AI is responding..."
                ):
    
                    response = generate_ai_response(
                        speech_text
                    )
    
                st.subheader(
                    "🤖 EduMind AI Response"
                )
    
                st.write(response)
                
                st.session_state[
                    "study_sessions"
                ].append({
                
                    "activity": "Voice Learning",

                    "duration": 1
                })

            else:
            
                st.error(speech_text)
            # ---------------------------------------------------
            # TRACK STUDY SESSION
            # ---------------------------------------------------

            st.session_state[
                "study_sessions"
            ].append({
            
                "activity": "AI Tutor",

                "duration": 1
            })

    # ===================================================
    # TEACHER DASHBOARD
    # ===================================================

    elif menu == "Teacher Dashboard":

        st.title(
            "👨‍🏫 Teacher Dashboard"
        )

        st.markdown(
            "### AI-Powered Classroom Management"
        )

        # ---------------------------------------------------
        # KPI METRICS
        # ---------------------------------------------------

        total_students = get_student_count()

        total_teachers = get_teacher_count()

        total_courses = len(
            get_courses()
        )

        total_quizzes = len(

            st.session_state[
                "quiz_history"
            ]
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Students",
                total_students
            )

        with col2:

            st.metric(
                "Teachers",
                total_teachers
            )

        with col3:

            st.metric(
                "Courses",
                total_courses
            )

        with col4:

            st.metric(
                "Quizzes Taken",
                total_quizzes
            )

        st.markdown("---")

        # ---------------------------------------------------
        # CREATE COURSE
        # ---------------------------------------------------

        st.subheader(
            "📚 Create New Course"
        )

        course_name = st.text_input(
            "Course Name"
        )

        course_description = st.text_area(
            "Course Description"
        )

        if st.button(
            "Create Course"
        ):

            create_course(

                st.session_state[
                    "username"
                ],

                course_name,

                course_description
            )

            st.success(
                "Course created successfully."
            )

            st.rerun()

        st.markdown("---")

        # ---------------------------------------------------
        # DISPLAY COURSES
        # ---------------------------------------------------

        st.subheader(
            "📖 Available Courses"
        )

        courses = get_courses()

        if courses:

            for course in courses:

                teacher = course[0]

                name = course[1]

                description = course[2]

                st.markdown(
                    f"""
                    ### 📘 {name}

                    👨‍🏫 Teacher: {teacher}

                    📝 {description}
                    """
                )

                st.markdown("---")

        else:

            st.info(
                "No courses available yet."
            )

        # ---------------------------------------------------
        # STUDENT PERFORMANCE
        # ---------------------------------------------------

        st.subheader(
            "📊 Student Performance Analytics"
        )

        if st.session_state[
            "quiz_history"
        ]:

            df = pd.DataFrame(

                st.session_state[
                    "quiz_history"
                ]
            )

            performance_chart = px.line(

                df,

                y="percentage",

                title="Quiz Performance Trend",

                markers=True
            )

            st.plotly_chart(
                performance_chart,
                use_container_width=True
            )

        else:

            st.info(
                "No quiz analytics available yet."
            )

        # ---------------------------------------------------
        # AI INSIGHTS
        # ---------------------------------------------------

        st.subheader(
            "🧠 AI Classroom Insights"
        )

        st.success(
            """
            Students are actively using
            AI-powered learning tools.
            """
        )

        st.info(
            """
            Encourage students to:
            - upload study materials
            - practice quizzes
            - use AI tutor regularly
            """
        )

    # ===================================================
    # ADMIN DASHBOARD
    # ===================================================

    elif menu == "Admin Dashboard":

        st.title(
            "🛡️ Enterprise Admin Dashboard"
        )

        # ---------------------------------------------------
        # PENDING USERS
        # ---------------------------------------------------

        st.subheader(
            "⏳ Pending User Approvals"
        )

        pending_users = get_pending_users()

        if pending_users:

            for user in pending_users:

                user_id = user[0]

                username = user[1]

                role = user[2]

                col1, col2 = st.columns([4,1])

                with col1:

                    st.write(
                        f"👤 {username} ({role})"
                    )

                with col2:

                    if st.button(
                        f"Approve {username}"
                    ):

                        approve_user(user_id)

                        st.success(
                            f"{username} approved."
                        )

                        st.rerun()

        else:

            st.success(
                "No pending users."
            )

        st.markdown("---")

        # ---------------------------------------------------
        # USER MANAGEMENT
        # ---------------------------------------------------

        st.subheader(
            "👥 User Management"
        )

        users = get_all_users()

        for user in users:

            user_id = user[0]

            username = user[1]

            role = user[2]

            approved = user[3]

            status = (
                "Approved"
                if approved
                else "Blocked"
            )

            st.markdown("---")

            col1, col2, col3 = (
                st.columns([3,2,3])
            )

            # ---------------------------------------------------
            # USER INFO
            # ---------------------------------------------------

            with col1:

                st.write(
                    f"👤 {username}"
                )

                st.write(
                    f"Status: {status}"
                )

            # ---------------------------------------------------
            # ROLE UPDATE
            # ---------------------------------------------------

            with col2:

                if username != "admin":

                    new_role = st.selectbox(

                        f"Role for {username}",

                        [
                            "student",
                            "teacher",
                            "admin"
                        ],

                        index=[
                            "student",
                            "teacher",
                            "admin"
                        ].index(role),

                        key=f"role_{user_id}"
                    )

                    if st.button(
                        f"Update Role {username}"
                    ):

                        update_user_role(

                            user_id,

                            new_role
                        )

                        st.success(
                            f"{username} updated to {new_role}"
                        )

                        st.rerun()

            # ---------------------------------------------------
            # USER ACTIONS
            # ---------------------------------------------------

            with col3:

                if username != "admin":

                    # BLOCK USER

                    if approved:

                        if st.button(
                            f"Block {username}"
                        ):

                            block_user(user_id)

                            st.warning(
                                f"{username} blocked."
                            )

                            st.rerun()

                    # DELETE USER

                    if st.button(
                        f"Delete {username}"
                    ):

                        delete_user(user_id)

                        st.error(
                            f"{username} deleted."
                        )

                        st.rerun()