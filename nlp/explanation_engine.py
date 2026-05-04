import spacy
import nltk

from nltk.tokenize import sent_tokenize

nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")


def generate_explanation(shap_values, feature_names, prediction_result=None):

    values = shap_values.values[0]

    feature_impacts = sorted(zip(feature_names, values), key=lambda x: abs(x[1]), reverse=True)
    
    negative_drivers = [(f, v) for f, v in feature_impacts if v < 0][:3]

    positive_drivers = [(f, v) for f, v in feature_impacts if v > 0][:3]

    reason_text = ""
    if prediction_result == "REJECTED" and negative_drivers:
        top_reason = negative_drivers[0]
        feature, impact = top_reason
        reason_text = f"Primary Rejection Reason: Your {feature} is below the approval threshold. This was the strongest factor influencing the rejection decision (impact: {impact:+.2f})."
    elif prediction_result == "APPROVED" and positive_drivers:
        top_reason = positive_drivers[0]
        feature, impact = top_reason
        reason_text = f"Primary Approval Reason: Your {feature} demonstrates strong loan eligibility. This was the key factor supporting your approval (impact: {impact:+.2f})."
    else:
        reason_text = "Your application was evaluated based on multiple factors including income, credit history, and loan details."

    coaching_tips = []
    
    if prediction_result == "REJECTED":

        if negative_drivers:
            for feature, impact in negative_drivers:
                if "Income" in feature:
                    coaching_tips.append(f"💡 Increase your {feature} - Consider waiting until your income increases or apply with a co-applicant.")
                elif "Credit_History" in feature:
                    coaching_tips.append(f"💡 Build your {feature} - Ensure all payments are on time for the next few months and re-apply.")
                elif "LoanAmount" in feature:
                    coaching_tips.append(f"💡 Reduce your {feature} - Request a lower loan amount that's more aligned with your income.")
                elif "Loan_Amount_Term" in feature:
                    coaching_tips.append(f"💡 Adjust your {feature} - Choose a shorter loan term to improve your approval chances.")
                elif "Property_Area" in feature:
                    coaching_tips.append(f"💡 {feature} affects approval odds - Consider properties in urban or semi-urban areas.")
                else:
                    coaching_tips.append(f"💡 Focus on improving {feature} - This metric significantly impacts your loan eligibility.")
        
        if not coaching_tips:
            coaching_tips = [
                "💡 Improve your income stability and credit history",
                "💡 Consider applying with a co-applicant to strengthen the application",
                "💡 Reduce the requested loan amount"
            ]
    else:

        coaching_tips = [
            "✓ Congratulations! Ensure you maintain your financial stability going forward.",
            "✓ Keep your credit score strong by making timely payments.",
            "✓ Monitor your income to maintain the approval eligibility status."
        ]
    
    sentences = []
    for feature, value in feature_impacts[:3]:
        direction = "approval" if value > 0 else "rejection"
        sentences.append(f"{feature} was a primary driver for {direction} (impact: {value:+.2f}).")

    full_text = " ".join(sentences)

    doc = nlp(full_text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    return {
        "reason": reason_text,
        "coaching": coaching_tips,
        "summary": full_text,
        "keywords": list(set(keywords)),  # Unique keywords
        "full_text": full_text
    }