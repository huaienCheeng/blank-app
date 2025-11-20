import streamlit as st
from clips import Environment


# ---------------------------------------------------------
# Expert System (Safe: build line-by-line)
# ---------------------------------------------------------
def create_environment():
    env = Environment()

    # --- Build templates ---
    env.build("(deftemplate symptom (slot name) (slot value))")
    env.build("(deftemplate result (slot diagnosis))")

    # --- Build rules (NO MULTILINE!!!) ---
    env.build(
        '(defrule covid-possible '
        '(symptom (name fever) (value yes)) '
        '(symptom (name cough) (value yes)) '
        '=> '
        '(assert (result (diagnosis "Possible COVID-19 infection. Please test and isolate."))))'
    )

    env.build(
        '(defrule covid-unlikely '
        '(symptom (name fever) (value no)) '
        '(symptom (name cough) (value no)) '
        '=> '
        '(assert (result (diagnosis "Unlikely COVID-19 from these symptoms."))))'
    )

    return env


# ---------------------------------------------------------
# Run Expert System
# ---------------------------------------------------------
def run_expert_system(has_fever: bool, has_cough: bool) -> str:
    env = create_environment()
    env.reset()

    fever_value = "yes" if has_fever else "no"
    cough_value = "yes" if has_cough else "no"

    env.assert_string(f"(symptom (name fever) (value {fever_value}))")
    env.assert_string(f"(symptom (name cough) (value {cough_value}))")

    env.run()

    for fact in env.facts():
        if fact.template.name == "result":
            return fact["diagnosis"]

    return "No rule fired."


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
def main():
    st.title("🩺 COVID-19 Diagnosis Expert System (CLIPS + Streamlit)")
    st.write("Simple CLIPS rule-based diagnosis. Educational only.")

    fever = st.radio("Do you have a fever?", ["No", "Yes"], horizontal=True)
    cough = st.radio("Do you have a cough?", ["No", "Yes"], horizontal=True)

    has_fever = fever == "Yes"
    has_cough = cough == "Yes"

    if st.button("Diagnose"):
        try:
            result = run_expert_system(has_fever, has_cough)
            st.success(result)
        except Exception as e:
            st.error("CLIPS error occurred")
            st.code(str(e))


if __name__ == "__main__":
    main()
