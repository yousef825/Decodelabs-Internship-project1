
import streamlit as st 
import pandas as pd 
import numpy as np 
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

# Load and prepare data
df = pd.read_csv('Dataset/cleaned_dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = df['Date'].dt.hour
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Month_Name'] = df['Date'].dt.strftime('%B')

# Streamlit configuration
st.set_page_config(page_title="Sales & Orders Dashboard", layout="wide")
st.title("📊 Sales & Orders Dashboard")


# ==================== SIDEBAR FILTERS ====================
st.sidebar.header("Filters")

# Get all products
all_products = sorted(df['Product'].unique())
# Product selection with "All Products" option
selected_product = st.sidebar.multiselect("Select Products:", ["All Products"] + list(all_products), default=["All Products"])

if "All Products" in selected_product:
    selected_products = all_products
else:
    selected_products = selected_product



# Get all order statuses
all_status = sorted(df['OrderStatus'].unique())
# Status selection with "All Status" option
selected_status = st.sidebar.multiselect("Select Status:", ["All Status"] + list(all_status), default=["All Status"])

if "All Status" in selected_status:
    selected_status = all_status
else:
    selected_status = selected_status



# Get all payment methods
all_payment_method = sorted(df['PaymentMethod'].unique())
# Payment method selection with "All Methods" option
selected_payment = st.sidebar.multiselect("Select Payment Method:",["All Methods"] + list(all_payment_method), default=["All Methods"])

if "All Methods" in selected_payment:
    selected_payment = all_payment_method
else:
    selected_payment = selected_payment


# Apply all filters
filtered_df = df[
    (df['Product'].isin(selected_products)) & 
    (df['OrderStatus'].isin(selected_status)) & 
    (df['PaymentMethod'].isin(selected_payment))
]

# ==================== SIDEBAR KPIs ====================
st.sidebar.markdown("---")
st.sidebar.header("📈 Key Metrics")
col1, col2 = st.sidebar.columns(2)
with col1:
    # st.metric("Total Orders", f"{len(filtered_df):,}")
    st.metric("Avg Order Value", f"${filtered_df['TotalPrice'].mean():.2f}")
    # st.metric("Total Quantity", f"{filtered_df['Quantity'].sum():,}")
with col2:
    # st.metric("Total Revenue", f"${filtered_df['TotalPrice'].sum():,.2f}")
    # st.metric("Unique Customers", f"{filtered_df['CustomerID'].nunique():,}")
    st.metric("Avg Qty/Order", f"{filtered_df['Quantity'].mean():.1f}")

# ==================== TABS STRUCTURE ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📅 Temporal", "📦 Orders", "👥 Customers", "📋 Report"])
# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.header("Products & Revenue Overview")
    product_data = filtered_df['Product'].value_counts().head(10)
    fig_products = px.bar(x=product_data.values, y=product_data.index, title="Products by Orders", labels={'x': 'Orders', 'y': 'Product'},
                          orientation='h', color=product_data.values, color_continuous_scale='Viridis',
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_products, use_container_width=True)
    st.info(f"Total Orders:{len(filtered_df):,}")

    st.markdown("---")

    st.header("Revenue & Quantity Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        product_revenue = filtered_df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=True)
        fig_rev = px.bar(x=product_revenue.values, y=product_revenue.index,
                         title="Revenue by Product", labels={'x': 'Revenue ($)', 'y': 'Product'},
                         color=product_revenue.values, color_continuous_scale='Sunset')
        st.plotly_chart(fig_rev, use_container_width=True)
        
        st.info(f"Total Revenue: ${filtered_df['TotalPrice'].sum():,.2f}")

    with col2:
        product_qty = filtered_df.groupby('Product')['Quantity'].sum().sort_values(ascending=True)
        fig_qty_pie = px.pie(values=product_qty.values, names=product_qty.index,
                     title="Quantity Distribution by Product",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_qty_pie, use_container_width=True)
        
        st.info(f"Total Quantity: {filtered_df['Quantity'].sum():,}")
        
# ==================== TAB 2: TEMPORAL PATTERNS ====================
with tab2:
    st.header("Temporal Patterns Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        monthly = filtered_df.groupby('Month')['TotalPrice'].sum().sort_index()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_labels = [month_names[i-1] for i in monthly.index]
        fig_monthly = go.Figure(data=[go.Scatter(x=month_labels, y=monthly.values, mode='lines+markers', 
                                                   fill='tozeroy', line=dict(color='#2ecc71'))])
        fig_monthly.update_layout(title="Monthly Revenue Trends", xaxis_title="Month", 
                                  yaxis_title="Revenue ($)", hovermode='x unified')
        st.plotly_chart(fig_monthly, use_container_width=True)

    
    with col2:
        st.info("Trend: Strong H1 growth, weaker H2 performance")
        st.info("Biggest Drop: June → July (~48% decrease)")
        st.info("Highest Revenue: June — ~$170K")
        st.info("Lowest Revenue: September — ~$70K")

        # daily_orders = filtered_df.groupby(filtered_df['Date'].dt.date).size()
        # fig_daily = go.Figure(data=[go.Scatter(x=daily_orders.index, y=daily_orders.values, 
        #                                         mode='lines+markers', fill='tozeroy', 
        #                                         line=dict(color='#1f77b4'))])
        # fig_daily.update_layout(title="Daily Order Count", xaxis_title="Date", 
        #                         yaxis_title="Orders", hovermode='x unified')
        # st.plotly_chart(fig_daily, use_container_width=True)

    
        
    day_order = filtered_df['DayOfWeek'].value_counts()
    day_order_sorted = day_order.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig_day = px.bar(x=day_order_sorted.index, y=day_order_sorted.values, 
                    title="Orders by Day of Week", labels={'x': 'Day', 'y': 'Orders'},
                    color=day_order_sorted.index,
                    color_discrete_map={day: '#FF6B6B' if day in ['Saturday', 'Sunday'] else '#4ECDC4' 
                                       for day in day_order_sorted.index})
    
    st.plotly_chart(fig_day, use_container_width=True)

# ==================== TAB 4: ORDER ANALYSIS ====================
with tab3:
    st.header("Order Status Analysis")
    
    pending = len(filtered_df[filtered_df['OrderStatus'] == 'Pending'])
    cancelled = len(filtered_df[filtered_df['OrderStatus'] == 'Cancelled'])
    returned = len(filtered_df[filtered_df['OrderStatus'] == 'Returned'])
    shipped = len(filtered_df[filtered_df['OrderStatus'] == 'Shipped'])
    delivered = len(filtered_df[filtered_df['OrderStatus'] == 'Delivered'])

    status_data = filtered_df['OrderStatus'].value_counts()
    fig_status = px.pie(values=status_data.values, names=status_data.index,
                        title="Order Status Distribution",
                        color_discrete_sequence=['#E74C3C', '#F39C12', '#F1C40F', '#3498DB', '#2ECC71'])
    st.plotly_chart(fig_status, use_container_width=True)
        

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Pending", f"{pending:,}")
    with col2:
        st.metric("Cancelled", f"{cancelled:,}")
    with col3:
        st.metric("Returned", f"{returned:,}")
    with col4:
        st.metric("Shipped", f"{shipped:,}")
    with col5:
        st.metric("Delivered", f"{delivered:,}")
    
    st.markdown("---")

    st.subheader("Critical KPIs")

    total_orders = len(filtered_df)
    cancellation_rate = (cancelled / total_orders * 100) if total_orders > 0 else 0
    return_rate = (returned / total_orders * 100) if total_orders > 0 else 0
    problem_rate = cancellation_rate + return_rate

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%", delta="Goal: <5%")
    with col2:
        st.metric("Return Rate", f"{return_rate:.1f}%", delta="Goal: <3%")
    with col3:
        st.metric("Problem Rate", f"{problem_rate:.1f}%", delta="Goal: <8%")
    
    st.markdown("---")

    st.subheader("Payment Methods & Coupun Impact Analysis")

    col1, col2 = st.columns(2)    
    coupon_used = len(filtered_df[filtered_df['CouponCode'] != 'no_coupon'])
    no_coupon = len(filtered_df[filtered_df['CouponCode'] == 'no_coupon'])
    coupon_rev = filtered_df[filtered_df['CouponCode'] != 'no_coupon']['TotalPrice'].sum()
    no_coupon_rev = filtered_df[filtered_df['CouponCode'] == 'no_coupon']['TotalPrice'].sum()
    
    with col1:
        fig_coupon = px.pie(values=[coupon_used, no_coupon], names=['With Coupon', 'No Coupon'],
                           title="Orders with/without Coupons")
        st.plotly_chart(fig_coupon, use_container_width=True)
        
        st.info("Customer Trend: High reliance on discounts")
        st.info("Coupons drive majority of sales")
        
        
        
    with col2:
        payment_data = filtered_df['PaymentMethod'].value_counts()
        fig_payment = px.bar(x=payment_data.index, y=payment_data.values,
                            title="Orders Payment Method", labels={'x': 'Payment Method', 'y': 'Orders'},
                            color=payment_data.values, color_continuous_scale='Blues')
        st.plotly_chart(fig_payment, use_container_width=True)
        
        st.info("Top Payment Method: Online Payments")
        st.info("Least Used Method: Gift Card")
        st.info("Customers prefer digital transactions") 
        
    
    st.markdown("---")
    
    st.subheader("Orders by Referral Source")
    referral_data = filtered_df['ReferralSource'].value_counts()
    fig_referral = px.pie(values=referral_data.values, names=referral_data.index,
                          title="Orders by Referral Source",
                          color_discrete_sequence=['#E74C3C', '#F39C12', '#F1C40F', '#3498DB', '#2ECC71'])
    st.plotly_chart(fig_referral, use_container_width=True)
    
    st.info("Top Referral Source: Instagram (21.6%)")
    
# ==================== TAB 5: CUSTOMER ANALYSIS ====================
with tab4:
    st.header("Customer Analysis")
    
    customer_data = filtered_df.groupby('CustomerID').agg(
        OrderCount=('OrderID', 'count'),
        TotalSpent=('TotalPrice', 'sum'),
        AvgOrderValue=('TotalPrice', 'mean')
        ).reset_index()
    customer_data['CustomerType'] = np.where(customer_data['OrderCount'] > 1, 'Repeat Buyer', 'One-Time Buyer')    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        repeat_buyers = len(customer_data[customer_data['CustomerType'] == 'Repeat Buyer'])
        st.metric("Repeat Buyers", f"{repeat_buyers:,}")
    with col2:
        one_time = len(customer_data[customer_data['CustomerType'] == 'One-Time Buyer'])
        st.metric("One-Time Buyers", f"{one_time:,}")
    with col3:
        avg_clv = customer_data['TotalSpent'].mean()
        st.metric("Avg CLV", f"${avg_clv:,.2f}")
    with col4:
        repeat_rate = (repeat_buyers / len(customer_data) * 100) if len(customer_data) > 0 else 0
        st.metric("Repeat Rate", f"{repeat_rate:.1f}%")
    
    st.markdown("---")
    st.subheader("Customer Segmentation")
    col1, col2 = st.columns(2)
    
    with col1:
        customer_type_counts = customer_data['CustomerType'].value_counts()
        fig_type = px.pie(values=customer_type_counts.values, names=customer_type_counts.index,
                         title="Repeat vs One-Time Buyers")
        st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        fig_clv = px.histogram(customer_data, x='TotalSpent', nbins=30, title="CLV Distribution",
                              labels={'TotalSpent': 'Customer Lifetime Value ($)'})
        st.plotly_chart(fig_clv, use_container_width=True)
    
    st.subheader("Top 15 Customers")
    top_customers = customer_data.nlargest(15, 'TotalSpent')[['CustomerID', 'OrderCount', 'TotalSpent', 'AvgOrderValue', 'CustomerType']]
    st.dataframe(top_customers, use_container_width=True)
        
# ==================== TAB 5: COMPREHENSIVE REPORT ====================
with tab5:
    st.header("📋 Comprehensive Business Report")
    
    # Calculate key metrics
    cancellation_rate = (cancelled / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    return_rate = (returned / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    total_rev = filtered_df['TotalPrice'].sum()
    coupon_impact = (coupon_rev / (coupon_rev + no_coupon_rev) * 100) if (coupon_rev + no_coupon_rev) > 0 else 0
    avg_customer_value = total_rev / filtered_df['CustomerID'].nunique() if filtered_df['CustomerID'].nunique() > 0 else 0
    customer_report = filtered_df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
    top_customer_value = customer_report.iloc[0] if len(customer_report) > 0 else 0
    
    # ========== Section 1: Dataset Summary ==========
    st.subheader("📊 1. Dataset Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Total Orders:** {len(df):,}")
        st.write(f"**Unique Products:** {df['Product'].nunique()}")
    with col2:
        st.write(f"**Unique Customers:** {df['CustomerID'].nunique()}")
        st.write(f"**Payment Methods:** {df['PaymentMethod'].nunique()}")
    with col3:
        date_min = df['Date'].min().strftime('%Y-%m-%d')
        date_max = df['Date'].max().strftime('%Y-%m-%d')
        st.write(f"**Date Range:** {date_min} to {date_max}")
        st.write(f"**Referral Sources:** {df['ReferralSource'].nunique()}")
    
    st.markdown("---")
    
    # ========== Section 2: Key Findings ==========
    st.subheader("💡 2. Key Findings & Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Revenue & Sales Insights")
        st.write(f"• **Total Revenue:** ${total_rev:,.2f}")
        st.write(f"• **Coupon Penetration:** {coupon_impact:.1f}% from coupon users")
        st.write(f"• **Avg Order Value:** ${filtered_df['TotalPrice'].mean():.2f}")
        st.write(f"• **Top Product:** {product_revenue.idxmax()} (${product_revenue.max():,.2f})")
        referral_rev = filtered_df.groupby('ReferralSource')['TotalPrice'].sum().sort_values(ascending=False)
        st.write(f"• **Best Referral Source:** {referral_rev.idxmax()} (${referral_rev.max():,.2f})")
    
    with col2:
        st.write("### ⚠️ Problem Areas")
        st.write(f"• **Cancellation Rate:** {cancellation_rate:.1f}% ({cancelled:,} orders)")
        st.write(f"• **Return Rate:** {return_rate:.1f}% ({returned:,} orders)")
        st.write(f"• **Combined Issue Rate:** {(cancellation_rate + return_rate):.1f}%")
        st.write(f"• **Pending Orders:** {pending:,} awaiting fulfillment")
        st.write(f"• **Top Customer:** {(top_customer_value/total_rev*100):.2f}% of revenue")
    
    st.markdown("---")
    
    # ========== Section 3: Problem Analysis & Solutions ==========
    st.subheader("🔍 3. Detailed Problem Analysis & Solutions")
    
    with st.expander("❌ Problem 1: High Cancellation & Return Rate ({:.1f}%)".format(cancellation_rate + return_rate), expanded=True):
        st.write(f"""
        **Current Status:** {cancelled} cancellations + {returned} returns = {cancelled + returned} problematic orders
        
        **Root Causes:**
        - Product quality or shipping damage
        - Mismatched customer expectations
        - Payment processing failures
        - Inventory/availability issues
        
        **Solutions:**
        1. **Improve Product Descriptions:** Add detailed specs, dimensions, high-quality images
        2. **Quality Control:** Inspect items pre-shipping to reduce damage
        3. **Customer Communication:** Send detailed order confirmation and set expectations
        4. **Streamline Returns:** Make return process seamless
        5. **Product Analysis:** Identify high-return products and address root causes
        6. **Target:** Reduce to <15% within 90 days
        """)
    
    with st.expander(f"💰 Problem 2: Coupon Dependency ({coupon_impact:.1f}% of revenue)", expanded=False):
        coupon_order_pct = (coupon_used / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.write(f"""
        **Current Status:** {coupon_used} orders ({coupon_order_pct:.1f}%) use coupons = {coupon_impact:.1f}% of revenue
        
        **Risk:** Over-reliance on discounts reduces profit margins and customer lifetime value
        
        **Solutions:**
        1. **Value-Based Marketing:** Emphasize product quality over discounts
        2. **Loyalty Program:** Reward repeat customers with exclusive benefits
        3. **Strategic Coupons:** Use only for new customer acquisition
        4. **Dynamic Pricing:** Use AI for demand-based pricing
        5. **Bundle Offers:** Create bundles to increase AOV without discounting
        6. **Target:** Increase non-coupon revenue to 35% within 6 months
        """)
    
    with st.expander("👥 Problem 3: Low Customer Lifetime Value", expanded=False):
        st.write(f"""
        **Current Status:** Top customer = ${top_customer_value:.2f}; Average customer = ${avg_customer_value:.2f}
        
        **Root Cause:** Limited customer retention and repeat purchase strategy
        
        **Solutions:**
        1. **Customer Segmentation:** Identify high-value vs. at-risk customers
        2. **Personalized Retention:** Targeted offers based on purchase history
        3. **VIP Program:** Exclusive membership for top 10% customers
        4. **Reactivation Campaigns:** Win back inactive customers
        5. **Cross-Sell Strategy:** Recommend complementary products at checkout
        6. **Target:** Increase average customer lifetime value by 50% in 12 months
        """)
    
    with st.expander(f"🌍 Problem 4: Unbalanced Traffic Sources ({referral_rev.idxmin()} vs {referral_rev.idxmax()})", expanded=False):
        best_source = referral_rev.idxmax()
        worst_source = referral_rev.idxmin()
        st.write(f"""
        **Current Status:** {best_source} = ${referral_rev.max():,.2f} vs {worst_source} = ${referral_rev.min():,.2f}
        
        **Root Cause:** Unequal marketing investment and channel optimization
        
        **Solutions:**
        1. **Performance Analysis:** Audit which channels deliver quality customers
        2. **Budget Reallocation:** Shift budget from low to high-ROI channels
        3. **Channel Optimization:** Improve {worst_source} with better targeting
        4. **Diversification:** Reduce {best_source} dependency ({(referral_rev.max()/referral_rev.sum()*100):.1f}%)
        5. **Influencer Partnerships:** Leverage top-performing channels
        6. **Target:** Balance across channels (±20% variance)
        """)
    
    with st.expander("📈 Problem 5: Seasonal Revenue Volatility", expanded=False):
        monthly_revenue = filtered_df.groupby('Month')['TotalPrice'].sum()
        peak_month = monthly_revenue.idxmax()
        low_month = monthly_revenue.idxmin()
        month_names_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        variance = ((monthly_revenue.max() - monthly_revenue.min()) / monthly_revenue.mean() * 100)
        st.write(f"""
        **Current Status:** Monthly revenue variance = {variance:.1f}%
        Peak: ${monthly_revenue.max():,.2f} (Month {peak_month}) | Low: ${monthly_revenue.min():,.2f} (Month {low_month})
        
        **Root Cause:** Lack of consistent marketing and seasonal demand management
        
        **Solutions:**
        1. **Seasonal Calendar:** Plan campaigns for peak seasons
        2. **Off-Season Boosts:** Create promotions during slow months
        3. **Inventory Planning:** Stock popular items during peaks
        4. **Predictive Analytics:** Forecast demand using historical data
        5. **Partnership Campaigns:** Collaborate during slow periods
        6. **Target:** Reduce variance to <30%
        """)
    
    st.markdown("---")
    
    # ========== Section 4: Action Items ==========
    st.subheader("✅ 4. Action Items & Success Metrics")
    
    action_items = pd.DataFrame({
        'Priority': ['🔴 Critical', '🟠 High', '🟠 High', '🟡 Medium', '🟡 Medium'],
        'Action': [
            'Reduce cancellation/return rate',
            'Decrease coupon dependency',
            'Improve customer retention',
            'Optimize referral channels',
            'Stabilize seasonal revenue'
        ],
        'Current Target': [
            f'{(cancellation_rate + return_rate):.1f}% → <15%',
            f'{coupon_impact:.1f}% → 35%',
            f'${avg_customer_value:.0f} → +50%',
            'Unbalanced → Balanced',
            f'{variance:.1f}% → <30%'
        ],
        'Timeline': ['90 days', '6 months', '12 months', '3 months', '6 months'],
        'Owner': ['Operations', 'Marketing', 'CRM Team', 'Marketing', 'Planning']
    })
    
    st.dataframe(action_items, use_container_width=True)
    
    st.markdown("---")
    
    # ========== Section 5: Top Customers ==========
    st.subheader("👑 5. Top 10 Customers by Revenue")
    customer_df = pd.DataFrame({
        'Customer': customer_report.index,
        'Revenue': customer_report.values,
        'Percentage': (customer_report.values / total_rev * 100).round(2)
    })
    st.dataframe(customer_df, use_container_width=True)
    
    st.markdown("---")
    
    # ========== Section 6: Sample Data ==========
    st.subheader("📋 6. Sample Data (First 50 Records)")
    st.dataframe(filtered_df[['OrderID', 'Date', 'CustomerID', 'Product', 'Quantity', 'TotalPrice', 
                              'OrderStatus', 'PaymentMethod', 'ReferralSource']].head(50), use_container_width=True)
