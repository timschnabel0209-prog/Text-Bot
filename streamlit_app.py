
import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURATION & SYSTEM-PROMPT ---
SYSTEM_INSTRUCTION = """
Identität: Du bist ein spezialisierter KI-Berater für soziale Anliegen und Konfliktmanagement.
Rolle: Empathisch, sachlich, vorurteilsfrei und lösungsorientiert.
Regeln: 
- Neutralität & Hilfe zur Selbsthilfe.
- Klare, einfache Sprache.
- Schema: Validierung -> Analyse -> Deeskalation (Ich-Botschaften, Perspektivwechsel, Mediation).
- Mobbing: Sofort Hilfe durch Erwachsene/Stellen empfehlen.
- Recht: Nur allgemeine Infos (SGB II/XII), keine Rechtsberatung.
- Notfall (WICHTIG): Bei Gewalt/Selbstharmonie SOFORT an 110/112 oder Telefonseelsorge (0800-1110111) verweisen.
- Datenschutz: Keine Klarnamen/Adressen fordern. Keine Diagnosen stellen.
"""

# --- 2. SEITEN-LAYOUT ---
st.set_page_config(page_title="Sozial-Beratungs-Bot", page_icon="🤝")

# Notfall-Banner oben
st.error("🆘 **NOTFALL?** Ruf sofort die **112** (Notruf) oder die **0800-1110111** (Telefonseelsorge) an.")

st.title("🤝 Dein Sozial-Beratungs-Bot")
st.markdown("Ich bin deine erste Anlaufstelle bei Konflikten und sozialen Sorgen. Schreib mir einfach, was dich bedrückt.")

# Sidebar für Infos & Impressum
with st.sidebar:
    st.header("Wichtige Kontakte")
    st.write("📞 **Nummer gegen Kummer:** 116 111")
    st.write("📞 **Elterntelefon:** 0800 111 0 550")
    st.divider()
    st.info("Dies ist ein KI-Pilotprojekt. Ich ersetze keine professionelle Therapie oder Rechtsberatung.")
    st.write("---")
    st.write("**Impressum:** [Dein Name/Organisation], [Deine Adresse]")

# --- 3. KI-LOGIK ---
# API Key sicher eingeben (lokal oder in Streamlit Secrets)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Das "models/" davor ist wichtig!
    system_instruction=SYSTEM_INSTRUCTION
)

    # Chat-Verlauf speichern
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat-Verlauf anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Benutzereingabe
    if prompt := st.chat_input("Erzähl mir, was los ist..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Antwort generieren
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("Bitte gib deinen Google API Key in der Seitenleiste ein, um den Bot zu starten.")