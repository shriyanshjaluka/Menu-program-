
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Financial & Inventory Management",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial & Inventory Management System")
st.caption("Manage products, prices, profits and inventory in one place.")

# ==========================================
# 2. DEMO DATA
# ==========================================

data = {
    "Product": [
        "Laptop", "Mobile", "Keyboard", "Mouse",
        "Monitor", "Printer", "Headphones", "Tablet",
        "Speaker", "Webcam", "Router", "USB Drive"
    ],

    "Cost Price": [
        40000, 12000, 700, 300,
        8000, 5000, 1000, 15000,
        1500, 800, 2000, 400
    ],

    "Selling Price": [
        48000, 15000, 1000, 500,
        10000, 6500, 1500, 18000,
        2200, 1200, 2700, 600
    ],

    "Current Stock": [
        15, 30, 50, 100,
        20, 12, 40, 18,
        25, 35, 16, 80
    ]
}

demo_df = pd.DataFrame(data)

demo_df["Profit per Unit"] = (
    demo_df["Selling Price"] - demo_df["Cost Price"]
)

demo_df["Stock Value"] = (
    demo_df["Cost Price"] * demo_df["Current Stock"]
)

demo_df["Potential Profit"] = (
    demo_df["Profit per Unit"] * demo_df["Current Stock"]
)

# ==========================================
# 3. SESSION STORAGE
# ==========================================

if "products" not in st.session_state:
    st.session_state.products = []

# ==========================================
# 4. HELPER FUNCTION
# ==========================================

def prepare_data(records):

    df = pd.DataFrame(records)

    if not df.empty:

        df["Profit per Unit"] = (
            df["Selling Price"] - df["Cost Price"]
        )

        df["Stock Value"] = (
            df["Cost Price"] * df["Current Stock"]
        )

        df["Potential Profit"] = (
            df["Profit per Unit"] * df["Current Stock"]
        )

    return df


# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🏢 Main Menu")

