
import seaborn as sns
import streamlit as st
st.set_page_config(page_title="ChatSleuth", page_icon="🕵️‍♂️", layout="wide")
import preprocessor
import helper
import matplotlib.pyplot as plt


st.sidebar.markdown(
    """
    <h1 style='font-family:Segoe UI; color:#1E9AFF; font-size: 36px;'>🕵️‍♂️ ChatSleuth</h1>
    <p style='font-size:16px; color:#9ED3FF;'>From Texts to Trends – Your Chats, Analyzed.</p>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)



    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t. ",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,links = helper.fetch_stats(selected_user,df)
        st.markdown("""
            <h1 style='text-align: center; color: #FFFFFF; font-family: Segoe UI;'>Top Statistics</h1>
        """, unsafe_allow_html=True)
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)



        with col1:
            st.markdown("""
                    <div style='background-color: #FFFFFF; padding: 1px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>
                        <h4 style='color: #2c3e50; font-family: Segoe UI;'>Total Messages</h4>
                        <h2 style='color: #1a73e8;'>""" + str(num_messages) + """</h2>
                    </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                                <div style='background-color: #FFFFFF; padding: 1px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>
                                    <h4 style='color: #2c3e50; font-family: Segoe UI;'>Total Words</h4>
                                    <h2 style='color: #1a73e8;'>""" + str(words) + """</h2>
                                </div>
                            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                                <div style='background-color: #FFFFFF; padding: 1px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>
                                    <h4 style='color: #2c3e50; font-family: Segoe UI;'> Media Shared</h4>
                                    <h2 style='color: #1a73e8;'>""" + str(num_media_messages) + """</h2>
                                </div>
                            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
                                <div style='background-color: #FFFFFF; padding: 1px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>
                                    <h4 style='color: #2c3e50; font-family: Segoe UI;'>Total Links</h4>
                                    <h2 style='color: #1a73e8;'>""" + str(links) + """</h2>
                                </div>
                            """, unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            # monthly timeline
            st.markdown("---")
            st.markdown("### 🔹 Monthly Timeline")
            st.markdown("---")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            # daily timeline
            st.markdown("---")
            st.markdown("### 🔹 Daily Timeline")
            st.markdown("---")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #finding busy users

        if selected_user == 'Overall':

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("---")
                st.markdown("#### 🔹 Most Active Users")
                st.markdown("---")
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.markdown("---")
                st.markdown("#### 🔹 User Contribution (%)")
                st.markdown("---")
                st.dataframe(new_df)
                # activity map

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("---")
                    st.markdown("### 🔹 Most Busy Day")
                    st.markdown("---")
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values, color='purple')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.markdown("---")
                    st.markdown("### 🔹 Most Busy Month")
                    st.markdown("---")
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
        # WordCloud
        st.markdown("---")
        st.markdown("#### 🔹 Word Cloud")
        st.markdown("---")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.markdown("---")
        st.markdown("#### 🔹 Most Common Words")
        st.markdown("---")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='#FAE206')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("---")
        st.markdown("### 🔹 Weekly Activity Map")
        st.markdown("---")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #Emoji analysis
        st.markdown("---")
        st.markdown("#### 🔹Emoji Analysis")
        st.markdown("---")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f%%")

            st.pyplot(fig)