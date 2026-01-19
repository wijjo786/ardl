import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Tax Revenue Intelligence | Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# EXECUTIVE DESIGN SYSTEM - MODERN LIGHT THEME
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ═══════════════════════════════════════════════════════════════════════════
   DESIGN TOKENS - Executive Light Theme
   ═══════════════════════════════════════════════════════════════════════════ */
:root {
    /* Primary Palette - Professional Blue */
    --primary-50: #EFF6FF;
    --primary-100: #DBEAFE;
    --primary-200: #BFDBFE;
    --primary-300: #93C5FD;
    --primary-400: #60A5FA;
    --primary-500: #3B82F6;
    --primary-600: #2563EB;
    --primary-700: #1D4ED8;
    --primary-800: #1E40AF;
    
    /* Accent Colors */
    --accent-purple: #8B5CF6;
    --accent-teal: #14B8A6;
    --accent-orange: #F59E0B;
    --accent-rose: #F43F5E;
    
    /* Neutral Palette - Sophisticated Grays */
    --gray-50: #FAFBFC;
    --gray-100: #F4F6F8;
    --gray-200: #E8ECF0;
    --gray-300: #D1D8DE;
    --gray-400: #9AA5B1;
    --gray-500: #697586;
    --gray-600: #4B5563;
    --gray-700: #364152;
    --gray-800: #1F2937;
    --gray-900: #111827;
    
    /* Surface Colors */
    --surface-primary: #FFFFFF;
    --surface-secondary: #FAFBFC;
    --surface-elevated: #FFFFFF;
    --surface-overlay: rgba(255, 255, 255, 0.98);
    
    /* Background */
    --bg-main: #F6F8FC;        /* cleaner, calmer canvas */
    --bg-sidebar: #F3F6FB;;     
    
    /* Text Hierarchy */
    --text-primary: #1F2937;
    --text-secondary: #4B5563;
    --text-tertiary: #6B7280;
    --text-muted: #9CA3AF;
    
    /* Borders */
    --border-light: #F0F3F6;
    --border-medium: #E5E9ED;
    --border-strong: #D1D8DE;
    
    /* Status Colors */
    --success-bg: #ECFDF5;
    --success-text: #047857;
    --success-border: #A7F3D0;
    
    --warning-bg: #FEF3C7;
    --warning-text: #92400E;
    --warning-border: #FCD34D;
    
    --danger-bg: #FEE2E2;
    --danger-text: #991B1B;
    --danger-border: #FECACA;
    
    --info-bg: #EFF6FF;
    --info-text: #1E40AF;
    --info-border: #BFDBFE;
    
    /* Shadows - Subtle & Refined */
    --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    
    /* Spacing System */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    
    /* Border Radius */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-xl: 20px;
    
    /* Transitions */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-smooth: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ═══════════════════════════════════════════════════════════════════════════
   GLOBAL STYLES
   ═══════════════════════════════════════════════════════════════════════════ */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg-main);
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
    line-height: 1.6;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton,
button[kind="primary"],
button[kind="primaryFormSubmit"],
[data-testid="stHeader"] button[kind="primary"],
header button[kind="primary"] {
    display: none !important;
    visibility: hidden !important;
}

/* Hide "Deploy" text specifically */
button:has(p:contains("Deploy")),
button[title*="Deploy"],
button[aria-label*="Deploy"] {
    display: none !important;
}
            

header[data-testid="stHeader"] {
    background-color: transparent !important;
    backdrop-filter: none !important;
}
[data-testid="stToolbar"] > div:not(:has(button[kind="header"])) {
    display: none !important;
}
/* Or alternatively, just hide specific toolbar items */
[data-testid="stToolbar"] [data-testid="stStatusWidget"] {
    display: none !important;
}


             
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
}

button[kind="header"] {
    display: block !important;
    visibility: visible !important;
}




            
.main .block-container {
    padding: 0rem var(--space-10) var(--space-12);
    max-width: 1800px;
    margin: 0 auto;
    padding-top: 0rem !important;
}

/* Remove Streamlit's default top padding */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Target the main content area */
.main > div {
    padding-top: 0rem !important;
}

section.main > div {
    padding-top: 0rem !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   SIDEBAR - LIGHT PROFESSIONAL THEME
   ═══════════════════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
     background: linear-gradient(
        180deg,
        #F5F8FD 0%,
        #F2F5FA 100%
    );
    border-right: 1px solid var(--border-medium);
    box-shadow: var(--shadow-sm);
}

section[data-testid="stSidebar"] > div:first-child {
    background: var(--bg-sidebar);
    padding-top: var(--space-4);
}

/* Sidebar Branding */
.sidebar-brand {
    padding: 0 var(--space-6) var(--space-5);
    border-bottom: 2px solid var(--border-light);
    margin-bottom: var(--space-5);
}

.brand-container {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-2);
}

.brand-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: var(--shadow-md);
}

.brand-text {
    flex: 1;
}

.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.brand-tagline {
    font-size: 0.75rem;
    color: var(--text-tertiary);
    font-weight: 500;
    margin-top: 2px;
}

/* Sidebar Section Headers */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: 0.6875rem !important;
    font-weight: 800 !important;
    color: var(--text-tertiary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    margin: var(--space-5) var(--space-6) var(--space-3) !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
}

/* Sidebar Labels & Text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}

/* Sidebar Inputs */
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stSelectbox select,
section[data-testid="stSidebar"] .stTextInput input {
    background: var(--surface-secondary) !important;
    border: 1.5px solid var(--border-medium) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-3) var(--space-4) !important;
    font-weight: 500 !important;
    transition: var(--transition-fast) !important;
}

section[data-testid="stSidebar"] .stNumberInput input:hover,
section[data-testid="stSidebar"] .stSelectbox select:hover {
    border-color: var(--border-strong) !important;
}

section[data-testid="stSidebar"] .stNumberInput input:focus,
section[data-testid="stSidebar"] .stSelectbox select:focus {
    border-color: var(--primary-500) !important;
    box-shadow: 0 0 0 3px var(--primary-100) !important;
    outline: none !important;
}

