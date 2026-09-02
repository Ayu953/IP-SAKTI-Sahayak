import streamlit as st

def render_classification_page(vector_store=None):
    st.markdown("## 🔍 Formulation Classifier Wizard")
    st.caption("Answer 2-3 quick questions to determine your product category and its exact IP & ABS posture.")
    
    st.markdown("---")
    
    # Question 1: Intended Use
    use_case = st.radio(
        "**1. What is the primary intended use of your product?**", 
        ["Medicinal / Therapeutic", "Food / Nutritional (Ayurveda-Aahar)", "Cosmetic / Beautification"], 
        index=None
    )
    
    if use_case == "Food / Nutritional (Ayurveda-Aahar)":
        show_result(
            category="Ayurveda-Aahar (Nutraceutical)", 
            regulatory="FSSAI Ayurveda-Aahar Regulations.",
            ip_posture="Patents possible only if the processing/manufacturing method is novel. Traditional recipes are barred under Section 3(p). Trademarks highly recommended.", 
            abs_posture="Standard ABS guidelines apply if Indian biological resources are accessed for commercial utilization."
        )
        
    elif use_case == "Cosmetic / Beautification":
        show_result(
            category="Ayurvedic Cosmetic", 
            regulatory="Drugs and Cosmetics Act, 1940 (Cosmetics Division).",
            ip_posture="Eligible for Trademarks (brand name) and Design patents (packaging). Formulation patents are difficult if combining known traditional herbs.", 
            abs_posture="Requires State Biodiversity Board intimation (for Indians) or NBA approval (for foreigners)."
        )
        
    elif use_case == "Medicinal / Therapeutic":
        # Question 2: Classical vs Proprietary
        classical = st.radio(
            "**2. Are all active ingredients and the exact method of preparation drawn directly from an authoritative classical text (e.g., Charaka Samhita)?**", 
            ["Yes, exactly as per classical texts (First Schedule)", "No, it is a new combination or uses modern delivery formats (e.g., syrups, capsules)"], 
            index=None
        )
        
        if classical == "Yes, exactly as per classical texts (First Schedule)":
            show_result(
                category="Classical / Generic Ayurvedic Medicine",
                regulatory="Drugs and Cosmetics Act, 1940 (Chapter IVA).",
                ip_posture="Considered Protected Traditional Knowledge. Strictly barred from patenting under Section 3(p) of the Patents Act. Defended internationally by TKDL. Cannot be patented, but can be trademarked.", 
                abs_posture="Exempted from strict ABS approvals for local registered practitioners (Vaidyas), but commercial manufacturing requires compliance."
            )
            
        elif classical == "No, it is a new combination or uses modern delivery formats (e.g., syrups, capsules)":
            # Question 3: Proprietary vs New Drug
            novelty = st.radio(
                "**3. Does the formulation contain highly purified fractions of plants (Phytopharmaceuticals) or make entirely new, unproven therapeutic claims?**", 
                ["No, it is just a new combination of known traditional herbs for known ailments.", "Yes, it uses purified active fractions or makes a new therapeutic claim (Requires clinical trials)"], 
                index=None
            )
            
            if novelty == "No, it is just a new combination of known traditional herbs for known ailments.":
                show_result(
                    category="Patent or Proprietary Ayurvedic Medicine", 
                    regulatory="Drugs and Cosmetics Act, 1940 (Proprietary Medicine License).",
                    ip_posture="To get a patent, you MUST prove 'Synergistic Effect' (the combination works better than individual herbs). Otherwise, it will be rejected under Section 3(p).", 
                    abs_posture="Commercial utilization requires ABS compliance and benefit-sharing via National Biodiversity Authority (NBA)."
                )
                
            elif novelty == "Yes, it uses purified active fractions or makes a new therapeutic claim (Requires clinical trials)":
                show_result(
                    category="Phytopharmaceutical / New Drug", 
                    regulatory="New Drugs and Clinical Trials Rules, 2019 (Requires CDSCO approval).",
                    ip_posture="High Patent Potential. Not barred by Section 3(p) if it is a novel, purified fraction with proven clinical efficacy.", 
                    abs_posture="Strict ABS compliance required under the Biological Diversity Act and Nagoya Protocol prior to patent grant."
                )

def show_result(category, regulatory, ip_posture, abs_posture):
    st.markdown("### 📋 Classification Verdict")
    st.success(f"**Product Category:** {category}")
    st.info(f"🏛️ **Regulatory Framework:** {regulatory}")
    st.error(f"🛡️ **IP Posture (Patents/TK):** {ip_posture}")
    st.warning(f"🌿 **ABS Posture (Biodiversity):** {abs_posture}")