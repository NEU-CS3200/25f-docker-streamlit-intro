# API Access Page

import streamlit as st
import requests
import pandas as pd


st.title("API Access")
st.markdown("Explore JSONPlaceholder API endpoints and visualize the data")

# Base URL for JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"

# Sidebar for endpoint selection
st.sidebar.header("API Endpoints")
endpoint_options = {
    "Posts": "/posts",
    "Comments": "/comments",
    "Albums": "/albums",
    "Photos": "/photos",
    "Todos": "/todos",
    "Users": "/users"
}

selected_endpoint = st.sidebar.selectbox(
    "Select an endpoint:",
    options=list(endpoint_options.keys())
)

# Additional options for specific resources
st.sidebar.markdown("---")
st.sidebar.subheader("Options")

# For posts, allow filtering by user ID
if selected_endpoint == "Posts":
    user_id_filter = st.sidebar.number_input(
        "Filter by User ID (0 for all):",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )
else:
    user_id_filter = 0

# For posts and comments, allow selecting a specific ID
if selected_endpoint in ["Posts", "Comments", "Albums", "Photos", "Todos", "Users"]:
    specific_id = st.sidebar.number_input(
        f"Get specific {selected_endpoint[:-1].lower()} by ID (0 for all):",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )
else:
    specific_id = 0

# Make API request
def fetch_data(endpoint_path, resource_id=0, user_id=0):
    """Fetch data from JSONPlaceholder API"""
    try:
        if resource_id > 0:
            # Fetch specific resource by ID
            url = f"{BASE_URL}{endpoint_path}/{resource_id}"
        elif user_id > 0 and endpoint_path == "/posts":
            # Filter posts by user ID
            url = f"{BASE_URL}{endpoint_path}?userId={user_id}"
        else:
            # Fetch all resources
            url = f"{BASE_URL}{endpoint_path}"
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), response.status_code, None
    except requests.exceptions.RequestException as e:
        return None, None, str(e)

# Fetch button
if st.button("Fetch Data", type="primary"):
    with st.spinner(f"Fetching {selected_endpoint.lower()}..."):
        data, status_code, error = fetch_data(
            endpoint_options[selected_endpoint],
            specific_id if specific_id > 0 else 0,
            user_id_filter if user_id_filter > 0 else 0
        )
        
        if error:
            st.error(f"Error fetching data: {error}")
        elif data:
            st.success(f"Successfully fetched data! (Status: {status_code})")
            
            # Store data in session state for visualization
            st.session_state['api_data'] = data
            st.session_state['endpoint_name'] = selected_endpoint
        else:
            st.warning("No data returned from API")