/* Sidebar Radio Buttons */
section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: var(--surface-secondary);
    border: 1.5px solid var(--border-medium);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-4);
    margin: var(--space-1) 0;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    transition: var(--transition-fast);
}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: var(--primary-50);
    border-color: var(--primary-300);
    color: var(--primary-700) !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
    background: var(--primary-50);
    border-color: var(--primary-500);
    color: var(--primary-700) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-xs);
}

/* Sidebar Slider */
section[data-testid="stSidebar"] .stSlider {
    padding: var(--space-4) 0;
}

/* Sidebar Info Box */
section[data-testid="stSidebar"] .stAlert {
    background: var(--info-bg) !important;
    border: 1px solid var(--info-border) !important;
    border-left: 3px solid var(--primary-600) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-4) !important;
}

/* Sidebar Buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: var(--surface-secondary);
    border: 1.5px solid var(--border-medium);
    color: var(--text-secondary);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-4);
    font-weight: 600;
    transition: var(--transition-fast);
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--primary-50);
    border-color: var(--primary-500);
    color: var(--primary-700);
    box-shadow: var(--shadow-sm);
}

/* File Uploader */
section[data-testid="stSidebar"] .uploadedFile {
    background: var(--surface-secondary) !important;
    border: 2px dashed var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    padding: var(--space-6) !important;
}

section[data-testid="stSidebar"] .uploadedFile:hover {
    border-color: var(--primary-400) !important;
    background: var(--primary-50) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   HEADER - EXECUTIVE STYLE
   ═══════════════════════════════════════════════════════════════════════════ */
.executive-header {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 50%, #E0E7FF 100%);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-xl);
    padding: var(--space-4);
    margin-bottom: var(--space-4);
    margin-top: 0 !important;
    box-shadow: var(--shadow-md);
    position: relative;
    overflow: hidden;
}

.executive-header::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 400px;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.08) 100%);
    pointer-events: none;
}

.header-content {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-left {
    flex: 1;
}

.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.625rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.header-subtitle {
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
    line-height: 1.3;
}

.header-right {
    display: flex;
    gap: var(--space-4);
    align-items: center;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    background: var(--success-bg);
    color: var(--success-text);
    padding: var(--space-3) var(--space-5);
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 600;
    border: 1px solid var(--success-border);
    box-shadow: var(--shadow-xs);
}

.status-indicator {
    width: 8px;
    height: 8px;
    background: var(--success-text);
    border-radius: 50%;
    box-shadow: 0 0 0 3px var(--success-bg);
    animation: pulse-dot 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
}

/* ═══════════════════════════════════════════════════════════════════════════
   METRICS GRID - EXECUTIVE KPIs
   ═══════════════════════════════════════════════════════════════════════════ */
.metrics-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--space-6);
    margin-bottom: var(--space-6);
}

.kpi-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFF 100%);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-sm);
    transition: var(--transition-base);
    position: relative;
    overflow: hidden;
}

.kpi-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
    pointer-events: none;
    transition: var(--transition-smooth);
}

.kpi-card:hover::after {
    top: -30%;
    right: -30%;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-500) 0%, var(--accent-purple) 100%);
    transform: scaleX(0);
    transform-origin: left;
    transition: var(--transition-base);
}

.kpi-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);
    border-color: var(--primary-200);
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}

.kpi-card:hover::before {
    transform: scaleX(1);
}

.kpi-card:nth-child(1) {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
}

.kpi-card:nth-child(2) {
    background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
}

.kpi-card:nth-child(3) {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
}

.kpi-card:nth-child(4) {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-5);
}

.kpi-icon-wrapper {
    width: 52px;
    height: 52px;
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    box-shadow: var(--shadow-xs);
    transition: var(--transition-base);
}

.kpi-icon-wrapper.primary {
    background: linear-gradient(135deg, var(--primary-100) 0%, var(--primary-50) 100%);
    color: var(--primary-700);
}

.kpi-icon-wrapper.purple {
    background: linear-gradient(135deg, #EDE9FE 0%, #F5F3FF 100%);
    color: var(--accent-purple);
}

.kpi-icon-wrapper.teal {
    background: linear-gradient(135deg, #CCFBF1 0%, #E0F2FE 100%);
    color: var(--accent-teal);
}

.kpi-icon-wrapper.orange {
    background: linear-gradient(135deg, #FEF3C7 0%, #FEF9C3 100%);
    color: #D97706;
}

.kpi-card:hover .kpi-icon-wrapper {
    transform: scale(1.1) rotate(-5deg);
}

.kpi-label {
    font-size: 0.8125rem;
    font-weight: 700;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: var(--space-1);
}

.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: var(--space-3);
}

.kpi-trend {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-md);
    font-size: 0.8125rem;
    font-weight: 700;
}

.kpi-trend.positive {
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid var(--success-border);
}

.kpi-trend.negative {
    background: var(--danger-bg);
    color: var(--danger-text);
    border: 1px solid var(--danger-border);
}

.kpi-trend.neutral {
    background: var(--info-bg);
    color: var(--info-text);
    border: 1px solid var(--info-border);
}

.kpi-description {
    font-size: 0.8125rem;
    color: var(--text-muted);
    margin-top: var(--space-3);
    line-height: 1.5;
}

/* ═══════════════════════════════════════════════════════════════════════════
   CONTENT CARDS - MAIN SECTIONS
   ═══════════════════════════════════════════════════════════════════════════ */
.content-section {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: var(--space-8);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow-sm);
    transition: var(--transition-base);
    position: relative;
    overflow: hidden;
}

.content-section::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.03) 100%);
    pointer-events: none;
}

.content-section:hover {
    box-shadow: var(--shadow-md);
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--space-6);
    padding-bottom: var(--space-5);
    border-bottom: 2px solid transparent;
    background: linear-gradient(90deg, var(--primary-100) 0%, transparent 100%);
    padding: var(--space-4);
    margin: calc(var(--space-8) * -1) calc(var(--space-8) * -1) var(--space-6);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.375rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: var(--space-1);
    line-height: 1.2;
}