page = st.sidebar.selectbox(
    "Select Section",
    [
        "Home Dashboard",
        "Add Product",
        "Update Product",
        "Sell Product",
        "Charts",
        "Product Records",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Financial Management System\n\n"
    "Manage your business inventory easily."
)

# ==========================================
# 6. HOME DASHBOARD
# ==========================================

if page == "Home Dashboard":

    st.header("Business Overview")

    source = st.radio(
        "Choose Data Source",
        ["My Data", "Demo Data"],
        horizontal=True
    )

    if source == "Demo Data":
        df = demo_df.copy()
    else:
        df = prepare_data(st.session_state.products)

    if df.empty:

        st.warning("No product records available.")

    else:

        total_products = len(df)

        total_stock = df["Current Stock"].sum()

        stock_value = df["Stock Value"].sum()

        potential_profit = df["Potential Profit"].sum()

        # Dashboard cards

        c1, c2 = st.columns(2)

        c1.metric(
            "Total Products",
            f"{total_products:,}"
        )

        c2.metric(
            "Total Stock Units",
            f"{total_stock:,}"
        )

        c3, c4 = st.columns(2)

        c3.metric(
            "Total Inventory Value",
            f"₹{stock_value:,.2f}"
        )

        c4.metric(
            "Potential Stock Profit",
            f"₹{potential_profit:,.2f}"
        )

        st.divider()

        # Low stock alert

        st.subheader("⚠️ Low Stock Alert")

        low_stock = df[df["Current Stock"] <= 5]

        if not low_stock.empty:

            st.warning(
                f"{len(low_stock)} product(s) have low stock."
            )

            st.dataframe(
                low_stock,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success("All products have sufficient stock.")

        # Product records

        st.subheader("Product Overview")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# 7. ADD PRODUCT
# ==========================================

elif page == "Add Product":

    st.header("➕ Add New Product")

    st.subheader("Demo Data Reference")

    st.caption(
        "Use the following table to understand "
        "the format for entering your data."
    )

    st.dataframe(
        demo_df.head(5),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Enter Product Details")

    with st.form("add_product_form"):

        product = st.text_input(
            "Product Name",
            placeholder="Example: Laptop"
        )

        cp = st.number_input(
            "Cost Price (₹)",
            min_value=0.0,
            step=100.0
        )

        sp = st.number_input(
            "Selling Price (₹)",
            min_value=0.0,
            step=100.0
        )

        stock = st.number_input(
            "Current Stock (Units)",
            min_value=0,
            step=1
        )

        submit = st.form_submit_button(
            "Add Product",
            use_container_width=True
        )

        if submit:

            if not product.strip():

                st.error("Please enter a product name.")

            elif any(
                p["Product"].lower() == product.strip().lower()
                for p in st.session_state.products
            ):

                st.error("This product already exists.")

            elif cp <= 0 or sp <= 0:

                st.error("Enter valid prices greater than zero.")

            else:

                st.session_state.products.append({
                    "Product": product.strip(),
                    "Cost Price": cp,
                    "Selling Price": sp,
                    "Current Stock": stock
                })

                st.success(
                    f"{product} added successfully!"
                )

                st.info(
                    f"Profit per unit: ₹{sp - cp:,.2f}"
                )

    st.divider()

    st.subheader("Your Products")

    if st.session_state.products:

        df = prepare_data(st.session_state.products)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No products added yet.")

# ==========================================
# 8. UPDATE PRODUCT
# ==========================================

elif page == "Update Product":

    st.header("✏️ Update Product Details")

    if not st.session_state.products:

        st.warning("Please add a product first.")

    else:

        product_names = [
            p["Product"]
            for p in st.session_state.products
        ]

        selected = st.selectbox(
            "Select Product",
            product_names
        )

        index = next(
            i for i, p in enumerate(st.session_state.products)
            if p["Product"] == selected
        )

        current = st.session_state.products[index]

        with st.form("update_form"):

            new_name = st.text_input(
                "Product Name",
                value=current["Product"]
            )

            new_cp = st.number_input(
                "Cost Price (₹)",
                min_value=0.0,
                value=float(current["Cost Price"]),
                step=100.0
            )

            new_sp = st.number_input(
                "Selling Price (₹)",
                min_value=0.0,
                value=float(current["Selling Price"]),
                step=100.0
            )

            new_stock = st.number_input(
                "Current Stock",
                min_value=0,
                value=int(current["Current Stock"]),
                step=1
            )

            update = st.form_submit_button(
                "Save Changes",
                use_container_width=True
            )

            if update:

                duplicate = any(
                    p["Product"].lower() == new_name.strip().lower()
                    and i != index
                    for i, p in enumerate(st.session_state.products)
                )

                if not new_name.strip():

                    st.error("Product name cannot be empty.")

                elif duplicate:

                    st.error("Another product has this name.")

                elif new_cp <= 0 or new_sp <= 0:

                    st.error("Prices must be greater than zero.")

                else:

                    st.session_state.products[index] = {
                        "Product": new_name.strip(),
                        "Cost Price": new_cp,
                        "Selling Price": new_sp,
                        "Current Stock": new_stock
                    }

                    st.success("Product updated successfully!")

# ==========================================
# 9. SELL PRODUCT
# ==========================================

elif page == "Sell Product":

    st.header("🛒 Sell Product / Update Stock")

    if not st.session_state.products:

        st.warning("Please add a product first.")

    else:

        product_names = [
            p["Product"]
            for p in st.session_state.products
        ]

        selected = st.selectbox(
            "Select Product",
            product_names
        )

        index = next(
            i for i, p in enumerate(st.session_state.products)
            if p["Product"] == selected
        )

        current = st.session_state.products[index]

        st.info(
            f"Available Stock: {current['Current Stock']} units"
        )

        with st.form("sell_form"):

            quantity = st.number_input(
                "Enter Quantity to Sell",
                min_value=1,
                max_value=max(1, int(current["Current Stock"])),
                step=1,
                disabled=current["Current Stock"] == 0
            )

            sell = st.form_submit_button(
                "Confirm Sale",
                use_container_width=True,
                disabled=current["Current Stock"] == 0
            )

            if sell:

                if quantity > current["Current Stock"]:

                    st.error("Insufficient stock!")

                else:

                    current["Current Stock"] -= quantity

                    st.session_state.products[index] = current

                    total_amount = (
                        current["Selling Price"] * quantity
                    )

                    total_profit = (
                        current["Selling Price"]
                        - current["Cost Price"]
                    ) * quantity

                    st.success("Sale completed successfully!")

                    st.write(
                        f"Total Sales Amount: ₹{total_amount:,.2f}"
                    )

                    st.write(
                        f"Profit from Sale: ₹{total_profit:,.2f}"
                    )

                    st.write(
                        f"Remaining Stock: {current['Current Stock']}"
                    )

# ==========================================
# 10. CHARTS
# ==========================================

elif page == "Charts":

    st.header("📈 Financial Charts")

    source = st.radio(
        "Select Data",
        ["My Data", "Demo Data"],
        horizontal=True
    )

    if source == "Demo Data":

        df = demo_df.copy()

    else:

        df = prepare_data(st.session_state.products)

    if df.empty:

        st.warning("Please add your products first.")

    else:

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart"
            ]
        )

        fig, ax = plt.subplots(figsize=(12, 6))

        # BAR CHART

        if chart_type == "Bar Chart":

            x = range(len(df))

            width = 0.35

            ax.bar(
                [i - width / 2 for i in x],
                df["Cost Price"],
                width,
                label="Cost Price"
            )

            ax.bar(
                [i + width / 2 for i in x],
                df["Selling Price"],
                width,
                label="Selling Price"
            )

            ax.set_xticks(list(x))

            ax.set_xticklabels(
                df["Product"],
                rotation=45,
                ha="right"
            )

            ax.set_title("Cost Price vs Selling Price")

            ax.set_ylabel("Amount (₹)")

            ax.legend()

        # LINE CHART

        elif chart_type == "Line Chart":

            ax.plot(
                df["Product"],
                df["Cost Price"],
                marker="o",
                label="Cost Price"
            )

            ax.plot(
                df["Product"],
                df["Selling Price"],
                marker="o",
                label="Selling Price"
            )

            ax.plot(
                df["Product"],
                df["Profit per Unit"],
                marker="o",
                label="Profit per Unit"
            )

            ax.set_title("Product Price and Profit Analysis")

            ax.set_ylabel("Amount (₹)")

            ax.set_xlabel("Products")

            ax.legend()

            ax.grid(True)

            plt.xticks(rotation=45, ha="right")

        # PIE CHART

        elif chart_type == "Pie Chart":

            profit_df = df[
                (df["Potential Profit"] > 0)
            ]

            if profit_df.empty:

                ax.text(
                    0.5, 0.5,
                    "No positive potential profit available",
                    ha="center",
                    va="center"
                )

            else:

                ax.pie(
                    profit_df["Potential Profit"],
                    labels=profit_df["Product"],
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.set_title(
                    "Potential Profit Distribution by Product"
                )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

        st.caption(
            "Pie chart displays the distribution of positive "
            "potential profit from current stock."
        )

# ==========================================
# 11. PRODUCT RECORDS
# ==========================================

elif page == "Product Records":

    st.header("📋 Product Records")

    source = st.radio(
        "Select Records",
        ["My Data", "Demo Data"],
        horizontal=True
    )

    if source == "Demo Data":

        df = demo_df.copy()

    else:

        df = prepare_data(st.session_state.products)

    if df.empty:

        st.warning("No records found.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "product_records.csv",
            "text/csv"
        )

    st.divider()

    st.subheader("Delete Product")

    if st.session_state.products:

        names = [
            p["Product"]
            for p in st.session_state.products
        ]

        delete_name = st.selectbox(
            "Choose Product to Delete",
            names,
            key="delete_product"
        )

        if st.button("Delete Selected Product"):

            st.session_state.products = [
                p for p in st.session_state.products
                if p["Product"] != delete_name
            ]

            st.success(
                f"{delete_name} deleted successfully."
            )

            st.rerun()

    else:

        st.info("No user products available to delete.")

# ==========================================
# 12. ABOUT PAGE
# ==========================================

elif page == "About":

    st.header("About This Project")

    st.write("""
    Financial and Inventory Management System

    Developed using Python, Pandas, Matplotlib and Streamlit.

    FEATURES:

    1. Product Management
    2. Cost Price Management
    3. Selling Price Management
    4. Current Stock Management
    5. Automatic Profit Calculation
    6. Bar Chart
    7. Line Chart
    8. Pie Chart
    9. Low Stock Alerts
    10. Sell Product Functionality
    11. Update Product
    12. Delete Product
    13. CSV Download
    """)

    st.success(
        "Thank you for using Financial Management System!"
    )

    st.caption("Created with Python and Streamlit.")

