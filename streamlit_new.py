import streamlit as st
import pandas as pd

def load_data(uploaded_file):
    """Loads CSV/Excel file and returns a cleaned DataFrame."""
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')  # Ensure openpyxl is used
            else:
                df = pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None
    return None

def get_filtered_values(df, column_name, filters={}):
    """Returns unique values for a column, filtered based on selected values in other columns."""
    if column_name in df.columns:
        filtered_df = df.copy()
        for col, val in filters.items():
            if val and col in df.columns:
                filtered_df = filtered_df[filtered_df[col] == val]
        
        return sorted(filtered_df[column_name].dropna().unique().tolist())
    return []

def apply_status_background(index):
    """Returns a background color for the Project Status cell in a repeating sequence."""
    status_colors = ["#4CAF50", "#FFC107", "#FF9800", "#8B0000", "#FF0000"]  # Green, Amber Green, Amber, Red Amber, Red
    return status_colors[index % len(status_colors)]  # Cycle through colors

def generate_styled_table_html(df):
    """Generates HTML table with background color styling for Project Status column."""
    if df.empty:
        return "<p>No data available.</p>"
    
    columns = df.columns.tolist()
    table_html = "<table style='width:100%; border-collapse: collapse;'>"

    # Table Headers
    table_html += "<tr style='background-color: #f2f2f2;'>"
    for col in columns:
        table_html += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>{col}</th>"
    table_html += "</tr>"

    # Table Rows with alternating status colors
    for i, row in df.iterrows():
        table_html += "<tr>"
        for col in columns:
            if col == "Project Status":
                color = apply_status_background(i)
                table_html += f"<td style='border: 1px solid #ddd; padding: 8px; background-color: {color}; color: white; font-weight: bold;'>{row[col]}</td>"
            else:
                table_html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{row[col]}</td>"
        table_html += "</tr>"

    table_html += "</table>"
    return table_html