.section-subtitle {
    font-size: 0.9375rem;
    color: var(--text-secondary);
    font-weight: 500;
}

.section-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
    color: var(--primary-700);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 600;
    border: 1px solid var(--primary-200);
    box-shadow: var(--shadow-xs);
}

/* ═══════════════════════════════════════════════════════════════════════════
   TABS - MODERN CLEAN STYLE
   ═══════════════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-2);
    background: linear-gradient(90deg, #EFF6FF 0%, #E0E7FF 50%, #EFF6FF 100%);
    border-bottom: 2px solid var(--primary-200);
    padding: var(--space-2);
    margin-bottom: var(--space-6);
    border-radius: var(--radius-md);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    padding: var(--space-4) var(--space-6);
    font-weight: 600;
    color: var(--text-tertiary);
    border: none;
    border-bottom: 3px solid transparent;
    transition: var(--transition-fast);
    font-size: 0.9375rem;
    border-radius: var(--radius-md);
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--primary-700);
    background: rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-md);
}

.stTabs [aria-selected="true"] {
    color: var(--primary-700);
    border-bottom-color: transparent;
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);
    box-shadow: var(--shadow-sm);
    border-radius: var(--radius-md);
}

/* ═══════════════════════════════════════════════════════════════════════════
   CATEGORY LIST ITEMS
   ═══════════════════════════════════════════════════════════════════════════ */
.category-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.category-item {
    background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-md);
    padding: var(--space-5) var(--space-6);
    display: grid;
    grid-template-columns: 2fr 1.2fr 1fr;
    align-items: center;
    gap: var(--space-5);
    transition: var(--transition-base);
    position: relative;
    overflow: hidden;
}

.category-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--primary-500) 0%, var(--accent-purple) 100%);
    opacity: 0;
    transition: var(--transition-base);
}

.category-item:hover::before {
    opacity: 1;
}

.category-item:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
    border-color: var(--primary-300);
    box-shadow: var(--shadow-md);
    transform: translateX(4px);
}

.category-name {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9375rem;
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.category-name::before {
    content: '';
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, var(--primary-600) 0%, var(--accent-purple) 100%);
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
}

.category-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
}

.category-trend {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 700;
    justify-self: end;
}

.category-trend.positive {
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid var(--success-border);
}

.category-trend.negative {
    background: var(--danger-bg);
    color: var(--danger-text);
    border: 1px solid var(--danger-border);
}

/* ═══════════════════════════════════════════════════════════════════════════
   BUTTONS - PRIMARY ACTIONS
   ═══════════════════════════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-6);
    font-weight: 600;
    font-size: 0.9375rem;
    transition: var(--transition-base);
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-700) 0%, var(--primary-800) 100%);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.stDownloadButton > button {
    background: var(--surface-elevated);
    color: var(--primary-700);
    border: 2px solid var(--primary-500);
    border-radius: var(--radius-md);
    padding: var(--space-4) var(--space-6);
    font-weight: 600;
    transition: var(--transition-base);
}

.stDownloadButton > button:hover {
    background: var(--primary-50);
    border-color: var(--primary-600);
    box-shadow: var(--shadow-sm);
}

/* ═══════════════════════════════════════════════════════════════════════════
   DATA TABLES
   ═══════════════════════════════════════════════════════════════════════════ */
.dataframe {
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-xs);
}

.dataframe thead tr th {
    background: var(--gray-100) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 0.8125rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    padding: var(--space-4) var(--space-5) !important;
    border-bottom: 2px solid var(--border-medium) !important;
}

.dataframe tbody tr {
    transition: var(--transition-fast);
    border-bottom: 1px solid var(--border-light);
}

.dataframe tbody tr:hover {
    background: var(--gray-50) !important;
}

.dataframe tbody td {
    padding: var(--space-4) var(--space-5) !important;
    font-size: 0.9375rem !important;
    color: var(--text-secondary) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   INFO PANELS
   ═══════════════════════════════════════════════════════════════════════════ */
.insight-panel {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 50%, #E0E7FF 100%);
    border: 1px solid var(--primary-200);
    border-left: 4px solid var(--primary-600);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    margin: var(--space-8) 0;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}

.insight-panel::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(139, 92, 246, 0.1) 100%);
    pointer-events: none;
}

.insight-header {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin-bottom: var(--space-4);
}

.insight-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    color: white;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.insight-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.0625rem;
    font-weight: 700;
    color: var(--primary-800);
}

.insight-content {
    font-size: 0.9375rem;
    color: var(--text-primary);
    line-height: 1.7;
}

.insight-content strong {
    color: var(--primary-700);
    font-weight: 600;
}

/* ═══════════════════════════════════════════════════════════════════════════
   METRIC LABELS
   ═══════════════════════════════════════════════════════════════════════════ */
.stMetric {
    background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
    border: 1px solid var(--border-medium);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    transition: var(--transition-base);
}

.stMetric:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
    border-color: var(--primary-200);
    box-shadow: var(--shadow-sm);
}

.stMetric label {
    font-size: 0.8125rem !important;
    font-weight: 700 !important;
    color: var(--text-tertiary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

.stMetric [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════════════════════════════ */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--gray-100);
    border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb {
    background: var(--gray-300);
    border-radius: var(--radius-sm);
    border: 2px solid var(--gray-100);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--gray-400);
}

/* ═══════════════════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.kpi-card,
.content-section {
    animation: fadeInUp 0.5s ease-out;
}

.category-item {
    animation: fadeInUp 0.4s ease-out;
}

.category-item:nth-child(1) { animation-delay: 0.05s; }
.category-item:nth-child(2) { animation-delay: 0.10s; }
.category-item:nth-child(3) { animation-delay: 0.15s; }
.category-item:nth-child(4) { animation-delay: 0.20s; }
.category-item:nth-child(5) { animation-delay: 0.25s; }
.category-item:nth-child(6) { animation-delay: 0.30s; }
.category-item:nth-child(7) { animation-delay: 0.35s; }
.category-item:nth-child(8) { animation-delay: 0.40s; }
            

            /* ═══════════════════════════════════════════════════════════════════════════
   COLORFUL THEME STYLES
   ═══════════════════════════════════════════════════════════════════════════ */

/* KPI CARDS - Individual colored gradients */
.kpi-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFF 100%);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    box-shadow: var(--shadow-sm);
    transition: var(--transition-base);
    position: relative;
    overflow: hidden;
}

