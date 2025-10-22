import streamlit as st

st.set_page_config(page_title="Proofelle Prototype", page_icon="💎")

st.title("💎 Proofelle — Digital Authenticity Prototype")

st.subheader("Step 1: Enter Product Details")
brand = st.text_input("Brand (e.g., Rolex, Louis Vuitton)")
model_name = st.text_input("Model Name")
serial_number = st.text_input("Serial Number")
price_omr = st.number_input("Price (OMR)", min_value=0.0)
retailer_id = st.text_input("Retailer ID")
purchase_date = st.date_input("Purchase Date")

if st.button("Validate Metadata"):
    input_data = {
        "brand": brand,
        "model_name": model_name,
        "serial_number": serial_number,
        "price_omr": price_omr,
        "retailer_id": retailer_id,
        "purchase_date": str(purchase_date)
    }

    # result = validate_metadata(input_data)
    # st.write("### AI Validation Result")
    # st.json(result)

    # if result["auto_filled"]:
    #     st.success("AI auto-filled some missing fields:")
    #     st.json(result["auto_filled"])

    # if result["warnings"]:
    #     st.warning("Warnings detected:")
    #     for w in result["warnings"]:
    #         st.write("- " + w)

    # if st.button("Mint NFT"):
    #     nft, file_name = generate_nft(input_data, result["score"])
    #     st.success(f"NFT metadata created → `{file_name}`")
    #     st.json(nft)