def main():
    st.title("Project Monitoring Dashboard")
    
    uploaded_file = st.file_uploader("Upload Excel/CSV File", type=["csv", "xlsx"])
    df = load_data(uploaded_file) if uploaded_file is not None else None
    
    if df is not None:
        st.markdown("<h3 style='text-align: center;'>Select Options</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            week_selected = st.selectbox("Week", get_filtered_values(df, "Week"), index=None, placeholder="Select Week")
        
        with col2:
            account_options = get_filtered_values(df, "Account Name", {"Week": week_selected})
            account_selected = st.selectbox("Account Name", account_options, index=None, placeholder="Select Account")
        
        with col3:
            client_options = get_filtered_values(df, "Client Name", {"Week": week_selected, "Account Name": account_selected})
            client_selected = st.selectbox("Client Name", client_options, index=None, placeholder="Select Client")
        
        with col4:
            project_options = get_filtered_values(df, "Project Name", {"Week": week_selected, "Account Name": account_selected, "Client Name": client_selected})
            project_selected = st.selectbox("Project Name", project_options, index=None, placeholder="Select Project")
        
        submit = st.button("SUBMIT")

        if submit:
            st.subheader("Project Details")

            # Apply filtering (Only filter non-default selections)
            filtered_data = df.copy()
            if week_selected:
                filtered_data = filtered_data[filtered_data["Week"] == week_selected]
            if account_selected:
                filtered_data = filtered_data[filtered_data["Account Name"] == account_selected]
            if client_selected:
                filtered_data = filtered_data[filtered_data["Client Name"] == client_selected]
            if project_selected:
                filtered_data = filtered_data[filtered_data["Project Name"] == project_selected]

            if not filtered_data.empty:
                # Display table with background-colored Project Status column
                styled_table = generate_styled_table_html(filtered_data)
                st.markdown(styled_table, unsafe_allow_html=True)
            else:
                st.write("No data available for the selected options.")

if __name__ == "__main__":
    main()

# import streamlit as st
# import pandas as pd

# def load_data(uploaded_file):
#     """Loads CSV/Excel file and returns a cleaned DataFrame."""
#     if uploaded_file is not None:
#         try:
#             if uploaded_file.name.endswith('.xlsx'):
#                 df = pd.read_excel(uploaded_file, engine='openpyxl')  # Ensure openpyxl is used
#             else:
#                 df = pd.read_csv(uploaded_file)
#             df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
#             return df
#         except Exception as e:
#             st.error(f"Error loading file: {e}")
#             return None
#     return None

# def get_filtered_values(df, column_name, filters={}):
#     """Returns unique values for a column, filtered based on selected values in other columns."""
#     if column_name in df.columns:
#         filtered_df = df.copy()
#         for col, val in filters.items():
#             if val and val != "All Selections" and col in df.columns:
#                 filtered_df = filtered_df[filtered_df[col] == val]
        
#         values = filtered_df[column_name].dropna().unique().tolist()
#         return ["All Selections"] + sorted(values)  # Include default "All Selections"
#     return ["All Selections"]

# def apply_status_background(index):
#     """Returns a background color for the Project Status cell in a repeating sequence."""
#     status_colors = ["#4CAF50", "#FFC107", "#FF9800", "#8B0000", "#FF0000"]  # Green, Amber Green, Amber, Red Amber, Red
#     return status_colors[index % len(status_colors)]  # Cycle through colors

# def generate_styled_table_html(df):
#     """Generates HTML table with background color styling for Project Status column."""
#     if df.empty:
#         return "<p>No data available.</p>"
    
#     columns = df.columns.tolist()
#     table_html = "<table style='width:100%; border-collapse: collapse;'>"

#     # Table Headers
#     table_html += "<tr style='background-color: #f2f2f2;'>"
#     for col in columns:
#         table_html += f"<th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>{col}</th>"
#     table_html += "</tr>"

#     # Table Rows with alternating status colors
#     for i, row in df.iterrows():
#         table_html += "<tr>"
#         for col in columns:
#             if col == "Project Status":
#                 color = apply_status_background(i)
#                 table_html += f"<td style='border: 1px solid #ddd; padding: 8px; background-color: {color}; color: white; font-weight: bold;'>{row[col]}</td>"
#             else:
#                 table_html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{row[col]}</td>"
#         table_html += "</tr>"

#     table_html += "</table>"
#     return table_html

# def main():
#     st.title("Project Monitoring Dashboard")
    
#     uploaded_file = st.file_uploader("Upload Excel/CSV File", type=["csv", "xlsx"])
#     df = load_data(uploaded_file) if uploaded_file is not None else None
    
#     if df is not None:
#         st.markdown("<h3 style='text-align: center;'>Select Options</h3>", unsafe_allow_html=True)
        
#         col1, col2, col3, col4 = st.columns(4)

#         # Initialize default selections
#         with col1:
#             week_selected = st.selectbox("Week", get_filtered_values(df, "Week"))

#         with col2:
#             account_options = get_filtered_values(df, "Account Name", {"Week": week_selected})
#             account_selected = st.selectbox("Account Name", account_options)

#         with col3:
#             client_options = get_filtered_values(df, "Client Name", {"Week": week_selected, "Account Name": account_selected})
#             client_selected = st.selectbox("Client Name", client_options)

#         with col4:
#             project_options = get_filtered_values(df, "Project Name", {"Week": week_selected, "Account Name": account_selected, "Client Name": client_selected})
#             project_selected = st.selectbox("Project Name", project_options)

#         submit = st.button("SUBMIT")

#         if submit:
#             st.subheader("Project Details")

#             # Apply filtering (Only filter non-default selections)
#             filtered_data = df.copy()
#             if week_selected != "All Selections":
#                 filtered_data = filtered_data[filtered_data["Week"] == week_selected]
#             if account_selected != "All Selections":
#                 filtered_data = filtered_data[filtered_data["Account Name"] == account_selected]
#             if client_selected != "All Selections":
#                 filtered_data = filtered_data[filtered_data["Client Name"] == client_selected]
#             if project_selected != "All Selections":
#                 filtered_data = filtered_data[filtered_data["Project Name"] == project_selected]

#             if not filtered_data.empty:
#                 # Display table with background-colored Project Status column
#                 styled_table = generate_styled_table_html(filtered_data)
#                 st.markdown(styled_table, unsafe_allow_html=True)
#             else:
#                 st.write("No data available for the selected options.")

# if __name__ == "__main__":
#     main()