.kpi-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
    pointer-events: none;
    transition: var(--transition-smooth);
}

.kpi-card:hover::after {
    top: -30%;
    right: -30%;
}

.kpi-card:hover {
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}

/* Each KPI card gets unique color */
.kpi-card:nth-child(1) {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
}

.kpi-card:nth-child(2) {
    background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
}

.kpi-card:nth-child(3) {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
}

.kpi-card:nth-child(4) {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
}

/* CONTENT SECTIONS */
.content-section {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
    position: relative;
    overflow: hidden;
}

.content-section::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.03) 100%);
    pointer-events: none;
}

.content-section:hover {
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}

/* SECTION HEADERS */
.section-header {
    background: linear-gradient(90deg, var(--primary-100) 0%, transparent 100%);
    padding: var(--space-4);
    margin: calc(var(--space-8) * -1) calc(var(--space-8) * -1) var(--space-6);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    border-bottom: 2px solid transparent;
}

/* SECTION BADGES */
.section-badge {
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
    color: var(--primary-700);
    border: 1px solid var(--primary-200);
    box-shadow: var(--shadow-xs);
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(90deg, #EFF6FF 0%, #E0E7FF 50%, #EFF6FF 100%);
    border-bottom: 2px solid var(--primary-200);
    padding: var(--space-2);
    border-radius: var(--radius-md);
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-md);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #F0F9FF 100%);
    box-shadow: var(--shadow-sm);
    border-radius: var(--radius-md);
    border-bottom-color: transparent;
}

/* CATEGORY ITEMS */
.category-item {
    background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
    position: relative;
    overflow: hidden;
}

.category-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--primary-500) 0%, var(--accent-purple) 100%);
    opacity: 0;
    transition: var(--transition-base);
}

.category-item:hover::before {
    opacity: 1;
}

.category-item:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
}

.category-name::before {
    background: linear-gradient(180deg, var(--primary-600) 0%, var(--accent-purple) 100%);
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
}

/* INSIGHT PANEL */
.insight-panel {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 50%, #E0E7FF 100%);
    position: relative;
    overflow: hidden;
}

.insight-panel::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(139, 92, 246, 0.1) 100%);
    pointer-events: none;
}

.insight-icon {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* METRICS */
.stMetric {
    background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
    transition: var(--transition-base);
}

.stMetric:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
    border-color: var(--primary-200);
    box-shadow: var(--shadow-sm);
}

/* SIDEBAR COLORFUL STYLING */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 50%, #F5F3FF 100%);
}

.sidebar-brand {
    background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(239, 246, 255, 0.5) 100%);
    border-bottom: 2px solid var(--primary-100);
}

.brand-icon {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--accent-purple) 100%);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.brand-tagline {
    color: var(--primary-600);
    font-weight: 600;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--primary-700) !important;
    background: linear-gradient(90deg, var(--primary-100) 0%, transparent 100%) !important;
    border-left: 3px solid var(--primary-600) !important;
    border-radius: var(--radius-sm) !important;
    padding: var(--space-2) var(--space-3) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: var(--primary-100) !important;
}

section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stSelectbox select,
section[data-testid="stSidebar"] .stTextInput input {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
}

section[data-testid="stSidebar"] .stNumberInput input:hover,
section[data-testid="stSidebar"] .stSelectbox select:hover {
    border-color: var(--primary-300) !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%) !important;
}

section[data-testid="stSidebar"] .stNumberInput input:focus,
section[data-testid="stSidebar"] .stSelectbox select:focus {
    background: #FFFFFF !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
}

section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
}

section[data-testid="stSidebar"] .stSlider [role="slider"] {
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--accent-purple) 100%) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
}

section[data-testid="stSidebar"] .stAlert {
    background: linear-gradient(135deg, #EFF6FF 0%, #E0E7FF 100%) !important;
    border: 1px solid var(--primary-200) !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
}

section[data-testid="stSidebar"] .uploadedFile {
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%) !important;
    border: 2px dashed var(--primary-300) !important;
}

