import streamlit as st
from config.settings import CONFIG
from utils.utils import load_model
from utils.features import batch_analyze_files, derive_acd_standard

def main():
    # 页面配置
    st.set_page_config(
        page_title="Batch prediction of soil ACd",
        page_icon="📊",
        layout="wide"
    )
    st.title("📊 The batch analysis and prediction of ACd")
    st.divider()
    
    # 加载模型
    with st.spinner("🔧 loading ACd prediction model..."):
        try:
            model = load_model()
            st.success("✅ Successfully loading prediction model (XGBoost)")
        except Exception as e:
            st.error(f"❌ failing to load the model：{str(e)}")
            return
    
    # 批量文件上传与分析
    st.subheader("🔹 Step1: Batch upload of sample data")
    uploaded_files = st.file_uploader(
        "File format: CSV or XLSX",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        help=f"文件需包含列：{', '.join(CONFIG['FEATURE_COLS'] + [CONFIG['TARGET_COL']])}"
    )
    
    data_stats = None
    r2_log_scale = None
    
    if uploaded_files:
        st.divider()
        st.subheader("🔹 Step2: Analysis and prediction results of the batch data")
        data_stats, r2_log_scale = batch_analyze_files(uploaded_files, model)
    
if __name__ == "__main__":
    main()


#https://standard-derivation-acd-soil-for-gm-sc.streamlit.app/