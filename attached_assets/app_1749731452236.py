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

# Custom CSS for Indonesian currency formatting and styling
st.markdown("""
<style>
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
    }
    .metric-label {
        color: #6b7280;
        font-size: 0.875rem;
    }
    .success-button {
        background-color: #22c55e;
        color: white;
    }
    .warning-button {
        background-color: #f59e0b;
        color: white;
    }
    .info-button {
        background-color: #3b82f6;
        color: white;
    }
    .danger-button {
        background-color: #ef4444;
        color: white;
    }
</style>
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
    
    # Sidebar navigation
    st.sidebar.title("🕌 Menu Navigasi")
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
    st.title("Dashboard Pembayaran Zakat")
    
    # Calculate statistics
    total_payments = sum([p['total_bayar'] for p in st.session_state.zakat_payments])
    transaction_count = len(st.session_state.zakat_payments)
    last_update = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Total Pembayaran</div>
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
    st.subheader("Daftar Pembayaran Terbaru")
    
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
        
        # Rename columns
        column_renames = {
            'id': 'ID',
            'nama': 'Nama',
            'jumlah_jiwa': 'Jumlah Jiwa',
            'jenis_zakat': 'Jenis Zakat',
            'metode_pembayaran': 'Metode Pembayaran',
            'total_bayar': 'Total Bayar (Rp)',
            'nominal_dibayar': 'Nominal Dibayar (Rp)',
            'kembalian': 'Kembalian (Rp)',
            'tanggal_bayar': 'Tanggal Bayar'
        }
        
        display_columns = ['ID', 'Nama', 'Jenis Zakat', 'Total Bayar (Rp)', 'Tanggal Bayar']
        df_display = df_display.rename(columns=column_renames)
        
        # Show only selected columns
        available_display_cols = [col for col in display_columns if col in df_display.columns]
        if available_display_cols:
            st.dataframe(df_display[available_display_cols], use_container_width=True)
    else:
        st.info("Belum ada data pembayaran.")
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Tambah Pembayaran", type="primary", use_container_width=True):
            st.session_state.menu_override = "Tambah Pembayaran"
            st.rerun()
    
    with col2:
        if st.button("📊 History Pembayaran", use_container_width=True):
            st.session_state.menu_override = "Riwayat Pembayaran"
            st.rerun()
    
    with col3:
        if st.button("📋 Data Beras", use_container_width=True):
            st.session_state.menu_override = "Data Harga Beras"
            st.rerun()

def show_payment_form():
    """Display payment form"""
    st.title("Melakukan Pembayaran Zakat")
    
    with st.form("payment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama*", placeholder="Masukkan nama lengkap")
            jumlah_jiwa = st.number_input("Jumlah Jiwa", min_value=1, value=1, step=1)
            jenis_zakat = st.selectbox("Jenis Zakat*", ["Pilih Jenis Zakat"] + get_zakat_types())
            metode_pembayaran = st.selectbox("Metode Pembayaran*", ["Pilih Metode Pembayaran"] + get_payment_methods())
        
        with col2:
            total_bayar = st.number_input("Total Bayar (Rp)*", min_value=0.0, format="%.2f", step=1000.0)
            nominal_dibayar = st.number_input("Nominal Dibayar (Rp)*", min_value=0.0, format="%.2f", step=1000.0)
            
            # Calculate change automatically
            kembalian = max(0, nominal_dibayar - total_bayar) if nominal_dibayar > 0 and total_bayar > 0 else 0
            st.number_input("Kembalian (Rp)", value=kembalian, disabled=True, format="%.2f")
            
            tanggal_bayar = st.date_input("Tanggal Bayar*", value=datetime.now().date())
        
        # Form submission buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("💾 Simpan Pembayaran", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Kembali", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            if not nama.strip():
                errors.append("Nama harus diisi")
            if jenis_zakat == "Pilih Jenis Zakat":
                errors.append("Pilih jenis zakat")
            if metode_pembayaran == "Pilih Metode Pembayaran":
                errors.append("Pilih metode pembayaran")
            if total_bayar <= 0:
                errors.append("Total bayar harus lebih dari 0")
            if nominal_dibayar <= 0:
                errors.append("Nominal dibayar harus lebih dari 0")
            if nominal_dibayar < total_bayar:
                errors.append("Nominal dibayar tidak boleh kurang dari total bayar")
            
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
                st.success("✅ Pembayaran berhasil disimpan!")
                st.balloons()
                
                # Reset form by rerunning
                st.rerun()
        
        if cancel:
            st.session_state.menu_override = "Dashboard"
            st.rerun()

def show_payment_history():
    """Display payment history with CRUD operations"""
    st.title("Pembayaran Zakat")
    
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
                label="📊 Generate Excel",
                data=excel_data,
                file_name=f"pembayaran_zakat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📊 Generate Excel", disabled=True, use_container_width=True)
    
    with col3:
        if st.button("✏️ Edit", disabled=True, use_container_width=True):
            pass
    
    if not st.session_state.zakat_payments:
        st.info("Belum ada data pembayaran.")
        return
    
    # Create DataFrame for display
    df = pd.DataFrame(st.session_state.zakat_payments)
    
    # Display table with actions
    st.markdown("### Data Pembayaran")
    
    for i, payment in enumerate(st.session_state.zakat_payments):
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col_actions = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2])
            
            with col1:
                st.write(payment.get('id', i+1))
            with col2:
                st.write(payment.get('jumlah_jiwa', ''))
            with col3:
                st.write(payment.get('jenis_zakat', ''))
            with col4:
                st.write(payment.get('nama', ''))
            with col5:
                st.write(payment.get('metode_pembayaran', ''))
            with col6:
                st.write(format_currency(payment.get('total_bayar', 0)))
            with col7:
                st.write(format_currency(payment.get('nominal_dibayar', 0)))
            with col8:
                st.write(format_currency(payment.get('kembalian', 0)))
            
            with col_actions:
                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("✏️", key=f"edit_{payment.get('id', i)}", help="Edit"):
                        st.session_state.edit_payment_id = payment.get('id', i)
                        st.session_state.show_edit_form = True
                        st.rerun()
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_{payment.get('id', i)}", help="Delete"):
                        if st.session_state.get(f"confirm_delete_{payment.get('id', i)}", False):
                            delete_payment(payment.get('id', i))
                            st.success("Pembayaran berhasil dihapus!")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{payment.get('id', i)}"] = True
                            st.warning("Klik sekali lagi untuk mengkonfirmasi penghapusan!")
                            st.rerun()
    
    # Show edit form if needed
    if st.session_state.get('show_edit_form', False):
        show_edit_form()

def show_edit_form():
    """Show edit form for selected payment"""
    payment_id = st.session_state.get('edit_payment_id')
    payment = next((p for p in st.session_state.zakat_payments if p.get('id') == payment_id), None)
    
    if not payment:
        st.error("Pembayaran tidak ditemukan!")
        return
    
    st.markdown("### Edit Pembayaran")
    
    with st.form("edit_payment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama*", value=payment.get('nama', ''))
            jumlah_jiwa = st.number_input("Jumlah Jiwa", min_value=1, value=payment.get('jumlah_jiwa', 1), step=1)
            
            zakat_types = get_zakat_types()
            current_zakat = payment.get('jenis_zakat', '')
            zakat_index = zakat_types.index(current_zakat) if current_zakat in zakat_types else 0
            jenis_zakat = st.selectbox("Jenis Zakat*", zakat_types, index=zakat_index)
            
            payment_methods = get_payment_methods()
            current_method = payment.get('metode_pembayaran', '')
            method_index = payment_methods.index(current_method) if current_method in payment_methods else 0
            metode_pembayaran = st.selectbox("Metode Pembayaran*", payment_methods, index=method_index)
        
        with col2:
            total_bayar = st.number_input("Total Bayar (Rp)*", min_value=0.0, value=float(payment.get('total_bayar', 0)), format="%.2f", step=1000.0)
            nominal_dibayar = st.number_input("Nominal Dibayar (Rp)*", min_value=0.0, value=float(payment.get('nominal_dibayar', 0)), format="%.2f", step=1000.0)
            
            kembalian = max(0, nominal_dibayar - total_bayar) if nominal_dibayar > 0 and total_bayar > 0 else 0
            st.number_input("Kembalian (Rp)", value=kembalian, disabled=True, format="%.2f")
            
            try:
                current_date = datetime.strptime(payment.get('tanggal_bayar', ''), '%Y-%m-%d').date()
            except:
                current_date = datetime.now().date()
            tanggal_bayar = st.date_input("Tanggal Bayar*", value=current_date)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Update Pembayaran", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Batal", use_container_width=True)
        
        if submit:
            # Validation
            errors = []
            if not nama.strip():
                errors.append("Nama harus diisi")
            if total_bayar <= 0:
                errors.append("Total bayar harus lebih dari 0")
            if nominal_dibayar <= 0:
                errors.append("Nominal dibayar harus lebih dari 0")
            if nominal_dibayar < total_bayar:
                errors.append("Nominal dibayar tidak boleh kurang dari total bayar")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Update payment
                updated_data = {
                    'nama': nama.strip(),
                    'jumlah_jiwa': jumlah_jiwa,
                    'jenis_zakat': jenis_zakat,
                    'metode_pembayaran': metode_pembayaran,
                    'total_bayar': total_bayar,
                    'nominal_dibayar': nominal_dibayar,
                    'kembalian': kembalian,
                    'tanggal_bayar': tanggal_bayar.strftime("%Y-%m-%d")
                }
                
                update_payment(payment_id, updated_data)
                st.success("✅ Pembayaran berhasil diupdate!")
                
                # Clear edit state
                st.session_state.show_edit_form = False
                if 'edit_payment_id' in st.session_state:
                    del st.session_state.edit_payment_id
                st.rerun()
        
        if cancel:
            st.session_state.show_edit_form = False
            if 'edit_payment_id' in st.session_state:
                del st.session_state.edit_payment_id
            st.rerun()

def show_rice_prices():
    """Display rice price management"""
    st.title("Data Harga Beras")
    
    # Action buttons
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🔙 Kembali", use_container_width=True):
            st.session_state.menu_override = "Dashboard"
            st.rerun()
    
    with col2:
        if st.button("➕ Tambah Data", type="primary", use_container_width=True):
            st.session_state.show_add_rice_form = True
            st.rerun()
    
    # Display rice prices table
    if st.session_state.rice_prices:
        st.markdown("### Daftar Harga Beras")
        
        # Table header
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown("**ID**")
        with col2:
            st.markdown("**Harga**")
        with col3:
            st.markdown("**Aksi**")
        
        st.markdown("---")
        
        # Table rows
        for price_data in st.session_state.rice_prices:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.write(price_data['id'])
            
            with col2:
                st.write(format_currency(price_data['harga']))
            
            with col3:
                if st.button("🗑️", key=f"delete_rice_{price_data['id']}", help="Delete"):
                    if st.session_state.get(f"confirm_delete_rice_{price_data['id']}", False):
                        delete_rice_price(price_data['id'])
                        st.success("Data harga beras berhasil dihapus!")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_delete_rice_{price_data['id']}"] = True
                        st.warning("Klik sekali lagi untuk mengkonfirmasi!")
                        st.rerun()
    else:
        st.info("Belum ada data harga beras.")
    
    # Show add form if needed
    if st.session_state.get('show_add_rice_form', False):
        st.markdown("### Tambah Data Beras")
        
        with st.form("add_rice_form"):
            harga = st.number_input("Harga (Rp)*", min_value=0.0, format="%.2f", step=1000.0, placeholder="Masukkan harga")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("💾 Simpan", type="primary", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Batal", use_container_width=True)
            
            if submit:
                if harga <= 0:
                    st.error("Harga harus lebih dari 0")
                else:
                    add_rice_price(harga)
                    st.success("✅ Data harga beras berhasil ditambahkan!")
                    st.session_state.show_add_rice_form = False
                    st.rerun()
            
            if cancel:
                st.session_state.show_add_rice_form = False
                st.rerun()

# Handle menu override from dashboard buttons
if 'menu_override' in st.session_state:
    if st.session_state.menu_override == "Tambah Pembayaran":
        show_payment_form()
        del st.session_state.menu_override
    elif st.session_state.menu_override == "Riwayat Pembayaran":
        show_payment_history()
        del st.session_state.menu_override
    elif st.session_state.menu_override == "Data Harga Beras":
        show_rice_prices()
        del st.session_state.menu_override
    elif st.session_state.menu_override == "Dashboard":
        show_dashboard()
        del st.session_state.menu_override
else:
    # Run main application
    if __name__ == "__main__":
        main()