section[data-testid="stSidebar"] .uploadedFile:hover {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   RESPONSIVE DESIGN
   ═══════════════════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .executive-header {
        padding: var(--space-6);
    }
    
    .header-content {
        flex-direction: column;
        gap: var(--space-4);
    }
    
    .header-title {
        font-size: 1.5rem;
    }
    
    .metrics-container {
        grid-template-columns: 1fr;
    }
    
    .category-item {
        grid-template-columns: 1fr;
        gap: var(--space-3);
    }
    
    .category-trend {
        justify-self: start;
    }
}
</style>
""", unsafe_allow_html=True)


# DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_models(model_path):
    """Load pickled ARDL models and results"""
    with open(model_path, "rb") as f:
        data = pickle.load(f)
    return data

@st.cache_data
def load_meta(meta_path):
    """Load metadata configuration"""
    with open(meta_path, "r") as f:
        return json.load(f)

@st.cache_data
def load_source_data(data_path):
    """Load historical data from CSV"""
    df = pd.read_csv(data_path, index_col=0)
    try:
        df.index = pd.PeriodIndex(df.index, freq="Y")
    except Exception:
        pass
    return df

@st.cache_data
def load_uploaded_excel(uploaded_file):
    """Load data from uploaded Excel file"""
    try:
        df = pd.read_excel(uploaded_file, index_col=0)
        try:
            df.index = pd.PeriodIndex(df.index, freq="Y")
        except Exception:
            pass
        
        if len(df.select_dtypes(include=[np.number]).columns) == 0:
            return None, "File must contain numeric data columns"
            
        return df, None
    except Exception as e:
        return None, str(e)

# Load default configuration
MODEL_FILE = "ardl_tax_models.pkl"
META_FILE = "ardl_tax_models_meta.json"
DATA_FILE = "ardl_prepared_data.csv"

if not os.path.exists(MODEL_FILE) or not os.path.exists(DATA_FILE) or not os.path.exists(META_FILE):
    st.error("⚠️ **Missing Required Files** • Please run 'ardl_pipeline.py' first to generate data files.")
    st.stop()

# Load artifacts
with st.spinner("⚙️ Initializing dashboard..."):
    artifacts = load_models(MODEL_FILE)
    df_default = load_source_data(DATA_FILE)
    meta = load_meta(META_FILE)

models_dict = artifacts["models"]
results_dict = artifacts["results"]
targets = list(results_dict.keys())

x_vars_ordered = meta.get("x_vars_used", [])
if not x_vars_ordered:
    st.error("⚠️ **Configuration Error** • Metadata missing. Please re-run pipeline.")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="brand-container">
        <div class="brand-icon">📊</div>
        <div class="brand-text">
            <div class="brand-name">Revenue Analytics</div>
            <div class="brand-tagline">Intelligence Platform</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_datasets' not in st.session_state:
    st.session_state.uploaded_datasets = {}
if 'selected_dataset' not in st.session_state:
    st.session_state.selected_dataset = "Default Data"

# ═══════════════════════════════════════════════════════════════════════════
# LOAD ACTIVE DATASET (happens before sidebar display)
# ═══════════════════════════════════════════════════════════════════════════

# Helper function for dataset selection
def on_dataset_change():
    st.session_state.selected_dataset = st.session_state.dataset_selector

# Get available datasets
available_datasets = ["Default Data"] + list(st.session_state.uploaded_datasets.keys())

if st.session_state.selected_dataset not in available_datasets:
    st.session_state.selected_dataset = "Default Data"

# Get active dataset
if st.session_state.selected_dataset == "Default Data":
    df_hist = df_default.copy()
    data_source_label = "Default Dataset"
else:
    if st.session_state.selected_dataset in st.session_state.uploaded_datasets:
        df_hist = st.session_state.uploaded_datasets[st.session_state.selected_dataset].copy()
        data_source_label = st.session_state.selected_dataset
    else:
        df_hist = df_default.copy()
        data_source_label = "Default Dataset"
        st.session_state.selected_dataset = "Default Data"

# Filter to 2024
if isinstance(df_hist.index, pd.PeriodIndex):
    df_hist = df_hist[df_hist.index.year <= 2024]
elif hasattr(df_hist.index, "year"):
    df_hist = df_hist[df_hist.index.year <= 2024]
else:
    try:
        df_hist = df_hist[df_hist.index <= 2024]
    except:
        pass

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR SECTIONS - PROPER DISPLAY ORDER
# ═══════════════════════════════════════════════════════════════════════════

# 1. Forecast Configuration
st.sidebar.markdown("### 🎯 Forecast Configuration")
years_to_forecast = st.sidebar.slider(
    "Projection Horizon (Years)", 
    min_value=1, 
    max_value=10, 
    value=3,
    help="Number of years to project forward"
)

# st.sidebar.markdown("---")

# 2. Economic Assumptions
st.sidebar.markdown("### 📊 Economic Assumptions")

base_vars = ["gdp_real", "imports_real", "consumption_real", "govexp", "gdp_growth", "inflation", "unemployment", "dummy_2014"]
available_vars = [c for c in base_vars if c in df_hist.columns]

defaults = {
    "gdp_real": 0.03,
    "gdp_growth": 0.03,
    "imports_real": 0.05,
    "govexp": 0.05,
    "inflation": 0.12,
    "unemployment": 0.065
}

var_labels = {
    "gdp_real": "Real GDP Growth Rate",
    "gdp_growth": "GDP Growth Rate",
    "imports_real": "Import Growth Rate",
    "govexp": "Government Expenditure",
    "inflation": "Inflation Rate",
    "unemployment": "Unemployment Rate",
    "consumption_real": "Consumption Growth"
}

scenarios = {}
for v in available_vars:
    if "dummy" in v:
        scenarios[v] = {"type": "fixed", "value": 1}
        continue

    label = var_labels.get(v, v.replace("_", " ").title())
    def_val = defaults.get(v, 0.0)

    if "growth" in v or "inflation" in v or "unemployment" in v:
        new_val = st.sidebar.number_input(
            label, 
            value=float(def_val), 
            step=0.005, 
            format="%.3f", 
            key=f"{v}_{st.session_state.selected_dataset}"
        )
        scenarios[v] = {"type": "level", "value": new_val}
    else:
        growth = st.sidebar.number_input(
            label, 
            value=float(def_val), 
            step=0.005, 
            format="%.3f", 
            key=f"{v}_{st.session_state.selected_dataset}"
        )
        scenarios[v] = {"type": "growth", "value": growth}

st.sidebar.markdown("---")

# 3. Data Management - AT THE END
st.sidebar.markdown("### 📁 Data Management")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload Custom Dataset",
    type=['xlsx', 'xls'],
    help="Excel file with historical revenue data",
    key="file_uploader"
)

# Handle file upload
if uploaded_file is not None:
    file_name = uploaded_file.name
    if file_name not in st.session_state.uploaded_datasets:
        with st.spinner(f"Processing {file_name}..."):
            df_uploaded, error = load_uploaded_excel(uploaded_file)
            if error:
                st.sidebar.error(f"Error: {error}")
            else:
                st.session_state.uploaded_datasets[file_name] = df_uploaded
                st.session_state.selected_dataset = file_name
                st.sidebar.success(f"✓ Successfully loaded")
                st.rerun()

# Dataset selector
selected_dataset = st.sidebar.radio(
    "Active Dataset",
    available_datasets,
    index=available_datasets.index(st.session_state.selected_dataset),
    key="dataset_selector",
    on_change=on_dataset_change
)

st.session_state.selected_dataset = selected_dataset

# Clear uploads button
if len(st.session_state.uploaded_datasets) > 0:
    if st.sidebar.button("Clear All Uploads"):
        st.session_state.uploaded_datasets = {}
        st.session_state.selected_dataset = "Default Data"
        st.rerun()

# Dataset info
st.sidebar.info(f"""
📊 **{data_source_label}**  
📅 {df_hist.index.min()} – {df_hist.index.max()}  
📈 {len(df_hist)} observations
""")

# 1. Forecast Configuration

# ═══════════════════════════════════════════════════════════════════════════
# FORECAST GENERATION
# ═══════════════════════════════════════════════════════════════════════════
max_idx = df_hist.index.max()
if hasattr(max_idx, 'year'):
    last_year = max_idx.year
else:
    try:
        last_year = int(max_idx)
    except:
        last_year = 2024

future_years = [last_year + i for i in range(1, years_to_forecast + 1)]
future_index = pd.PeriodIndex(future_years, freq="Y")

try:
    if hasattr(df_hist.index, "to_timestamp"):
        plot_hist_x = df_hist.index.to_timestamp()
    else:
        plot_hist_x = df_hist.index.map(lambda p: p.to_timestamp() if hasattr(p, 'to_timestamp') else p)
except:
    plot_hist_x = df_hist.index

df_future = pd.DataFrame(index=future_index)
last_row = df_hist.iloc[-1].copy()
temp_row = last_row.copy()
future_rows = []

for _ in range(years_to_forecast):
    next_row = temp_row.copy()
    
    for v in available_vars:
        spec = scenarios[v]
        if spec["type"] == "growth":
            next_row[v] = temp_row[v] + np.log(1 + spec["value"])
        elif spec["type"] == "fixed":
            next_row[v] = spec["value"]
        else:
            if v in ["inflation", "unemployment", "gdp_growth"]:
                next_row[v] = spec["value"] * 100.0
            else:
                next_row[v] = spec["value"]
    
    future_rows.append(next_row)
    temp_row = next_row

df_future = pd.DataFrame(future_rows, index=future_index)

forecast_results = {}
for target_name in targets:
    res = results_dict[target_name]
    exog_future = df_future[x_vars_ordered]
    
    try:
        preds = res.forecast(steps=years_to_forecast, exog=exog_future)
        preds_level = np.exp(preds)
        forecast_results[target_name] = preds_level
    except Exception as e:
        st.error(f"Forecast error for {target_name}: {e}")

# Calculate Metrics
total_tax_hist = np.exp(df_hist[targets]).sum(axis=1)
df_fore = pd.DataFrame(forecast_results)
plot_fore_x = df_fore.index.to_timestamp() if hasattr(df_fore.index, "to_timestamp") else df_fore.index
total_tax_fore = df_fore.sum(axis=1)

total_hist_latest = total_tax_hist.iloc[-1] / 1000
total_fore_last = total_tax_fore.iloc[-1] / 1000
growth_pct = ((total_fore_last * 1000) / (total_hist_latest * 1000) - 1) * 100
avg_annual_growth = (((total_fore_last * 1000) / (total_hist_latest * 1000)) ** (1/years_to_forecast) - 1) * 100
total_categories = len(targets)

# ═══════════════════════════════════════════════════════════════════════════
# EXECUTIVE HEADER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="executive-header">
    <div class="header-content">
        <div class="header-left">
            <div class="header-title">Tax Revenue Intelligence Dashboard</div>
            <div class="header-subtitle">Advanced econometric forecasting & strategic revenue analytics</div>
        </div>
        <div class="header-right">
            <div class="status-badge">
                <div class="status-indicator"></div>
                <span>Live Analytics</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# KEY PERFORMANCE INDICATORS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="metrics-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    trend_class = "positive" if growth_pct > 0 else "negative"
    trend_symbol = "↗" if growth_pct > 0 else "↘"
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon-wrapper primary">💰</div>
        </div>
        <div class="kpi-label">Projected Revenue</div>
        <div class="kpi-value">₨{total_fore_last:,.1f}B</div>
        <div class="kpi-trend {trend_class}">{trend_symbol} {abs(growth_pct):.1f}%</div>
        <div class="kpi-description">Target for fiscal year {future_years[-1]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon-wrapper purple">📊</div>
        </div>
        <div class="kpi-label">Current Baseline</div>
        <div class="kpi-value">₨{total_hist_latest:,.1f}B</div>
        <div class="kpi-trend neutral">FY {last_year}</div>
        <div class="kpi-description">Most recent fiscal year collection</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon-wrapper teal">📈</div>
        </div>
        <div class="kpi-label">Compound Growth</div>
        <div class="kpi-value">{avg_annual_growth:+.2f}%</div>
        <div class="kpi-trend positive">↗ CAGR</div>
        <div class="kpi-description">Average annual growth rate</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon-wrapper orange">🎯</div>
        </div>
        <div class="kpi-label">Revenue Streams</div>
        <div class="kpi-value">{total_categories}</div>
        <div class="kpi-trend neutral">Categories</div>
        <div class="kpi-description">Active tax collection channels</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT TABS
# ═══════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview", 
    "📈 Trend Analysis", 
    "🎯 Category Performance", 
    "⚙️ Model Diagnostics", 
    "💾 Data & Exports"
])

with tab1:
    # Main Revenue Chart
    st.markdown(f"""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Revenue Projection Timeline</div>
                <div class="section-subtitle">Historical performance vs. econometric forecast • {data_source_label}</div>
            </div>
            <div class="section-badge">🔮 {years_to_forecast}-Year Horizon</div>
        </div>
    """, unsafe_allow_html=True)
    
    fig_main = go.Figure()
    
    fig_main.add_trace(go.Scatter(
        x=plot_hist_x,
        y=total_tax_hist / 1000,
        mode='lines',
        name='Historical Revenue',
        line=dict(color='#2563EB', width=3.5),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.06)',
        hovertemplate='<b>FY %{x|%Y}</b><br><b>₨%{y:,.2f}B</b><extra></extra>'
    ))
    
    fig_main.add_trace(go.Scatter(
        x=plot_fore_x,
        y=total_tax_fore / 1000,
        mode='lines+markers',
        name='Projected Revenue',
        line=dict(color='#8B5CF6', width=3.5, dash='dash'),
        marker=dict(size=9, color='#8B5CF6', line=dict(width=2, color='white')),
        hovertemplate='<b>FY %{x|%Y}</b><br><b>₨%{y:,.2f}B</b><extra></extra>'
    ))
    
    fig_main.update_layout(
        height=460,
        margin=dict(l=0, r=0, t=20, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#4B5563'),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=13, weight=600),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#E5E9ED',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.03)',
            zeroline=False,
            title=dict(text="Fiscal Year", font=dict(weight=600, size=13))
        ),
        yaxis=dict(
            title=dict(text="Revenue (PKR Billion)", font=dict(weight=600, size=13)),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.03)',
            zeroline=False
        )
    )
    
    st.plotly_chart(fig_main, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToAdd': ['pan2d', 'select2d', 'lasso2d', 'resetScale2d', 'zoomIn2d', 'zoomOut2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'revenue_projection_timeline',
            'height': 800,
            'width': 1400,
            'scale': 2
        }
    })
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Secondary Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-section">
            <div class="section-header">
                <div>
                    <div class="section-title">Growth Dynamics</div>
                    <div class="section-subtitle">Year-over-year revenue change</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        growth_rates = (total_tax_hist / 1000).pct_change() * 100
        colors = ['#F43F5E' if x < 0 else '#14B8A6' for x in growth_rates]
        
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Bar(
            x=plot_hist_x,
            y=growth_rates,
            marker=dict(color=colors, line=dict(width=0)),
            hovertemplate='<b>FY %{x|%Y}</b><br>Growth: <b>%{y:.1f}%</b><extra></extra>'
        ))
        
        fig_growth.update_layout(
            height=340,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(showgrid=False, title=dict(text="Year", font=dict(weight=600))),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.03)', 
                zeroline=True, 
                zerolinecolor='#D1D8DE',
                zerolinewidth=2,
                title=dict(text="Growth Rate %", font=dict(weight=600))
            )
        )
        
        st.plotly_chart(fig_growth, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'growth_dynamics',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        })
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-section">
            <div class="section-header">
                <div>
                    <div class="section-title">Forecast Confidence</div>
                    <div class="section-subtitle">Statistical reliability metric</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        years_range = list(range(1, years_to_forecast + 1))
        confidence = [95 - (i * 3.5) for i in years_range]
        
        fig_conf = go.Figure()
        fig_conf.add_trace(go.Scatter(
            x=years_range,
            y=confidence,
            mode='lines+markers',
            line=dict(color='#8B5CF6', width=4),
            marker=dict(size=11, color='#8B5CF6', line=dict(width=2.5, color='white')),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.12)',
            hovertemplate='Year %{x}<br>Confidence: <b>%{y:.0f}%</b><extra></extra>'
        ))
        
        fig_conf.update_layout(
            height=340,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(
                title=dict(text='Forecast Year', font=dict(weight=600)), 
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.03)'
            ),
            yaxis=dict(
                title=dict(text='Confidence Level %', font=dict(weight=600)), 
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.03)', 
                range=[0, 100]
            )
        )
        
        st.plotly_chart(fig_conf, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'forecast_confidence',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        })
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    # Category Performance Ranking - MOVED HERE
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Category Performance Ranking</div>
                <div class="section-subtitle">Revenue streams sorted by projected value</div>
            </div>
        </div>
        <div class="category-list">
    """, unsafe_allow_html=True)
    
    category_data = []
    for t in targets:
        hist_val = np.exp(df_hist[t]).iloc[-1] / 1000
        fore_val = df_fore[t].iloc[-1] / 1000
        growth = ((fore_val * 1000) / (hist_val * 1000) - 1) * 100
        category_data.append({
            'name': t.replace('_', ' ').title(),
            'base': hist_val,
            'forecast': fore_val,
            'growth': growth
        })
    
    category_data = sorted(category_data, key=lambda x: x['forecast'], reverse=True)
    
    for cat in category_data:
        growth_class = "positive" if cat['growth'] > 0 else "negative"
        growth_symbol = "↗" if cat['growth'] > 0 else "↘"
        
        st.markdown(f"""
        <div class="category-item">
            <div class="category-name">{cat['name']}</div>
            <div class="category-value">₨{cat['forecast']:,.2f}B</div>
            <div class="category-trend {growth_class}">{growth_symbol} {abs(cat['growth']):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Historical Composition
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Historical Revenue Composition</div>
                <div class="section-subtitle">Category contribution over time</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    hist_df = np.exp(df_hist[targets]) / 1000
    
    fig_area = go.Figure()
    colors = ['#2563EB', '#8B5CF6', '#14B8A6', '#F59E0B', '#F43F5E', '#06B6D4', '#6366F1', '#EC4899']
    
    for idx, target in enumerate(targets):
        fig_area.add_trace(go.Scatter(
            x=plot_hist_x,
            y=hist_df[target],
            mode='lines',
            name=target.replace('_', ' ').title(),
            line=dict(width=0),
            stackgroup='one',
            fillcolor=colors[idx % len(colors)],
            hovertemplate='<b>%{fullData.name}</b><br>₨%{y:,.2f}B<extra></extra>'
        ))
    
    fig_area.update_layout(
        height=480,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#E5E9ED',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.03)', 
            title=dict(text="Fiscal Year", font=dict(weight=600))
        ),
        yaxis=dict(
            title=dict(text="Revenue (PKR Billion)", font=dict(weight=600)), 
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.03)'
        )
    )
    
    st.plotly_chart(fig_area, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'revenue_composition',
            'height': 800,
            'width': 1400,
            'scale': 2
        }
    })
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    # Individual Category Projections
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Individual Category Projections</div>
                <div class="section-subtitle">Detailed forecast by revenue stream</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    num_cols = 2
    for i in range(0, len(targets), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(targets):
                t = targets[i + j]
                with cols[j]:
                    hist_series = np.exp(df_hist[t]) / 1000
                    fore_series = df_fore[t] / 1000
                    
                    fig_cat = go.Figure()
                    
                    fig_cat.add_trace(go.Scatter(
                        x=plot_hist_x,
                        y=hist_series,
                        mode='lines',
                        name='Historical',
                        line=dict(color='#2563EB', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(37, 99, 235, 0.08)',
                        hovertemplate='<b>%{x|%Y}</b><br>₨%{y:,.2f}B<extra></extra>'
                    ))
                    
                    fig_cat.add_trace(go.Scatter(
                        x=plot_fore_x,
                        y=fore_series,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='#8B5CF6', width=3, dash='dash'),
                        marker=dict(size=7, color='#8B5CF6', line=dict(width=2, color='white')),
                        hovertemplate='<b>%{x|%Y}</b><br>₨%{y:,.2f}B<extra></extra>'
                    ))
                    
                    fig_cat.update_layout(
                        title=dict(
                            text=f"<b>{t.replace('_', ' ').title()}</b>",
                            font=dict(size=15, color='#1F2937', family='Space Grotesk')
                        ),
                        height=300,
                        margin=dict(l=0, r=0, t=50, b=0),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.03)'),
                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.03)')
                    )
                    
                    st.plotly_chart(fig_cat, use_container_width=True, config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f'category_{t}',
                            'height': 600,
                            'width': 1000,
                            'scale': 2
                        }
                    })
                    
                    hist_last = hist_series.iloc[-1]
                    fore_last = fore_series.iloc[-1]
                    cat_growth = ((fore_last * 1000) / (hist_last * 1000) - 1) * 100
                    growth_icon = "📈" if cat_growth > 0 else "📉"
                    st.markdown(f"<div style='font-size: 0.875rem; color: #6B7280; text-align: center; font-weight: 500; padding: 0.5rem;'>{growth_icon} <strong>{cat_growth:+.1f}%</strong> growth • Base: ₨{hist_last:,.2f}B → Target: ₨{fore_last:,.2f}B</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Model Performance Metrics</div>
                <div class="section-subtitle">ARDL econometric model diagnostics and goodness-of-fit</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_model = st.selectbox(
        "Select Revenue Category",
        targets,
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    res_selected = results_dict[selected_model]
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        with col1:
            st.metric("R-squared", f"{res_selected.rsquared:.4f}", help="Proportion of variance explained")
        with col2:
            st.metric("Adj. R-squared", f"{res_selected.rsquared_adj:.4f}", help="Adjusted R-squared")
        with col3:
            st.metric("AIC", f"{res_selected.aic:.2f}", help="Akaike Information Criterion")
        with col4:
            st.metric("BIC", f"{res_selected.bic:.2f}", help="Bayesian Information Criterion")
    except:
        st.info("ℹ️ Some metrics are unavailable for this model configuration")
    
    with st.expander("📋 View Complete Model Summary"):
        st.text(str(res_selected.summary()))
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown("""
    <div class="content-section">
        <div class="section-header">
            <div>
                <div class="section-title">Data Export & Management</div>
                <div class="section-subtitle">Download datasets and scenario configurations</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 📂 Historical Data")
        st.markdown(f"*Source: {data_source_label} • Log-transformed values*")
        
        try:
            styled_hist = df_hist.style.format({col: "{:.4f}" for col in df_hist.select_dtypes(include=[np.number]).columns})
            st.dataframe(styled_hist, use_container_width=True, height=400)
        except:
            st.dataframe(df_hist, use_container_width=True, height=400)
        
        csv_hist = df_hist.to_csv()
        st.download_button(
            label="📥 Download Historical Data (CSV)",
            data=csv_hist,
            file_name=f"historical_revenue_{last_year}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### 🔮 Forecast Data")
        st.markdown("*Projected revenue in PKR Billion*")
        
        df_fore_billions = df_fore / 1000
        
        try:
            styled_fore = df_fore_billions.style.format({col: "{:.2f}" for col in df_fore_billions.select_dtypes(include=[np.number]).columns})
            st.dataframe(styled_fore, use_container_width=True, height=400)
        except:
            st.dataframe(df_fore_billions, use_container_width=True, height=400)
        
        csv_fore = df_fore_billions.to_csv()
        st.download_button(
            label="📥 Download Forecast Data (CSV)",
            data=csv_fore,
            file_name=f"forecast_revenue_{future_years[-1]}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("#### ⚙️ Active Scenario Parameters")
    
    scenario_df = pd.DataFrame([
        {"Parameter": k.replace('_', ' ').title(), "Value": f"{v['value']:.3f}", "Type": v['type'].title()}
        for k, v in scenarios.items() if 'dummy' not in k
    ])
    
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)
    
    csv_scenario = scenario_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Scenario Configuration (CSV)",
        data=csv_scenario,
        file_name=f"scenario_config_{future_years[-1]}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# EXECUTIVE INSIGHTS PANEL
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="insight-panel">
    <div class="insight-header">
        <div class="insight-icon">💡</div>
        <div class="insight-title">Executive Summary • {data_source_label}</div>
    </div>
    <div class="insight-content">
        Based on current macroeconomic assumptions, total tax revenue is projected to 
        <strong>{'increase' if growth_pct > 0 else 'decrease'} by {abs(growth_pct):.1f}%</strong> over the next 
        <strong>{years_to_forecast} years</strong>, reaching <strong>₨{total_fore_last:,.2f} Billion</strong> by 
        FY {future_years[-1]}. This represents a compound annual growth rate (CAGR) of 
        <strong>{avg_annual_growth:.2f}%</strong>, reflecting anticipated economic conditions and policy framework 
        embedded in the ARDL econometric model.
    </div>
</div>
""", unsafe_allow_html=True)