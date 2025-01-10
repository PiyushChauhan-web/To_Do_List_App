import streamlit as st
from datetime import date, timedelta
import pandas as pd

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = pd.DataFrame(columns=['Task', 'Due Date', 'Completed'])

# Helper functions
def add_task(task, due_date):
    new_task = {'Task': task, 'Due Date': due_date, 'Completed': False}
    st.session_state['tasks'] = pd.concat([st.session_state['tasks'], pd.DataFrame([new_task])], ignore_index=True)

def delete_task(index):
    st.session_state['tasks'] = st.session_state['tasks'].drop(index).reset_index(drop=True)

def mark_completed(index):
    st.session_state['tasks'].at[index, 'Completed'] = not st.session_state['tasks'].at[index, 'Completed']

# Layout
def main():
    st.title("To-Do List App 🖍")

    # Sidebar for filters and search
    with st.sidebar:
        st.header("Filter Tasks")
        filter_option = st.radio(
            "View tasks for:", ["All Tasks", "My Day", "This Week", "This Month"]
        )
        search_query = st.text_input("Search tasks", "")

    # Task Input
    with st.form("add_task_form"):
        st.subheader("Add a New Task")
        task = st.text_input("Task Description")
        due_date = st.date_input("Due Date", min_value=date.today())
        submitted = st.form_submit_button("Add Task")

        if submitted:
            if task:
                add_task(task, due_date)
                st.success("Task added successfully!")
            else:
                st.error("Task description cannot be empty.")

    # Filter and Search Logic
    tasks_df = st.session_state['tasks']

    if filter_option == "My Day":
        tasks_df = tasks_df[tasks_df['Due Date'] == date.today()]
    elif filter_option == "This Week":
        start_of_week = date.today()
        end_of_week = start_of_week + timedelta(days=6)
        tasks_df = tasks_df[(tasks_df['Due Date'] >= start_of_week) & (tasks_df['Due Date'] <= end_of_week)]
    elif filter_option == "This Month":
        start_of_month = date.today().replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        tasks_df = tasks_df[(tasks_df['Due Date'] >= start_of_month) & (tasks_df['Due Date'] <= end_of_month)]

    if search_query:
        tasks_df = tasks_df[tasks_df['Task'].str.contains(search_query, case=False, na=False)]

    # Display Tasks
    st.subheader(f"Tasks ({filter_option})")
    if not tasks_df.empty:
        for index, row in tasks_df.iterrows():
            col1, col2, col3, col4 = st.columns([6, 2, 1, 1])
            with col1:
                st.write(row['Task'])
            with col2:
                st.write(row['Due Date'].strftime('%Y-%m-%d'))
            with col3:
                if st.button("✅" if row['Completed'] else "☑️", key=f"complete_{index}"):
                    mark_completed(index)
            with col4:
                if st.button("🗑", key=f"delete_{index}"):
                    delete_task(index)
    else:
        st.write("No tasks available.")

if __name__ == "__main__":
    main()
