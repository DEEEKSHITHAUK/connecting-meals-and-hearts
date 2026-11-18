
import streamlit as st
from datetime import datetime, date, time, timedelta
from difflib import SequenceMatcher
import re
import html
st.set_page_config(
    page_title="Meals & Hearts",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="auto"
)
# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Meals & Hearts",
    page_icon="💙",
    layout="wide"
)

# =====================================================
# SESSION STORAGE
# =====================================================

for key in ["donations", "requests", "feedback"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "donation_errors" not in st.session_state:
    st.session_state.donation_errors = {}

if "request_errors" not in st.session_state:
    st.session_state.request_errors = {}

if "feedback_errors" not in st.session_state:
    st.session_state.feedback_errors = {}

# =====================================================
# LANGUAGE TRANSLATIONS
# =====================================================

translations = {
    "English": {
        "home": "Home",
        "donate": "Donate Food",
        "request": "Request Food",
        "available": "Available Donations",
        "notifications": "Notifications",
        "feedback": "Feedback",
        "matching": "AI Food Matching",
        "about": "About Us",
        "choose": "Choose Your Page",
        "welcome": "Welcome to Meals & Hearts 💙",
        "mission": "Connecting Extra Meals with Hungry Hearts",
        "donor": "Donor Name",
        "food": "Food Name",
        "quantity": "Quantity of Meals",
        "location": "Pickup Location",
        "phone": "Contact Number",
        "category": "Food Category",
        "description": "Additional Information",
        "donation_date": "Donation Date",
        "donation_time": "Donation Time",
        "expiry_date": "Food Expiry Date",
        "expiry_time": "Food Expiry Time",
        "submit": "Submit Donation",
        "person": "Your Name",
        "required_food": "Food Required",
        "meals": "Number of Meals Required",
        "address": "Your Location",
        "submit_request": "Submit Request",
        "rating": "Rate Our Platform",
        "comment": "Your Feedback",
        "submit_feedback": "Submit Feedback",
        "search": "Search Food",
        "suggestions": "Similar Food Suggestions",
        "no_food": "No food donations available.",
        "no_notifications": "No new notifications.",
        "about_text": "Meals & Hearts connects food donors with people who need meals."
    },

    "Kannada": {
        "home": "ಮುಖಪುಟ",
        "donate": "ಆಹಾರ ದಾನ ಮಾಡಿ",
        "request": "ಆಹಾರ ವಿನಂತಿ",
        "available": "ಲಭ್ಯವಿರುವ ಆಹಾರ",
        "notifications": "ಅಧಿಸೂಚನೆಗಳು",
        "feedback": "ಪ್ರತಿಕ್ರಿಯೆ",
        "matching": "AI ಆಹಾರ ಹೊಂದಾಣಿಕೆ",
        "about": "ನಮ್ಮ ಬಗ್ಗೆ",
        "choose": "ಪುಟವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "welcome": "ಮೀಲ್ಸ್ ಅಂಡ್ ಹಾರ್ಟ್ಸ್‌ಗೆ ಸ್ವಾಗತ 💙",
        "mission": "ಹೆಚ್ಚುವರಿ ಆಹಾರವನ್ನು ಅಗತ್ಯವಿರುವವರಿಗೆ ತಲುಪಿಸುವುದು",
        "donor": "ದಾನಿಗಳ ಹೆಸರು",
        "food": "ಆಹಾರದ ಹೆಸರು",
        "quantity": "ಊಟಗಳ ಸಂಖ್ಯೆ",
        "location": "ಆಹಾರ ಪಡೆಯುವ ಸ್ಥಳ",
        "phone": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
        "category": "ಆಹಾರದ ವರ್ಗ",
        "description": "ಹೆಚ್ಚುವರಿ ಮಾಹಿತಿ",
        "donation_date": "ದಾನದ ದಿನಾಂಕ",
        "donation_time": "ದಾನದ ಸಮಯ",
        "expiry_date": "ಮುಕ್ತಾಯ ದಿನಾಂಕ",
        "expiry_time": "ಮುಕ್ತಾಯ ಸಮಯ",
        "submit": "ದಾನ ಸಲ್ಲಿಸಿ",
        "person": "ನಿಮ್ಮ ಹೆಸರು",
        "required_food": "ಅಗತ್ಯವಿರುವ ಆಹಾರ",
        "meals": "ಅಗತ್ಯವಿರುವ ಊಟಗಳ ಸಂಖ್ಯೆ",
        "address": "ನಿಮ್ಮ ಸ್ಥಳ",
        "submit_request": "ವಿನಂತಿ ಸಲ್ಲಿಸಿ",
        "rating": "ರೇಟಿಂಗ್ ನೀಡಿ",
        "comment": "ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆ",
        "submit_feedback": "ಪ್ರತಿಕ್ರಿಯೆ ಸಲ್ಲಿಸಿ",
        "search": "ಆಹಾರ ಹುಡುಕಿ",
        "suggestions": "ಹೋಲುವ ಆಹಾರಗಳು",
        "no_food": "ಯಾವುದೇ ಆಹಾರ ದಾನ ಲಭ್ಯವಿಲ್ಲ.",
        "no_notifications": "ಹೊಸ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ.",
        "about_text": "ಮೀಲ್ಸ್ ಅಂಡ್ ಹಾರ್ಟ್ಸ್ ಆಹಾರ ದಾನಿಗಳನ್ನು ಅಗತ್ಯವಿರುವವರೊಂದಿಗೆ ಸಂಪರ್ಕಿಸುತ್ತದೆ."
    },

    "Hindi": {
        "home": "होम",
        "donate": "भोजन दान करें",
        "request": "भोजन का अनुरोध",
        "available": "उपलब्ध भोजन",
        "notifications": "सूचनाएं",
        "feedback": "प्रतिक्रिया",
        "matching": "AI भोजन मिलान",
        "about": "हमारे बारे में",
        "choose": "अपना पेज चुनें",
        "welcome": "मील्स एंड हार्ट्स में आपका स्वागत है 💙",
        "mission": "अतिरिक्त भोजन जरूरतमंद लोगों तक पहुंचाना",
        "donor": "दाता का नाम",
        "food": "भोजन का नाम",
        "quantity": "भोजन की मात्रा",
        "location": "भोजन लेने का स्थान",
        "phone": "संपर्क नंबर",
        "category": "भोजन की श्रेणी",
        "description": "अतिरिक्त जानकारी",
        "donation_date": "दान की तारीख",
        "donation_time": "दान का समय",
        "expiry_date": "समाप्ति तिथि",
        "expiry_time": "समाप्ति का समय",
        "submit": "दान जमा करें",
        "person": "आपका नाम",
        "required_food": "आवश्यक भोजन",
        "meals": "आवश्यक भोजन की संख्या",
        "address": "आपका स्थान",
        "submit_request": "अनुरोध जमा करें",
        "rating": "रेटिंग दें",
        "comment": "आपकी प्रतिक्रिया",
        "submit_feedback": "प्रतिक्रिया जमा करें",
        "search": "भोजन खोजें",
        "suggestions": "मिलते-जुलते भोजन",
        "no_food": "अभी कोई भोजन उपलब्ध नहीं है।",
        "no_notifications": "कोई नई सूचना नहीं।",
        "about_text": "मील्स एंड हार्ट्स भोजन दाताओं को जरूरतमंद लोगों से जोड़ता है।"
    }
}

language = st.sidebar.selectbox(
    "🌐 Select Language / ಭಾಷೆ / भाषा",
    ["English", "Kannada", "Hindi"]
)

def T(key):
    return translations[language].get(key, key)

# =====================================================
# COUNTRY CODE OPTIONS
# =====================================================

country_codes = {
    "India (+91)": "+91",
    "USA / Canada (+1)": "+1",
    "United Kingdom (+44)": "+44",
    "UAE (+971)": "+971",
    "Australia (+61)": "+61",
    "Singapore (+65)": "+65",
    "Saudi Arabia (+966)": "+966",
    "Germany (+49)": "+49",
    "France (+33)": "+33",
    "Japan (+81)": "+81"
}

# This prototype requires 10 digits after every country code.

# =====================================================
# VALIDATION FUNCTIONS
# =====================================================

def valid_name(name):
    name = name.strip()

    return (
        bool(name)
        and all(
            character.isalpha() or character.isspace()
            for character in name
        )
    )

def valid_phone(number, country_code):
    number = number.strip()

    if not re.fullmatch(r"[0-9]{10}", number):
        return False

    if country_code == "+91" and number[0] not in "6789":
        return False

    return True

def validate_name_field(name):
    if not name.strip():
        return "Name is required."

    if not valid_name(name):
        return "Only alphabetic letters and spaces are allowed."

    return None

def validate_phone_field(number, country_code):
    if not number.strip():
        return "Contact number is required."

    if not valid_phone(number, country_code):
        return "Enter exactly 10 digits. Check the selected country code."

    return None

def show_error(message):
    if message:
        st.markdown(
            f'<p style="color:#d00000;font-weight:bold;'
            f'font-size:14px;margin-top:-8px;">'
            f'❌ {html.escape(message)}</p>',
            unsafe_allow_html=True
        )

# =====================================================
# FOOD SIMILARITY SEARCH
# =====================================================

def find_similar_food(search_text, food_list):

    search_text = search_text.strip().lower()

    if not search_text:
        return []

    results = {}

    for item in food_list:

        food_name = item["Food"]
        candidate = food_name.lower()

        if candidate == search_text:
            score = 1.0

        elif search_text in candidate or candidate in search_text:
            score = 0.90

        else:
            score = SequenceMatcher(
                None, search_text, candidate
            ).ratio()

        if score >= 0.40:
            results[food_name] = max(
                results.get(food_name, 0),
                score
            )

    return sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )[:6]