# Display data if available
if 'api_data' in st.session_state and st.session_state['api_data']:
    data = st.session_state['api_data']
    endpoint_name = st.session_state.get('endpoint_name', selected_endpoint)
    
    st.markdown("---")
    st.header(f"{endpoint_name} Data")
    
    # Handle single object vs list
    if isinstance(data, dict):
        data_list = [data]
    else:
        data_list = data
    
    # Display metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(data_list))
    
    if data_list and isinstance(data_list[0], dict):
        col2.metric("Fields per Record", len(data_list[0].keys()))
        # Show sample keys
        sample_keys = ", ".join(list(data_list[0].keys())[:5])
        if len(data_list[0].keys()) > 5:
            sample_keys += "..."
        col3.metric("Sample Fields", sample_keys)
    
    # Convert to DataFrame and display
    st.subheader("Data Table")
    df = pd.DataFrame(data_list)
    st.dataframe(df, use_container_width=True, height=400)
    
    # Display raw JSON
    with st.expander("View Raw JSON"):
        st.json(data)
    
    # Additional visualizations based on endpoint type
    st.subheader("Data Insights")
    
    if endpoint_name == "Posts":
        # Posts-specific visualizations
        if len(data_list) > 0:
            # Count posts by user
            if 'userId' in df.columns:
                posts_by_user = df['userId'].value_counts().sort_index()
                st.bar_chart(posts_by_user)
                st.caption("Number of posts per user")
            
            # Word count analysis (if we have titles)
            if 'title' in df.columns and len(df) > 0:
                df['title_length'] = df['title'].str.len()
                st.metric("Average Title Length", f"{df['title_length'].mean():.1f} characters")
    
    elif endpoint_name == "Comments":
        # Comments-specific visualizations
        if len(data_list) > 0 and 'postId' in df.columns:
            comments_by_post = df['postId'].value_counts().head(10)
            st.bar_chart(comments_by_post)
            st.caption("Top 10 posts by comment count")
    
    elif endpoint_name == "Users":
        # Users-specific visualizations
        if len(data_list) > 0:
            st.write("User Information:")
            for user in data_list:
                with st.expander(f"User {user.get('id', 'N/A')}: {user.get('name', 'N/A')}"):
                    st.write(f"**Username:** {user.get('username', 'N/A')}")
                    st.write(f"**Email:** {user.get('email', 'N/A')}")
                    st.write(f"**Phone:** {user.get('phone', 'N/A')}")
                    st.write(f"**Website:** {user.get('website', 'N/A')}")
                    if 'address' in user:
                        st.write(f"**Address:** {user['address'].get('street', '')}, {user['address'].get('city', '')}")
                    if 'company' in user:
                        st.write(f"**Company:** {user['company'].get('name', 'N/A')}")
    
    elif endpoint_name == "Todos":
        # Todos-specific visualizations
        if len(data_list) > 0 and 'completed' in df.columns:
            completed_count = df['completed'].sum()
            total_count = len(df)
            completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
            
            col1, col2 = st.columns(2)
            col1.metric("Completed", completed_count)
            col2.metric("Completion Rate", f"{completion_rate:.1f}%")
            
            # Pie chart data
            completion_data = pd.DataFrame({
                'Status': ['Completed', 'Pending'],
                'Count': [completed_count, total_count - completed_count]
            })
            st.bar_chart(completion_data.set_index('Status'))
    
    elif endpoint_name == "Albums":
        # Albums-specific visualizations
        if len(data_list) > 0 and 'userId' in df.columns:
            albums_by_user = df['userId'].value_counts().sort_index()
            st.bar_chart(albums_by_user)
            st.caption("Number of albums per user")
    
    elif endpoint_name == "Photos":
        # Photos-specific visualizations
        if len(data_list) > 0:
            st.write(f"Total photos: {len(data_list)}")
            if 'albumId' in df.columns:
                photos_by_album = df['albumId'].value_counts().head(10)
                st.bar_chart(photos_by_album)
                st.caption("Top 10 albums by photo count")
            
            # Display sample images if thumbnailUrl exists
            if 'thumbnailUrl' in df.columns and len(df) > 0:
                st.subheader("Sample Images")
                sample_photos = df.head(6)
                cols = st.columns(3)
                for idx, (_, photo) in enumerate(sample_photos.iterrows()):
                    with cols[idx % 3]:
                        st.image(photo.get('thumbnailUrl', ''), caption=photo.get('title', 'Photo')[:30])
    
    # Download button
    st.markdown("---")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{endpoint_name.lower()}_data.csv",
        mime="text/csv"
    )

else:
    # Show instructions when no data is loaded
    st.info("👆 Select an endpoint and click 'Fetch Data' to get started!")
    
    st.markdown("### Available Endpoints:")
    st.markdown("""
    - **Posts**: 100 posts with title, body, userId
    - **Comments**: 500 comments linked to posts
    - **Albums**: 100 albums with userId
    - **Photos**: 5000 photos with albumId and image URLs
    - **Todos**: 200 todos with completion status
    - **Users**: 10 users with contact information
    """)
    
    st.markdown("### Features:")
    st.markdown("""
    - 📊 Interactive data tables
    - 📈 Visualizations and insights
    - 📥 Download data as CSV
    - 🔍 Filter by ID or user
    - 📋 View raw JSON
    """)
