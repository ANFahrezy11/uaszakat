import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io

# Configure page
st.set_page_config(
    page_title="Pembayaran Zakat",
    page_icon="🕌",
    layout="wide"
)

# Custom CSS for Indonesian currency formatting and Islamic styling
st.markdown("""
<style>
    /* Main background styling */
    .stApp {
        background: linear-gradient(135deg, #ADFF2F 0%, #98FB98 100%);
        min-height: 100vh;
    }
    
    /* Islamic ornament watermark */
    .stApp::before {
        content: '';
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 200px;
        height: 200px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Cg fill='%23228B22' opacity='0.3'%3E%3Cpath d='M100 20 L120 60 L160 60 L130 85 L140 125 L100 105 L60 125 L70 85 L40 60 L80 60 Z'/%3E%3Ccircle cx='100' cy='100' r='15' fill='%23FFD700'/%3E%3Cpath d='M100 130 Q90 140 80 130 Q90 120 100 130 Q110 120 120 130 Q110 140 100 130' fill='%23228B22'/%3E%3Cpath d='M70 50 Q65 45 60 50 Q65 55 70 50' fill='%23FFD700'/%3E%3Cpath d='M140 50 Q135 45 130 50 Q135 55 140 50' fill='%23FFD700'/%3E%3C/g%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        z-index: -1;
        pointer-events: none;
    }
    
    /* Main container styling */
    .main > div {
        padding: 2rem 1rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(34, 139, 34, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #228B22 0%, #32CD32 100%);
        border-right: 3px solid #FFD700;
    }
    
    .css-1d391kg .element-container {
        color: white !important;
    }
    
    /* Header styling with Islamic calligraphy feel */
    h1, h2, h3 {
        color: #1B4332 !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 2px 2px 4px rgba(255, 215, 0, 0.3);
        border-bottom: 3px solid #FFD700;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Metric cards with Islamic theme */
    .metric-card {
        background: linear-gradient(135deg, #F0F8E8 0%, #E8F5E8 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(34, 139, 34, 0.2);
        text-align: center;
        border: 2px solid #FFD700;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Cg fill='%23FFD700' opacity='0.1'%3E%3Cpath d='M30 5 L35 20 L50 20 L38 30 L43 45 L30 37 L17 45 L22 30 L10 20 L25 20 Z'/%3E%3C/g%3E%3C/svg%3E") repeat;
        z-index: 0;
    }
    
    .metric-card > * {
        position: relative;
        z-index: 1;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1B4332;
        text-shadow: 1px 1px 2px rgba(255, 215, 0, 0.5);
    }
    
    .metric-label {
        color: #2E8B57;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Form styling with Lebaran theme */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #98FB98;
        border-radius: 10px;
        color: #1B4332;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Button styling with Islamic theme */
    .stButton > button {
        background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);
        color: white;
        border: 2px solid #FFD700;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(34, 139, 34, 0.4);
    }
    
    /* Primary button special styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1B4332;
        border-color: #228B22;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
    }
    
    /* Table styling for history */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        border: 2px solid #98FB98;
        overflow: hidden;
    }
    
    .stDataFrame table {
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #228B22 0%, #32CD32 100%);
        color: white;
        font-weight: bold;
        padding: 15px;
        text-align: center;
        border-bottom: 2px solid #FFD700;
    }
    
    .stDataFrame td {
        padding: 12px 15px;
        border-bottom: 1px solid #E8F5E8;
        text-align: center;
    }
    
    .stDataFrame tr:nth-child(even) {
        background: rgba(173, 255, 47, 0.1);
    }
    
    .stDataFrame tr:hover {
        background: rgba(255, 215, 0, 0.2);
        transform: scale(1.01);
        transition: all 0.2s ease;
    }
    
    /* Form container styling */
    .stForm {
        background: rgba(255, 255, 255, 0.9);
        border: 3px solid #FFD700;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(34, 139, 34, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stForm::before {
        content: '';
        position: absolute;
        top: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cg fill='%23FFD700' opacity='0.3'%3E%3Cpath d='M20 5 L23 15 L33 15 L25 22 L28 32 L20 27 L12 32 L15 22 L7 15 L17 15 Z'/%3E%3C/g%3E%3C/svg%3E");
        background-size: contain;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #90EE90 0%, #98FB98 100%);
        border: 2px solid #32CD32;
        border-radius: 10px;
        color: #1B4332;
    }
    
    .stError {
        background: linear-gradient(135deg, #FFB6C1 0%, #FFA07A 100%);
        border: 2px solid #DC143C;
        border-radius: 10px;
    }
    
    /* Info box styling */
    .stInfo {
        background: linear-gradient(135deg, #E0F6FF 0%, #87CEEB 100%);
        border: 2px solid #4169E1;
        border-radius: 10px;
        color: #1B4332;
    }
    
    /* Sidebar title styling */
    .css-1d391kg h1 {
        color: #FFD700 !important;
        text-align: center;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 10px;
    }
    
    /* Islamic ornament for corners */
    .corner-ornament {
        position: fixed;
        width: 80px;
        height: 80px;
        opacity: 0.2;
        z-index: -1;
        pointer-events: none;
    }
    
    .corner-ornament.top-left {
        top: 20px;
        left: 20px;
    }
    
    .corner-ornament.top-right {
        top: 20px;
        right: 20px;
    }
    
    .corner-ornament.bottom-left {
        bottom: 20px;
        left: 20px;
    }
    
    /* Rice bag icon for data beras page */
    .rice-icon {
        position: absolute;
        top: 10px;
        left: 10px;
        width: 60px;
        height: 60px;
        opacity: 0.4;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Cg fill='%23D2691E'%3E%3Crect x='15' y='20' width='30' height='25' rx='5' ry='5'/%3E%3Ctext x='30' y='35' text-anchor='middle' fill='white' font-size='8' font-weight='bold'%3EBERAS%3C/text%3E%3Ccircle cx='20' cy='15' r='2' fill='%23F5DEB3'/%3E%3Ccircle cx='25' cy='12' r='1.5' fill='%23F5DEB3'/%3E%3Ccircle cx='30' cy='14' r='1.5' fill='%23F5DEB3'/%3E%3Ccircle cx='35' cy='11' r='2' fill='%23F5DEB3'/%3E%3Ccircle cx='40' cy='15' r='1.5' fill='%23F5DEB3'/%3E%3C/g%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
    }
    
    /* Money/envelope icon for payment page */
    .money-icon {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        opacity: 0.4;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Cg fill='%23FFD700'%3E%3Crect x='10' y='20' width='40' height='25' rx='3' ry='3' stroke='%23228B22' stroke-width='2'/%3E%3Ccircle cx='30' cy='32.5' r='6' fill='%23228B22'/%3E%3Ctext x='30' y='36' text-anchor='middle' fill='%23FFD700' font-size='8' font-weight='bold'%3ERp%3C/text%3E%3Cpath d='M15 20 L30 30 L45 20' stroke='%23228B22' stroke-width='2' fill='none'/%3E%3C/g%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
    }
    
    /* Calendar icon for dates */
    .calendar-icon {
        display: inline-block;
        width: 16px;
        height: 16px;
        margin-right: 5px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cg fill='%23228B22'%3E%3Crect x='2' y='3' width='12' height='11' rx='1' ry='1' stroke='%23228B22' stroke-width='1' fill='%23F0F8E8'/%3E%3Cline x1='5' y1='1' x2='5' y2='5' stroke='%23228B22' stroke-width='1'/%3E%3Cline x1='11' y1='1' x2='11' y2='5' stroke='%23228B22' stroke-width='1'/%3E%3Cline x1='2' y1='6' x2='14' y2='6' stroke='%23228B22' stroke-width='1'/%3E%3C/g%3E%3C/svg%3E");
        background-size: contain;
        background-repeat: no-repeat;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# Add corner ornaments
st.markdown("""
<div class="corner-ornament top-left">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <g fill="#FFD700" opacity="0.3">
            <path d="M10 10 Q20 5 30 10 Q20 15 10 10"/>
            <path d="M40 10 Q50 5 60 10 Q50 15 40 10"/>
            <path d="M10 30 Q20 25 30 30 Q20 35 10 30"/>
            <path d="M40 30 Q50 25 60 30 Q50 35 40 30"/>
            <circle cx="35" cy="50" r="8" fill="#228B22"/>
            <path d="M35 58 Q30 63 25 58 Q30 53 35 58 Q40 53 45 58 Q40 63 35 58"/>
        </g>
    </svg>
</div>
<div class="corner-ornament top-right">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <g fill="#32CD32" opacity="0.3">
            <path d="M20 15 L25 25 L35 25 L28 32 L31 42 L20 37 L9 42 L12 32 L5 25 L15 25 Z"/>
            <circle cx="20" cy="55" r="6" fill="#FFD700"/>
            <path d="M50 20 Q55 15 60 20 Q55 25 50 20"/>
            <path d="M65 35 Q70 30 75 35 Q70 40 65 35"/>
        </g>
    </svg>
</div>
<div class="corner-ornament bottom-left">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <g fill="#228B22" opacity="0.2">
            <circle cx="25" cy="25" r="12" fill="none" stroke="#FFD700" stroke-width="2"/>
            <path d="M25 13 L28 20 L35 20 L30 25 L32 32 L25 28 L18 32 L20 25 L15 20 L22 20 Z"/>
            <path d="M50 60 Q60 55 70 60 Q60 65 50 60"/>
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
def initialize_session_state():
    if 'zakat_payments' not in st.session_state:
        st.session_state.zakat_payments = []
    
    if 'rice_prices' not in st.session_state:
        st.session_state.rice_prices = [
            {"id": 1, "harga": 10000.00},
            {"id": 2, "harga": 15000.00},
            {"id": 3, "harga": 20000.00},
            {"id": 4, "harga": 17000.00},
            {"id": 5, "harga": 13500.00}
        ]

# Helper functions
def format_currency(amount):
    """Format number as Indonesian Rupiah"""
    return f"Rp {amount:,.2f}".replace(",", ".")

def get_zakat_types():
    """Get available zakat types"""
    return [
        "Zakat Fitrah",
        "Zakat Mal",
        "Zakat Profesi",
        "Zakat Emas",
        "Zakat Perak",
        "Zakat Perdagangan"
    ]

def get_payment_methods():
    """Get available payment methods"""
    return [
        "Tunai",
        "Transfer Bank",
        "E-Wallet",
        "Kartu Kredit"
    ]

def save_payment(payment_data):
    """Save payment to session state"""
    payment_data['id'] = len(st.session_state.zakat_payments) + 1
    payment_data['tanggal_input'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.zakat_payments.append(payment_data)

def delete_payment(payment_id):
    """Delete payment from session state"""
    st.session_state.zakat_payments = [
        p for p in st.session_state.zakat_payments if p['id'] != payment_id
    ]

def update_payment(payment_id, updated_data):
    """Update payment in session state"""
    for i, payment in enumerate(st.session_state.zakat_payments):
        if payment['id'] == payment_id:
            updated_data['id'] = payment_id
            updated_data['tanggal_input'] = payment.get('tanggal_input', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            st.session_state.zakat_payments[i] = updated_data
            break

def add_rice_price(price):
    """Add new rice price"""
    new_id = max([rp['id'] for rp in st.session_state.rice_prices], default=0) + 1
    st.session_state.rice_prices.append({"id": new_id, "harga": price})

def delete_rice_price(price_id):
    """Delete rice price"""
    st.session_state.rice_prices = [
        rp for rp in st.session_state.rice_prices if rp['id'] != price_id
    ]

def export_to_excel():
    """Export payments to Excel"""
    if not st.session_state.zakat_payments:
        return None
    
    df = pd.DataFrame(st.session_state.zakat_payments)
    
    # Reorder columns for better presentation
    column_order = ['id', 'nama', 'jumlah_jiwa', 'jenis_zakat', 'metode_pembayaran', 
                   'total_bayar', 'nominal_dibayar', 'kembalian', 'tanggal_bayar', 'tanggal_input']
    
    # Only include columns that exist
    available_columns = [col for col in column_order if col in df.columns]
    df = df[available_columns]
    
    # Rename columns to Indonesian
    column_names = {
        'id': 'ID',
        'nama': 'Nama',
        'jumlah_jiwa': 'Jumlah Jiwa',
        'jenis_zakat': 'Jenis Zakat',
        'metode_pembayaran': 'Metode Pembayaran',
        'total_bayar': 'Total Bayar',
        'nominal_dibayar': 'Nominal Dibayar',
        'kembalian': 'Kembalian',
        'tanggal_bayar': 'Tanggal Bayar',
        'tanggal_input': 'Tanggal Input'
    }
    
    df = df.rename(columns=column_names)
    
    # Convert to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Pembayaran Zakat')
    
    return output.getvalue()

# Main application
def main():
    initialize_session_state()
    
    # Check for menu override from dashboard buttons
    if 'menu_override' in st.session_state:
        menu = st.session_state.menu_override
        del st.session_state.menu_override
    else:
        # Sidebar navigation
        st.sidebar.title("🕌 Menu Navigasi")
        st.sidebar.markdown("---")
        menu = st.sidebar.selectbox(
            "Pilih Menu:",
            ["Dashboard", "Tambah Pembayaran", "Riwayat Pembayaran", "Data Harga Beras"]
        )
    
    if menu == "Dashboard":
        show_dashboard()
    elif menu == "Tambah Pembayaran":
        show_payment_form()
    elif menu == "Riwayat Pembayaran":
        show_payment_history()
    elif menu == "Data Harga Beras":
        show_rice_prices()

def show_dashboard():
    """Display main dashboard"""
    st.title("🌙 Dashboard Pembayaran Zakat Lebaran 🌙")
    
    # Add Lebaran greeting
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                padding: 1rem; border-radius: 15px; margin-bottom: 2rem; border: 2px solid #228B22;">
        <h3 style="color: #1B4332; margin: 0; font-family: 'Segoe UI', sans-serif; border: none; text-shadow: none;">
            🎉 Selamat Hari Raya Idul Fitri 🎉
        </h3>
        <p style="color: #2E8B57; margin: 5px 0 0 0; font-weight: 600;">
            Mohon Maaf Lahir dan Batin
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate statistics
    total_payments = sum([p['total_bayar'] for p in st.session_state.zakat_payments])
    transaction_count = len(st.session_state.zakat_payments)
    last_update = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Total Pembayaran Zakat</div>
            <div class="metric-value">{format_currency(total_payments)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Jumlah Transaksi</div>
            <div class="metric-value">{transaction_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⏰ Terakhir Diperbarui</div>
            <div class="metric-value" style="font-size: 1rem;">{last_update}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent payments table
    st.subheader("📋 Daftar Pembayaran Terbaru")
    
    if st.session_state.zakat_payments:
        # Get last 5 payments
        recent_payments = st.session_state.zakat_payments[-5:]
        
        # Create DataFrame for display
        df_display = pd.DataFrame(recent_payments)
        
        # Format currency columns
        if 'total_bayar' in df_display.columns:
            df_display['total_bayar'] = df_display['total_bayar'].apply(format_currency)
        if 'nominal_dibayar' in df_display.columns:
            df_display['nominal_dibayar'] = df_display['nominal_dibayar'].apply(format_currency)
        if 'kembalian' in df_display.columns:
            df_display['kembalian'] = df_display['kembalian'].apply(format_currency)
        
        # Add calendar icon to dates
        if 'tanggal_bayar' in df_display.columns:
            df_display['tanggal_bayar'] = df_display['tanggal_bayar'].apply(
                lambda x: f"📅 {x}" if pd.notna(x) else ""
            )
        
        # Rename columns
        column_renames = {
            'id': 'ID',
            'nama': 'Nama',
            'jumlah_jiwa': 'Jumlah Jiwa',
            'jenis_zakat': 'Jenis Zakat',
            'metode_pembayaran': 'Metode Pembayaran',
            'total_bayar': 'Total Bayar',
            'nominal_dibayar': 'Nominal Dibayar',
            'kembalian': 'Kembalian',
            'tanggal_bayar': 'Tanggal Bayar'
        }
        
        display_columns = ['ID', 'Nama', 'Jenis Zakat', 'Total Bayar', 'Tanggal Bayar']
        df_display = df_display.rename(columns=column_renames)
        
        # Show only selected columns
        available_display_cols = [col for col in display_columns if col in df_display.columns]
        if available_display_cols:
            st.dataframe(df_display[available_display_cols], use_container_width=True)
    else:
        st.info("🌙 Belum ada data pembayaran zakat. Mari mulai dengan menambahkan pembayaran pertama!")
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Tambah Pembayaran Zakat", type="primary", use_container_width=True):
            st.session_state.menu_override = "Tambah Pembayaran"
            st.rerun()
    
    with col2:
        if st.button("📊 Riwayat Pembayaran", use_container_width=True):
            st.session_state.menu_override = "Riwayat Pembayaran"
            st.rerun()
    
    with col3:
        if st.button("🌾 Data Harga Beras", use_container_width=True):
            st.session_state.menu_override = "Data Harga Beras"
            st.rerun()

def show_payment_form():
    """Display payment form with Islamic theme"""
    st.title("💰 Melakukan Pembayaran Zakat")
    
    # Add money icon
    st.markdown('<div class="money-icon"></div>', unsafe_allow_html=True)
    
    # Add Islamic greeting
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E8 0%, #F0F8E8 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; 
                border-left: 5px solid #FFD700; text-align: center;">
        <p style="color: #1B4332; margin: 0; font-style: italic;">
            "Dan dirikanlah shalat, tunaikanlah zakat..." - QS. Al-Baqarah: 43
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("payment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 Data Muzakki")
            nama = st.text_input("Nama Lengkap*", placeholder="Masukkan nama lengkap")
            jumlah_jiwa = st.number_input("Jumlah Jiwa dalam Keluarga", min_value=1, value=1, step=1, 
                                        help="Jumlah anggota keluarga yang akan dibayarkan zakatnya")
            jenis_zakat = st.selectbox("Jenis Zakat*", ["Pilih Jenis Zakat"] + get_zakat_types())
            metode_pembayaran = st.selectbox("Metode Pembayaran*", ["Pilih Metode Pembayaran"] + get_payment_methods())
        
        with col2:
            st.markdown("### 💳 Informasi Pembayaran")
            total_bayar = st.number_input("Total Bayar (Rp)*", min_value=0.0, format="%.2f", step=1000.0,
                                        help="Jumlah zakat yang harus dibayar")
            nominal_dibayar = st.number_input("Nominal Dibayar (Rp)*", min_value=0.0, format="%.2f", step=1000.0,
                                            help="Jumlah uang yang diberikan")
            
            # Calculate change automatically
            kembalian = max(0, nominal_dibayar - total_bayar) if nominal_dibayar > 0 and total_bayar > 0 else 0
            st.number_input("Kembalian (Rp)", value=kembalian, disabled=True, format="%.2f")
            
            tanggal_bayar = st.date_input("📅 Tanggal Bayar*", value=datetime.now().date())
        
        # Form submission buttons
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("💾 Simpan Pembayaran", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("🔙 Kembali ke Dashboard", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            if not nama.strip():
                errors.append("❌ Nama harus diisi")
            if jenis_zakat == "Pilih Jenis Zakat":
                errors.append("❌ Pilih jenis zakat")
            if metode_pembayaran == "Pilih Metode Pembayaran":
                errors.append("❌ Pilih metode pembayaran")
            if total_bayar <= 0:
                errors.append("❌ Total bayar harus lebih dari 0")
            if nominal_dibayar <= 0:
                errors.append("❌ Nominal dibayar harus lebih dari 0")
            if nominal_dibayar < total_bayar:
                errors.append("❌ Nominal dibayar tidak boleh kurang dari total bayar")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save payment
                payment_data = {
                    'nama': nama.strip(),
                    'jumlah_jiwa': jumlah_jiwa,
                    'jenis_zakat': jenis_zakat,
                    'metode_pembayaran': metode_pembayaran,
                    'total_bayar': total_bayar,
                    'nominal_dibayar': nominal_dibayar,
                    'kembalian': kembalian,
                    'tanggal_bayar': tanggal_bayar.strftime("%Y-%m-%d")
                }
                
                save_payment(payment_data)
                st.success("✅ Alhamdulillah! Pembayaran zakat berhasil disimpan. Barakallahu fiikum!")
                st.balloons()
                
                # Reset form by rerunning
                st.rerun()
        
        if cancel:
            st.session_state.menu_override = "Dashboard"
            st.rerun()

def show_payment_history():
    """Display payment history with CRUD operations"""
    st.title("📚 Riwayat Pembayaran Zakat")
    
    # Add Islamic quote
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E8 0%, #F0F8E8 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; 
                border-left: 5px solid #FFD700; text-align: center;">
        <p style="color: #1B4332; margin: 0; font-style: italic;">
            "Ambillah zakat dari sebagian harta mereka..." - QS. At-Taubah: 103
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        if st.button("🔙 Kembali", use_container_width=True):
            st.session_state.menu_override = "Dashboard"
            st.rerun()
    
    with col2:
        excel_data = export_to_excel()
        if excel_data:
            st.download_button(
                label="📊 Export Excel",
                data=excel_data,
                file_name=f"pembayaran_zakat_lebaran_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📊 Export Excel", disabled=True, use_container_width=True, 
                     help="Tidak ada data untuk diekspor")
    
    with col3:
        if st.button("🗑️ Hapus Semua", use_container_width=True, 
                     help="Hapus semua data pembayaran"):
            if st.session_state.zakat_payments:
                # Show confirmation in session state
                st.session_state.show_delete_all_confirm = True
    
    # Show delete confirmation if needed
    if getattr(st.session_state, 'show_delete_all_confirm', False):
        st.warning("⚠️ Apakah Anda yakin ingin menghapus semua data pembayaran?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Ya, Hapus Semua", type="primary"):
                st.session_state.zakat_payments = []
                st.session_state.show_delete_all_confirm = False
                st.success("✅ Semua data pembayaran berhasil dihapus")
                st.rerun()
        with col2:
            if st.button("❌ Batal"):
                st.session_state.show_delete_all_confirm = False
                st.rerun()
    
    st.markdown("---")
    
    # Display payments table
    if st.session_state.zakat_payments:
        st.subheader(f"📋 Daftar Pembayaran ({len(st.session_state.zakat_payments)} transaksi)")
        
        # Create DataFrame
        df = pd.DataFrame(st.session_state.zakat_payments)
        
        # Format currency columns
        currency_columns = ['total_bayar', 'nominal_dibayar', 'kembalian']
        for col in currency_columns:
            if col in df.columns:
                df[col] = df[col].apply(format_currency)
        
        # Add calendar icons to dates
        if 'tanggal_bayar' in df.columns:
            df['tanggal_bayar'] = df['tanggal_bayar'].apply(
                lambda x: f"📅 {x}" if pd.notna(x) else ""
            )
        
        # Rename columns for display
        column_renames = {
            'id': 'ID',
            'nama': 'Nama Muzakki',
            'jumlah_jiwa': 'Jumlah Jiwa',
            'jenis_zakat': 'Jenis Zakat',
            'metode_pembayaran': 'Metode Pembayaran',
            'total_bayar': 'Total Bayar',
            'nominal_dibayar': 'Nominal Dibayar',
            'kembalian': 'Kembalian',
            'tanggal_bayar': 'Tanggal Bayar',
            'tanggal_input': 'Tanggal Input'
        }
        
        df_display = df.rename(columns=column_renames)
        
        # Select columns to display
        display_columns = ['ID', 'Nama Muzakki', 'Jenis Zakat', 'Total Bayar', 
                          'Nominal Dibayar', 'Kembalian', 'Tanggal Bayar']
        available_columns = [col for col in display_columns if col in df_display.columns]
        
        if available_columns:
            st.dataframe(df_display[available_columns], use_container_width=True)
        
        # Individual record management
        st.markdown("---")
        st.subheader("🔧 Kelola Data Pembayaran")
        
        # Select payment to edit/delete
        payment_options = [f"ID: {p['id']} - {p['nama']} ({p['jenis_zakat']})" 
                          for p in st.session_state.zakat_payments]
        
        if payment_options:
            selected_payment = st.selectbox(
                "Pilih pembayaran untuk diedit atau dihapus:",
                ["Pilih pembayaran..."] + payment_options
            )
            
            if selected_payment != "Pilih pembayaran...":
                payment_id = int(selected_payment.split(":")[1].split(" -")[0])
                payment_data = next((p for p in st.session_state.zakat_payments if p['id'] == payment_id), None)
                
                if payment_data:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("✏️ Edit Pembayaran", use_container_width=True):
                            st.session_state.edit_payment_id = payment_id
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ Hapus Pembayaran", use_container_width=True):
                            delete_payment(payment_id)
                            st.success(f"✅ Pembayaran ID {payment_id} berhasil dihapus")
                            st.rerun()
        
        # Edit form
        if hasattr(st.session_state, 'edit_payment_id'):
            edit_id = st.session_state.edit_payment_id
            edit_data = next((p for p in st.session_state.zakat_payments if p['id'] == edit_id), None)
            
            if edit_data:
                st.markdown("---")
                st.subheader(f"✏️ Edit Pembayaran ID: {edit_id}")
                
                with st.form(f"edit_form_{edit_id}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_nama = st.text_input("Nama", value=edit_data.get('nama', ''))
                        edit_jiwa = st.number_input("Jumlah Jiwa", value=edit_data.get('jumlah_jiwa', 1), min_value=1)
                        edit_jenis = st.selectbox("Jenis Zakat", get_zakat_types(), 
                                                index=get_zakat_types().index(edit_data.get('jenis_zakat', get_zakat_types()[0])) if edit_data.get('jenis_zakat') in get_zakat_types() else 0)
                        edit_metode = st.selectbox("Metode Pembayaran", get_payment_methods(),
                                                 index=get_payment_methods().index(edit_data.get('metode_pembayaran', get_payment_methods()[0])) if edit_data.get('metode_pembayaran') in get_payment_methods() else 0)
                    
                    with col2:
                        edit_total = st.number_input("Total Bayar", value=float(edit_data.get('total_bayar', 0)), min_value=0.0)
                        edit_nominal = st.number_input("Nominal Dibayar", value=float(edit_data.get('nominal_dibayar', 0)), min_value=0.0)
                        edit_kembalian = max(0, edit_nominal - edit_total) if edit_nominal > 0 and edit_total > 0 else 0
                        st.number_input("Kembalian", value=edit_kembalian, disabled=True)
                        
                        # Parse date string
                        try:
                            edit_date = datetime.strptime(edit_data.get('tanggal_bayar', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
                        except:
                            edit_date = datetime.now().date()
                        edit_tanggal = st.date_input("Tanggal Bayar", value=edit_date)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                            updated_data = {
                                'nama': edit_nama,
                                'jumlah_jiwa': edit_jiwa,
                                'jenis_zakat': edit_jenis,
                                'metode_pembayaran': edit_metode,
                                'total_bayar': edit_total,
                                'nominal_dibayar': edit_nominal,
                                'kembalian': edit_kembalian,
                                'tanggal_bayar': edit_tanggal.strftime('%Y-%m-%d')
                            }
                            update_payment(edit_id, updated_data)
                            del st.session_state.edit_payment_id
                            st.success("✅ Pembayaran berhasil diperbarui!")
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Batal", use_container_width=True):
                            del st.session_state.edit_payment_id
                            st.rerun()
    else:
        st.info("🌙 Belum ada riwayat pembayaran zakat. Silakan tambahkan pembayaran pertama melalui menu 'Tambah Pembayaran'.")

def show_rice_prices():
    """Display rice prices management with Islamic theme"""
    st.title("🌾 Data Penerimaan Beras Zakat")
    
    # Add rice icon
    st.markdown('<div class="rice-icon"></div>', unsafe_allow_html=True)
    
    # Add Islamic quote about zakat fitrah
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F5DEB3 0%, #DEB887 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem; 
                border-left: 5px solid #D2691E; text-align: center;">
        <p style="color: #8B4513; margin: 0; font-style: italic; font-weight: 600;">
            "Zakat Fitrah dengan Beras - Mensucikan Jiwa di Bulan Ramadhan"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation button
    if st.button("🔙 Kembali ke Dashboard", use_container_width=False):
        st.session_state.menu_override = "Dashboard"
        st.rerun()
    
    st.markdown("---")
    
    # Add new rice price
    st.subheader("➕ Tambah Harga Beras Baru")
    
    with st.form("add_rice_price"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_price = st.number_input(
                "Harga Beras per Kg (Rp)",
                min_value=0.0,
                format="%.2f",
                step=500.0,
                help="Masukkan harga beras per kilogram"
            )
        
        with col2:
            if st.form_submit_button("💾 Tambah Harga", type="primary", use_container_width=True):
                if new_price > 0:
                    add_rice_price(new_price)
                    st.success(f"✅ Harga beras {format_currency(new_price)} berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("❌ Harga harus lebih dari 0")
    
    st.markdown("---")
    
    # Display current rice prices
    st.subheader("📋 Daftar Harga Beras Saat Ini")
    
    if st.session_state.rice_prices:
        # Create DataFrame
        df_rice = pd.DataFrame(st.session_state.rice_prices)
        df_rice['harga_formatted'] = df_rice['harga'].apply(format_currency)
        
        # Calculate statistics
        avg_price = df_rice['harga'].mean()
        min_price = df_rice['harga'].min()
        max_price = df_rice['harga'].max()
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #F5DEB3 0%, #DEB887 100%);">
                <div class="metric-label">📊 Harga Rata-rata</div>
                <div class="metric-value" style="color: #8B4513;">{format_currency(avg_price)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #90EE90 0%, #98FB98 100%);">
                <div class="metric-label">💰 Harga Terendah</div>
                <div class="metric-value" style="color: #006400;">{format_currency(min_price)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #FFB6C1 0%, #FFA07A 100%);">
                <div class="metric-label">💎 Harga Tertinggi</div>
                <div class="metric-value" style="color: #B22222;">{format_currency(max_price)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display table
        df_display = df_rice[['id', 'harga_formatted']].rename(columns={
            'id': 'ID',
            'harga_formatted': 'Harga per Kg'
        })
        
        st.dataframe(df_display, use_container_width=True)
        
        # Delete rice price
        st.markdown("---")
        st.subheader("🗑️ Hapus Harga Beras")
        
        price_options = [f"ID: {rp['id']} - {format_currency(rp['harga'])}" 
                        for rp in st.session_state.rice_prices]
        
        selected_price = st.selectbox(
            "Pilih harga untuk dihapus:",
            ["Pilih harga..."] + price_options
        )
        
        if selected_price != "Pilih harga...":
            price_id = int(selected_price.split(":")[1].split(" -")[0])
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🗑️ Hapus", type="primary"):
                    delete_rice_price(price_id)
                    st.success(f"✅ Harga dengan ID {price_id} berhasil dihapus!")
                    st.rerun()
        
        # Quick actions
        st.markdown("---")
        st.subheader("⚡ Aksi Cepat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌾 Tambah Harga Standar", use_container_width=True, 
                        help="Tambah beberapa harga beras standar"):
                standard_prices = [12000, 15000, 18000, 20000, 25000]
                for price in standard_prices:
                    if not any(rp['harga'] == price for rp in st.session_state.rice_prices):
                        add_rice_price(price)
                st.success("✅ Harga beras standar berhasil ditambahkan!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Hapus Semua Harga", use_container_width=True):
                if len(st.session_state.rice_prices) > 0:
                    st.session_state.show_delete_all_rice_confirm = True
    
    else:
        st.info("🌾 Belum ada data harga beras. Silakan tambahkan harga beras pertama!")
        
        if st.button("🌾 Inisialisasi Harga Standar", type="primary"):
            standard_prices = [10000, 12000, 15000, 18000, 20000]
            for price in standard_prices:
                add_rice_price(price)
            st.success("✅ Harga beras standar berhasil ditambahkan!")
            st.rerun()
    
    # Show delete all confirmation
    if getattr(st.session_state, 'show_delete_all_rice_confirm', False):
        st.warning("⚠️ Apakah Anda yakin ingin menghapus semua data harga beras?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Ya, Hapus Semua Harga", type="primary"):
                st.session_state.rice_prices = []
                st.session_state.show_delete_all_rice_confirm = False
                st.success("✅ Semua data harga beras berhasil dihapus")
                st.rerun()
        with col2:
            if st.button("❌ Batal Hapus"):
                st.session_state.show_delete_all_rice_confirm = False
                st.rerun()

if __name__ == "__main__":
    main()