def show_food_suggestions(search_text):

    suggestions = find_similar_food(
        search_text,
        st.session_state.donations
    )

    if suggestions:

        st.markdown("**🔍 " + T("suggestions") + "**")

        for food_name, score in suggestions:

            st.markdown(
                f"""
                <div style="
                    background:#e8f4ff;
                    border:1px solid #78b5eb;
                    border-radius:10px;
                    padding:9px;
                    margin:5px 0;
                    color:#082b59;">
                    🍱 <b>{html.escape(food_name)}</b>
                    <span style="float:right;">
                    {round(score * 100)}% similarity
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================================================
# FOOD STATUS
# =====================================================

def food_status(item):

    now = datetime.now()
    expiry = item["Expiry"]

    if now >= expiry:
        return "expired"

    if expiry - now <= timedelta(hours=2):
        return "expiring"

    return "fresh"

# =====================================================
# AI FOOD MATCHING
# =====================================================

def match_food(donation, requests):

    matches = []

    for request in requests:

        score = 0
        reasons = []

        donor_food = donation["Food"].lower()
        requested_food = request["Food"].lower()

        if donor_food == requested_food:
            score += 40
            reasons.append("Exact food name match")

        elif (
            donor_food in requested_food
            or requested_food in donor_food
            or SequenceMatcher(
                None, donor_food, requested_food
            ).ratio() >= 0.60
        ):
            score += 20
            reasons.append("Similar food name")

        if donation["Quantity"] >= request["Meals"]:
            score += 25
            reasons.append("Sufficient quantity")

        donor_location = donation["Location"].lower()
        request_location = request["Location"].lower()

        if donor_location == request_location:
            score += 25
            reasons.append("Same location")

        elif (
            donor_location in request_location
            or request_location in donor_location
        ):
            score += 10
            reasons.append("Similar location")

        if food_status(donation) == "expired":
            continue

        if score >= 40:
            matches.append({
                "Name": request["Name"],
                "Food": request["Food"],
                "Meals": request["Meals"],
                "Location": request["Location"],
                "Contact": request["Contact"],
                "Score": score,
                "Reasons": reasons
            })

    return sorted(
        matches,
        key=lambda x: x["Score"],
        reverse=True
    )

# =====================================================
# BLUE THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background:linear-gradient(
        135deg,#d6ecff,#a9d5ff,#c5e4ff
    );
}

html,body,[class*="css"] {
    color:#082b59 !important;
}

h1,h2,h3,h4,h5,h6 {
    color:#082b59 !important;
    font-weight:800 !important;
}

.hero {
    background:#b4d9ff;
    padding:35px;
    border-radius:25px;
    text-align:center;
    border:2px solid #5b9bd5;
    margin-bottom:25px;
}

.info-card {
    background:#e8f4ff;
    padding:22px;
    border-radius:18px;
    border:2px solid #78b5eb;
    margin-bottom:15px;
}

.stButton > button {
    background-color:#347fc4 !important;
    color:white !important;
    border:2px solid #164d82 !important;
    border-radius:12px !important;
    font-weight:bold !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color:#edf7ff !important;
    color:#082b59 !important;
    border:2px solid #5b9bd5 !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(f"""
<div class="hero">
<h1>💙 Meals & Hearts 🍱</h1>
<h3>{T("mission")}</h3>
<p>Share Food • Spread Love • Make a Difference</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# NAVIGATION
# =====================================================

page_keys = [
    "home", "donate", "request", "available",
    "notifications", "feedback", "matching", "about"
]

menu_items = [T(key) for key in page_keys]

selected_menu = st.selectbox(
    T("choose"),
    menu_items
)

page = page_keys[menu_items.index(selected_menu)]

# =====================================================
# HOME PAGE
# =====================================================

if page == "home":

    st.subheader(T("welcome"))

    st.write(T("mission"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h2>🍱 Donate Food</h2>
        <p>Share extra meals with someone in need.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h2>❤️ Help People</h2>
        <p>Make a positive difference.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
        <h2>🌍 Reduce Waste</h2>
        <p>Prevent food from being wasted.</p>
        </div>
        """, unsafe_allow_html=True)

    a, b, c = st.columns(3)

    a.metric("Food Donations", len(st.session_state.donations))
    b.metric("Food Requests", len(st.session_state.requests))
    c.metric("Feedback Received", len(st.session_state.feedback))

# =====================================================
# DONATE FOOD PAGE
# =====================================================

elif page == "donate":

    st.subheader("🍱 " + T("donate"))

    # Input fields outside form enable live suggestions
    name = st.text_input(T("donor"), key="donor_name")

    name_error = validate_name_field(name)
    if name_error and name:
        show_error(name_error)

    food = st.text_input(T("food"), key="donation_food")

    if food.strip():
        show_food_suggestions(food)

    quantity = st.number_input(
        T("quantity"),
        min_value=1,
        step=1,
        key="donation_quantity"
    )

    location = st.text_input(
        T("location"),
        key="donation_location"
    )

    st.markdown("**Contact Number**")

    country_label = st.selectbox(
        "Country Code",
        list(country_codes.keys()),
        key="donation_country"
    )

    country_code = country_codes[country_label]

    phone = st.text_input(
        "10-digit mobile number",
        max_chars=10,
        placeholder="9876543210",
        key="donation_phone"
    )

    phone_error = validate_phone_field(phone, country_code)
    if phone_error and phone:
        show_error(phone_error)

    st.caption(
        "Your complete number will be saved as "
        + country_code + " followed by your 10 digits."
    )

    food_type = st.selectbox(
        T("category"),
        ["Vegetarian", "Non-Vegetarian", "Snacks", "Other"]
    )

    description = st.text_area(T("description"))

    col1, col2 = st.columns(2)

    with col1:
        donation_date = st.date_input(
            T("donation_date"),
            value=date.today()
        )

        donation_clock = st.time_input(
            T("donation_time"),
            value=datetime.now().time().replace(
                second=0, microsecond=0
            )
        )

    with col2:
        expiry_date = st.date_input(
            T("expiry_date"),
            value=date.today()
        )

        expiry_clock = st.time_input(
            T("expiry_time"),
            value=(datetime.now() + timedelta(hours=4)).time().replace(
                second=0, microsecond=0
            )
        )

    if st.button("💙 " + T("submit"), key="save_donation"):

        errors = []

        if name_error:
            errors.append(("name", name_error))

        if not food.strip():
            errors.append(("food", "Food name is required."))

        if not location.strip():
            errors.append(("location", "Pickup location is required."))

        if phone_error:
            errors.append(("phone", phone_error))

        donation_datetime = datetime.combine(
            donation_date, donation_clock
        )

        expiry_datetime = datetime.combine(
            expiry_date, expiry_clock
        )

        if donation_datetime > datetime.now():
            errors.append((
                "date",
                "Donation date and time cannot be in the future."
            ))

        if expiry_datetime <= donation_datetime:
            errors.append((
                "expiry",
                "Expiry must be after donation date and time."
            ))

        if errors:

            st.error("Please correct the highlighted fields below.")

            for field, message in errors:
                st.markdown(
                    f'<p style="color:#d00000;font-weight:bold;">'
                    f'❌ {html.escape(field.title())}: '
                    f'{html.escape(message)}</p>',
                    unsafe_allow_html=True
                )

        else:

            st.session_state.donations.append({
                "Donor": name.strip(),
                "Food": food.strip(),
                "Quantity": quantity,
                "Location": location.strip(),
                "Phone": country_code + phone,
                "Category": food_type,
                "Description": description,
                "Donated": donation_datetime,
                "Expiry": expiry_datetime
            })

            st.success("💙 Donation added successfully!")

            st.rerun()

# =====================================================
# REQUEST FOOD PAGE
# =====================================================

elif page == "request":

    st.subheader("❤️ " + T("request"))

    person = st.text_input(
        T("person"),
        key="request_name"
    )

    person_error = validate_name_field(person)

    if person_error and person:
        show_error(person_error)

    requested_food = st.text_input(
        T("required_food"),
        key="request_food"
    )

    if requested_food.strip():
        show_food_suggestions(requested_food)

    meals = st.number_input(
        T("meals"),
        min_value=1,
        step=1
    )

    address = st.text_input(
        T("address"),
        key="request_location"
    )

    st.markdown("**Contact Number**")

    request_country_label = st.selectbox(
        "Country Code",
        list(country_codes.keys()),
        key="request_country"
    )

    request_country_code = country_codes[request_country_label]

    contact = st.text_input(
        "10-digit mobile number",
        max_chars=10,
        placeholder="9876543210",
        key="request_phone"
    )

    contact_error = validate_phone_field(
        contact, request_country_code
    )

    if contact_error and contact:
        show_error(contact_error)

    if st.button("❤️ " + T("submit_request")):

        errors = []

        if person_error:
            errors.append(("name", person_error))

        if not requested_food.strip():
            errors.append(("food", "Food required field cannot be empty."))

        if not address.strip():
            errors.append(("location", "Location is required."))

        if contact_error:
            errors.append(("phone", contact_error))

        if errors:

            st.error("Please correct the highlighted fields.")

            for field, message in errors:
                st.markdown(
                    f'<p style="color:#d00000;font-weight:bold;">'
                    f'❌ {html.escape(field.title())}: '
                    f'{html.escape(message)}</p>',
                    unsafe_allow_html=True
                )

        else:

            st.session_state.requests.append({
                "Name": person.strip(),
                "Food": requested_food.strip(),
                "Meals": meals,
                "Location": address.strip(),
                "Contact": request_country_code + contact
            })

            st.success("❤️ Food request submitted successfully!")

            st.rerun()

# =====================================================
# AVAILABLE DONATIONS + SEARCH
# =====================================================

elif page == "available":

    st.subheader("🍲 " + T("available"))

    search = st.text_input(
        "🔍 " + T("search"),
        placeholder="Search Rice, Biriyani, Chapati..."
    )

    donations = [
        item for item in st.session_state.donations
        if food_status(item) != "expired"
    ]

    if search.strip():

        suggestions = find_similar_food(search, donations)

        if suggestions:
            st.markdown("**🔍 Similar food found:**")

            for food_name, score in suggestions:
                st.write(
                    f"🍱 {food_name} — {round(score * 100)}% similarity"
                )

        filtered = [
            item for item in donations
            if any(
                item["Food"] == food_name
                for food_name, score in suggestions
            )
        ]

    else:
        filtered = donations

    if filtered:

        filtered = sorted(
            filtered,
            key=lambda item: item["Food"].lower()
        )

        for i, item in enumerate(filtered, 1):

            with st.container(border=True):

                st.markdown(f"### 🍱 {item['Food']}")

                st.write("**Donor:**", item["Donor"])
                st.write("**Quantity:**", item["Quantity"], "meals")
                st.write("**Location:**", item["Location"])
                st.write("**Contact:**", item["Phone"])
                st.write("**Category:**", item["Category"])

                st.write(
                    "**Donated:**",
                    item["Donated"].strftime("%d-%m-%Y %I:%M %p")
                )

                st.write(
                    "**Expires:**",
                    item["Expiry"].strftime("%d-%m-%Y %I:%M %p")
                )

                if food_status(item) == "expiring":
                    st.warning("⚠️ Food is expiring within 2 hours!")
                else:
                    st.success("✅ Available")

    else:
        st.info(T("no_food"))

# =====================================================
# NOTIFICATIONS
# =====================================================

elif page == "notifications":

    st.subheader("🔔 " + T("notifications"))

    notifications = []

    for item in st.session_state.donations:

        status = food_status(item)

        if status == "expired":
            notifications.append(
                f"❌ {item['Food']} donated by {item['Donor']} has expired."
            )

        elif status == "expiring":
            notifications.append(
                f"⚠️ {item['Food']} is expiring within 2 hours!"
            )

    if notifications:

        for message in notifications:
            st.warning(message)

    else:
        st.success(T("no_notifications"))

    st.caption(
        "Notifications update when the app reruns. "
        "Background push notifications are not enabled."
    )

# =====================================================
# FEEDBACK
# =====================================================

elif page == "feedback":

    st.subheader("💬 " + T("feedback"))

    feedback_name = st.text_input(
        "Your Name",
        key="feedback_name"
    )

    feedback_name_error = validate_name_field(feedback_name)

    if feedback_name_error and feedback_name:
        show_error(feedback_name_error)

    rating = st.select_slider(
        T("rating"),
        options=[1, 2, 3, 4, 5],
        value=5
    )

    comment = st.text_area(T("comment"))

    if st.button("💙 " + T("submit_feedback")):

        if feedback_name_error:
            show_error(feedback_name_error)

        elif not comment.strip():
            st.error("Please enter your feedback.")

        else:

            st.session_state.feedback.append({
                "Name": feedback_name.strip(),
                "Rating": rating,
                "Comment": comment.strip(),
                "Date": datetime.now()
            })

            st.success("Thank you for your feedback!")

            st.rerun()

    st.markdown("---")
    st.subheader("⭐ User Reviews")

    for review in reversed(st.session_state.feedback):

        with st.container(border=True):

            st.markdown(f"### ⭐ {review['Rating']}/5")
            st.write("**Name:**", review["Name"])
            st.write(review["Comment"])
            st.caption(
                review["Date"].strftime("%d-%m-%Y %I:%M %p")
            )

# =====================================================
# AI FOOD MATCHING
# =====================================================

elif page == "matching":

    st.subheader("🤖 AI-Based Food Matching Agent")

    active_donations = [
        item for item in st.session_state.donations
        if food_status(item) != "expired"
    ]

    if not active_donations:

        st.info("No active food donations available.")

    elif not st.session_state.requests:

        st.info("No food requests available.")

    else:

        options = [
            f"{item['Food']} - {item['Donor']} - {item['Quantity']} meals"
            for item in active_donations
        ]

        selected = st.selectbox(
            "Select a donation",
            options
        )

        donation_index = options.index(selected)
        donation = active_donations[donation_index]

        if st.button("🤖 Find Best Matches"):

            matches = match_food(
                donation,
                st.session_state.requests
            )

            if matches:

                st.success(
                    f"{len(matches)} matching requests found!"
                )

                for i, match in enumerate(matches, 1):

                    with st.container(border=True):

                        st.markdown(f"### ❤️ Match {i}")

                        st.write("**Requester:**", match["Name"])
                        st.write("**Food:**", match["Food"])
                        st.write("**Quantity:**", match["Meals"])
                        st.write("**Location:**", match["Location"])
                        st.write("**Contact:**", match["Contact"])

                        st.progress(
                            min(match["Score"], 100)
                        )

                        st.write(
                            f"Matching Score: {match['Score']}%"
                        )

                        for reason in match["Reasons"]:
                            st.write("✅", reason)

            else:
                st.warning("No suitable food requests found.")

# =====================================================
# ABOUT US
# =====================================================

elif page == "about":

    st.subheader("🌍 " + T("about"))

    st.write(T("about_text"))

    st.write("""
    Our main goals:

    1. Reduce food wastage.
    2. Help people access meals.
    3. Connect donors and receivers.
    4. Support Kannada, English and Hindi.
    5. Track food expiry dates.
    6. Provide AI-based food matching.
    7. Collect user feedback.
    """)

    st.markdown("""
    <div class="info-card">
    <h2>💙 Every Meal Matters!</h2>
    <p>Share food, spread kindness and connect hearts.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:20px;">
<h3>💙 Meals & Hearts</h3>
<p>Connecting Meals, Creating Smiles.</p>
<p>Made with ❤️ for a better tomorrow.</p>
</div>
""", unsafe_allow_html=True)
