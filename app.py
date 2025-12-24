import streamlit as st
from run_model import validate_metadata

st.set_page_config(
    page_title="💎 Proofelle — Digital Authenticity Prototype",
    page_icon="💎",
    layout="wide"
)

# Custom CSS to match the document's purple theme and striped background effect
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Roboto:wght@300;400;700&display=swap');

    /* Main background with subtle purple vertical stripes */
    [data-testid="stAppViewContainer"] {
        background: repeating-linear-gradient(
            90deg,
            #f5f0ff 0px,
            #f5f0ff 40px,
            #e6dbff 40px,
            #e6dbff 80px
        );
        background-attachment: fixed;
    }

    /* Purple accent color matching the document */
    :root {
        --proofelle-purple: #6A1B9A;
        --proofelle-light-purple: #9C27B0;
    }

    h1, h2, h3, .stTextInput > label, .stNumberInput > label, 
    .stDateInput > label, .stSelectbox > label{
        color: var(--proofelle-purple) !important;
        font-family: 'Audiowide', cursive !important;
    }

    .stButton > button {
        font-color: white;
        border-radius: 8px;
        border: 3px solid var(--proofelle-dark-purple) !important;
        box-shadow: 0 6px 12px rgba(106, 27, 154, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--proofelle-light-purple);
    }

    /* Subtle floating images with lower opacity on light background */
    .floating-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 1;
    }

    .floating-img {
        position: absolute;
        opacity: 0.06;
        animation: float-diagonal linear infinite;
        filter: brightness(1.1) drop-shadow(0 0 10px rgba(106, 27, 154, 0.2));
        border-radius: 12px;
    }

    @keyframes float-diagonal {
        0% { transform: translate(-200px, -200px) rotate(0deg) scale(1); }
        50% { transform: translate(calc(50vw), calc(50vh)) rotate(180deg) scale(1.1); }
        100% { transform: translate(calc(100vw + 200px), calc(100vh + 200px)) rotate(360deg) scale(1); }
    }

    /* Individual animation settings */
    .floating-img:nth-child(1) { width: 180px; animation-duration: 45s; animation-delay: 0s; top: 5%; left: -10%; }
    .floating-img:nth-child(2) { width: 220px; animation-duration: 55s; animation-delay: 3s; top: 15%; left: -20%; }
    .floating-img:nth-child(3) { width: 160px; animation-duration: 40s; animation-delay: 6s; top: 25%; left: -5%; }
    .floating-img:nth-child(4) { width: 200px; animation-duration: 60s; animation-delay: 9s; top: 35%; left: -15%; }
    .floating-img:nth-child(5) { width: 140px; animation-duration: 50s; animation-delay: 12s; top: 45%; left: -25%; }
    .floating-img:nth-child(6) { width: 190px; animation-duration: 48s; animation-delay: 15s; top: 55%; left: -8%; }
    .floating-img:nth-child(7) { width: 170px; animation-duration: 65s; animation-delay: 18s; top: 65%; left: -18%; }
    .floating-img:nth-child(8) { width: 210px; animation-duration: 52s; animation-delay: 21s; top: 75%; left: -12%; }
    .floating-img:nth-child(9) { width: 150px; animation-duration: 58s; animation-delay: 24s; top: 10%; left: -30%; }
    .floating-img:nth-child(10) { width: 230px; animation-duration: 70s; animation-delay: 27s; top: 30%; left: -10%; }
    .floating-img:nth-child(11) { width: 180px; animation-duration: 42s; animation-delay: 30s; top: 50%; left: -20%; }
    .floating-img:nth-child(12) { width: 160px; animation-duration: 62s; animation-delay: 33s; top: 70%; left: -5%; }
    .floating-img:nth-child(13) { width: 200px; animation-duration: 55s; animation-delay: 36s; top: 20%; left: -25%; }
    .floating-img:nth-child(14) { width: 190px; animation-duration: 48s; animation-delay: 39s; top: 40%; left: -15%; }
    .floating-img:nth-child(15) { width: 170px; animation-duration: 68s; animation-delay: 42s; top: 60%; left: -10%; }
    .floating-img:nth-child(16) { width: 220px; animation-duration: 50s; animation-delay: 45s; top: 80%; left: -20%; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Subtle floating luxury/NFT images
floating_html = """
<div class="floating-container">
    <img class="floating-img" src="https://hodinkee.imgix.net/uploads/images/818eb488-942b-4fe1-9923-1cd1fb7352f1/UNIQUE.jpg?ixlib=rails-1.1.0&fm=jpg&q=55&auto=format&usm=12" alt="NFT Watch">
    <img class="floating-img" src="https://imageio.forbes.com/specials-images/imageserve/623a58e45e1d30b6a7e1b98c/0x0.jpg?format=jpg&crop=1920,1080,x0,y53,safe&height=600&width=1200&fit=bounds" alt="Jacob & Co. NFT">
    <img class="floating-img" src="https://static01.nyt.com/images/2021/04/13/multimedia/13sp-watchNFT-inyt2/13sp-watchNFT-inyt2-videoSixteenByNineJumbo1600.jpg" alt="NFT Watch World">
    <img class="floating-img" src="https://louismoinet.com/wp-content/uploads/2022/02/LM-NFT-Newsletter_3.jpg" alt="Louis Moinet NFT">
    <img class="floating-img" src="https://images.prestigeonline.com/wp-content/uploads/sites/8/2022/11/16005258/9ee0112f-82de-c756-ef79-7b406d397bf4-1280x900.jpg" alt="Astronomia Metaverso">
    <img class="floating-img" src="https://assets.thehourmarkers.com/public/image_watch_spec_5446e1c683.png" alt="Metaverse Watches">
    <img class="floating-img" src="https://media.modernluxury.com/ntgpghfuax/styles/card-social/2024/11/21/Jacob-Co-Launches-Stellar-NFT-Timepieces-With-Real-World-Bonuses_Header.jpg.webp?version=6947a941d4d0b" alt="Jacob & Co. Astronomia">
    <img class="floating-img" src="https://ineichen.com/upload/medialibrary/730/zwkach4aldb757x9n6ug1hikiwspnmui.jpg" alt="NFT Auction">
    <img class="floating-img" src="https://cdn.i-scmp.com/sites/default/files/styles/og_postmag/public/d8/images/canvas/2023/02/09/c5280630-b542-47d4-89fc-dfc77c6aa2d0_a8b82757.jpg?itok=5RCi5hZm" alt="MetaBirkin NFT">
    <img class="floating-img" src="https://assets.vogue.com/photos/60c75f782d7c27e9cc7f5d3c/4:3/w_2000,h_1500,c_limit/digital-clothes-and-nfts-voguebus-mason-Rothschild-june-21-story.jpg" alt="Baby Birkin NFT">
    <img class="floating-img" src="https://thumbs.dreamstime.com/b/glowing-diamond-sparkle-dark-background-luxury-ad-399613075.jpg" alt="Glowing Diamond">
    <img class="floating-img" src="https://hautetime.s3.us-west-1.amazonaws.com/wp-content/uploads/2022/05/27030517/JACOB7.jpg" alt="Jacob & Co. Metaverse">
    <img class="floating-img" src="https://thumbs.dreamstime.com/b/shining-diamond-glowing-reflections-dark-background-realistic-sparkling-prism-light-effects-symbol-luxury-purity-406134978.jpg" alt="Shining Diamond NFT">
    <img class="floating-img" src="https://www.digital-wall-art-factory.com/wp-content/uploads/2024/05/DigitalWallArtFactory-Download-Digital-Face-wall-Art-jpg-nft-180.jpg" alt="Ethereal NFT Portrait">
    <img class="floating-img" src="https://theglossarymagazine.com/wp-content/uploads/CURRENTS.webp" alt="Luxury Fashion NFT">
    <img class="floating-img" src="https://lookaside.fbsbx.com/lookaside/crawler/media/?media_id=9168538343181872" alt="Ethereal Abstract Luxury">
</div>
"""
st.markdown(floating_html, unsafe_allow_html=True)

# Title and subtitle exactly matching the document
st.markdown("""
    <div style="text-align: left; margin-top: 40px; margin-left: 60px;">
        <h1 style="font-family: 'Audiowide', cursive; color: #6A1B9A; font-size: 80px; margin: 0; line-height: 1;">
            Proofelle'
        </h1>
        <h2 style="font-family: 'Audiowide', cursive; color: #6A1B9A; font-size: 36px; margin: 10px 0 20px 0; line-height: 1.2;">
            where authenticity becomes a trusted digital identity
        </h2>

    </div>
""", unsafe_allow_html=True)

# Main form section
st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("Step 1: Enter Product Details")

brand = st.text_input("Brand")
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

    with st.spinner("AI is validating metadata..."):
        result = validate_metadata(input_data)

    st.subheader("AI Validation Result")
    st.json(result)

    status = result.get("validation_status")

    if status == "PASS":
        st.success("✅ Metadata passed AI validation")
    elif status == "REVIEW":
        st.warning("⚠️ Metadata requires manual review")
    else:
        st.error("❌ Metadata failed validation")

    if result.get("warnings"):
        st.subheader("Warnings")
        for w in result["warnings"]:
            st.write(f"- {w}")

    if result.get("suggested_fixes"):
        st.subheader("Suggested Fixes")
        st.json(result["suggested_fixes"])