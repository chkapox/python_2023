import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('dark_background')


# Function for the first figure __________________________________________________________
def sport(subject):
    bar = plt.figure(figsize=(10, 6))
    order = ['regularly', 'sometimes', 'never']
    sns.barplot(
        df_for_sport, x='WklyStudyHours', y=(subject + 'Score'),
        hue='PracticeSport', palette='light:#4E5173',
        hue_order=order, order=['< 5', '5 - 10', '> 10']
    ).legend(bbox_to_anchor=(1.02, 0.15), loc='upper left', borderaxespad=0)
    plt.ylabel((str(subject) + 'score'))
    plt.xlabel('Weekly studying hours')
    return bar


# Title of the site __________________________________________________________

st.set_page_config(page_title="my project", layout='wide')
toggle_switch = st.toggle('Notebook mode', value=True)
df = pd.read_csv(r'Expanded_data_with_more_features.csv',
                 index_col=0)
df_dirty = pd.read_csv(r'Expanded_data_with_more_features.csv')
df_cleaned = df.dropna()
df1 = df
df1['MeanScore'] = df[['MathScore', 'ReadingScore', 'WritingScore']].mean(axis=1)
df1 = df1.dropna()
if toggle_switch:
    st.title("Students' performance based on their data :sunglasses:")
    st.write('---')
    # datafarme with buttons __________________________________________________________
    st.dataframe(df)
    left, right = st.columns(2)
    with right:
        with st.expander('See the number of NaN Values'):
            st.write('##')
            st.write('##')
            st.write('##')
            st.write(df.isna().sum())
    with left:
        with st.expander('Show options'):
            button_name = ['Cleaned and modified', 'Not cleaned']
            button = st.radio(' ', button_name)
            if button == 'Cleaned and modified':
                df1['MeanScore'] = df_dirty[['MathScore', 'ReadingScore', 'WritingScore']].mean(axis=1)
                st.dataframe(df1.dropna())
            else:
                st.dataframe(df)
    st.write('___')
    # simple figures
    st.write("Let's take a look on some simple graphs to briefly get some information about this dataset")
    pie1 = px.pie(df_cleaned, names='Gender', title='Sex')
    pie2 = px.pie(df_cleaned, names='NrSiblings', title='The amount of siblings')
    pie3 = px.pie(df_cleaned, names='ParentMaritalStatus', title='The ratio of different parent marital statuses')
    pie4 = px.pie(df_cleaned, names='Gender', title='The amount of males and females', template='plotly_dark')
    pie_right, pie_left = st.columns(2)
    with pie_right:
        st.plotly_chart(pie1)
        st.plotly_chart(pie2)
    with pie_left:
        st.plotly_chart(pie3)
        st.plotly_chart(pie4)
    st.write('---')
    # first complicated figure  __________________________________________________________

    # global dataset transformations _______________________________________________________________
    st.title('Do sport affect on studying?')

    df_for_sport = df.groupby(
        by=['WklyStudyHours', 'PracticeSport'], as_index=False
    ).agg(MathScore=('MathScore', 'mean'), ReadingScore=('ReadingScore', 'mean'), WritingScore=('WritingScore', 'mean'))

    st.write(
        "Let's take a look at the correlation between exam results and hours of "
        "weekly preparation as well as the frequency of sporting activities"
    )
    st.write(
        'As it seen from all three graphs,'
        ' pupils that regularly and sometimes practise sports are more likely to write test better than '
        'the ones who are not practising.''\n'
        '\n''Also it is seen that pupils who are studying more hours per day are not always getting higher scores.'
    )
    st.write('##')
    left1, right1 = st.columns(2)
    with left1:
        st.write('Choose the subject')
        score_buttons = ['Math', 'Reading', 'Writing']
        buttons = st.radio(' ', score_buttons)
    with right1:
        st.write('Choose the exercise frequency')
        st.write("##")
        regularly = st.checkbox('Regularly', value=True)
        sometimes = st.checkbox('Sometimes', value=True)
        never = st.checkbox('Never', value=True)

    if not never:
        df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'never']
    if not sometimes:
        df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'sometimes']
    if not regularly:
        df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'regularly']

    if buttons == 'Math':
        st.pyplot(sport('Math').get_figure())
    elif buttons == 'Reading':
        st.pyplot(sport('Reading').get_figure())
    else:
        st.pyplot(sport('Writing').get_figure())

    st.header('Microlead')
    st.write(
        'As it seen from all three graphs,'
        ' pupils that regularly and sometimes practise sports are more likely to write test better than '
        'the ones whos not practising.''\n'
        '\n''Also it is seen that pupils who are studying more hours per day are not always getting higher scores.'
    )
    # ____________________________________________________________________________________________________________________
    st.write('---')
    st.title(
        "Then, let's see how parent education and their merital status"
        " as well as their gender affects on their mean score")
    violin1 = plt.figure(figsize=(30, 15))
    sns.violinplot(
        data=df1, bw_adjust=1, cut=2, linewidth=1,
        x='ParentEduc', y='MeanScore',
        hue='ParentMaritalStatus', palette=['#e0aaff', '#c77dff', '#9d4edd', '#7b2cbf']
    ).legend(bbox_to_anchor=(1.01, 0.08), loc='upper left', borderaxespad=0)
    plt.show()
    violin2 = plt.figure(figsize=(16, 9))
    sns.violinplot(
        data=df1, bw_adjust=1, cut=2,
        linewidth=1, x='ParentEduc', y='MeanScore',
        hue='Gender', palette=['#e0aaff', '#7b2cbf']
    ).legend(bbox_to_anchor=(1.01, 0.08), loc='upper left', borderaxespad=0)
    st.pyplot(violin1.get_figure())
    st.pyplot(violin2.get_figure())
    st.title('Microlead')

    st.write(
        "The first graph shows that pupils with a widowed parent are less evenly distributed than the others."
        "This is especially evident in the case of a parent with"
        " a bachelor's degree The second graph, on the other hand,"
        "indicates the same median for both sexes, and also in some"
        " places both boys and girls have a slightly unequal distribution"
    )
    st.write('---')
    # scatter______________________________________
    st.title("Next, I want to see if ethnicity as well as parent education affects test results.")
    df3 = df.loc[(df['MathScore'] >= 80) & (df['WritingScore'] >= 80) & (df['ReadingScore'] >= 80)]
    df3 = df3.sort_values(by='ReadingScore')
    df3 = df3.dropna()
    sp = px.scatter(
        df3, x='WritingScore', y='MathScore', animation_frame='ReadingScore', animation_group='EthnicGroup',
        color='ParentEduc', facet_col='EthnicGroup', size='NrSiblings',
        range_y=[70, 105], range_x=[70, 105], log_x=True, size_max=30, template='plotly_dark'
    )
    pirog = px.pie(df3, names='ParentEduc', template='plotly_dark', title="Parent's education")
    st.plotly_chart(sp, use_container_width=True)
    st.plotly_chart(pirog, use_container_width=True)
    st.title("Microlead")
    st.write(
        "it's noticeable that group A has a predominant concentration of students,"
        " most of whom have parents who graduated from college. Also, the better the score in one subject,"
        "the more likely it is to be higher in the other two.")
    st.write('---')
    # ______________________________________________________________________________________________________________
    st.title('Next thing')
    st.write(
        "The next thing is I want to see the pattern between math and writing test scores "
        "(I consider the reading test to be the easiest one that doesn't require much mental ability,"
        " so I want to compare the two more difficult exams) and also to see if the number of siblings"
        " affects the score."
    )

    fig = px.scatter(
        df3, x='WritingScore', y='MathScore', color='NrSiblings', size='NrSiblings',
        size_max=30, template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    st.title('Microlead')
    st.write(
        "This graph shows that this has no effect on the result, "
        "since at almost any point several points are overlapping,"
        " so the number of siblings has no effect on the math and writing results"
    )
    st.write('---')
    # ____________________________________________________________________________________________
    st.header('Overall')
    st.write(
        "Having analyzed this dataset I can confidently state that exercising definitely improves productivity "
        "and test results as well. I can justify it by the fact that sport disciplines a person"
        " and keeps him mentally healthy. I can also say that the parents' marital status also matters,"
        " because family is where a student spends most of his time, and if there are any problems in the family,"
        " it will affect on the results of studying. I would also like to point out that the type of lunch"
        " and the number of siblings in most cases also has no influence,"
        " but the education of the parent sometimes matters."
    )
else:
    selected = option_menu(
        menu_title=None,
        options=[
            'Dataset showcase', 'Observe the dataset', 'Sport affection',
            'Hypothesis check'
        ],
        icons=['box-arrow-up', 'box-seam', 'backpack', 'bookmark'],
        menu_icon='',
        default_index=0,
        orientation="horizontal",

    )
    # plate1, plate2, plate3, plate4 = st.tabs(
    #     [
    #         'Dataset showcase', 'Observe the dataset', 'Sport affection',
    #         'Forwarding hypothesis check with complex figures'
    #     ],
    # )
    if selected == 'Dataset showcase':
        st.title("Students' performance based on their data :sunglasses:")
        st.write('---')
        st.dataframe(df)
        st.write("Let's take a look on some simple graphs to briefly get some information about this dataset")
        pie1 = px.pie(df_cleaned, names='Gender', title='Sex')
        pie2 = px.pie(df_cleaned, names='NrSiblings', title='The amount of siblings')
        pie3 = px.pie(df_cleaned, names='ParentMaritalStatus', title='The ratio of different parent marital statuses')
        pie4 = px.pie(df_cleaned, names='Gender', title='The amount of males and females', template='plotly_dark')
        pie_right, pie_left = st.columns(2)
        with pie_right:
            st.plotly_chart(pie1)
            st.plotly_chart(pie2)
        with pie_left:
            st.plotly_chart(pie3)
            st.plotly_chart(pie4)
    if selected == 'Observe the dataset':
        st.dataframe(df)
        left, right = st.columns(2)
        with right:
            with st.expander('See the number of NaN Values'):
                st.write('##')
                st.write('##')
                st.write('##')
                st.write(df.isna().sum())
        with left:
            with st.expander('Show options'):
                button_name = ['Cleaned and modified', 'Not cleaned']
                button = st.radio(' ', button_name)
                if button == 'Cleaned and modified':
                    df1['MeanScore'] = df_dirty[['MathScore', 'ReadingScore', 'WritingScore']].mean(axis=1)
                    st.dataframe(df1.dropna())
                else:
                    st.dataframe(df)
    if selected == 'Sport affection':
        st.title('Do sport affect on studying?')

        df_for_sport = df.groupby(
            by=['WklyStudyHours', 'PracticeSport'], as_index=False
        ).agg(MathScore=('MathScore', 'mean'), ReadingScore=('ReadingScore', 'mean'),
              WritingScore=('WritingScore', 'mean'))
        st.write('##')
        left1, right1 = st.columns(2)
        with left1:
            st.write('Choose the subject')
            score_buttons = ['Math', 'Reading', 'Writing']
            buttons = st.radio(' ', score_buttons)
        with right1:
            st.write('Choose the exercise frequency')
            st.write("##")
            regularly = st.checkbox('Regularly', value=True)
            sometimes = st.checkbox('Sometimes', value=True)
            never = st.checkbox('Never', value=True)

        if not never:
            df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'never']
        if not sometimes:
            df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'sometimes']
        if not regularly:
            df_for_sport = df_for_sport.loc[df_for_sport['PracticeSport'] != 'regularly']

        if buttons == 'Math':
            st.pyplot(sport('Math').get_figure())
        elif buttons == 'Reading':
            st.pyplot(sport('Reading').get_figure())
        else:
            st.pyplot(sport('Writing').get_figure())
    if selected == 'Hypothesis check':
        st.title(
            "Let's see how parent education and their merital status"
            " as well as their gender affects on their mean score")
        violin1 = plt.figure(figsize=(30, 15))
        sns.violinplot(
            data=df1, bw_adjust=1, cut=2, linewidth=1,
            x='ParentEduc', y='MeanScore',
            hue='ParentMaritalStatus', palette=['#e0aaff', '#c77dff', '#9d4edd', '#7b2cbf']
        ).legend(bbox_to_anchor=(1.01, 0.08), loc='upper left', borderaxespad=0)
        plt.show()
        violin2 = plt.figure(figsize=(16, 9))
        sns.violinplot(
            data=df1, bw_adjust=1, cut=2,
            linewidth=1, x='ParentEduc', y='MeanScore',
            hue='Gender', palette=['#e0aaff', '#7b2cbf']
        ).legend(bbox_to_anchor=(1.01, 0.08), loc='upper left', borderaxespad=0)
        st.pyplot(violin1.get_figure())
        st.pyplot(violin2.get_figure())
        st.title('Microlead')

        st.write(
            "The first graph shows that pupils with a widowed parent are less evenly distributed than the others."
            " This is especially evident in the case of a parent with a bachelor's degree The second graph,"
            " on the other hand,"
            "indicates the same median for both sexes, and also in some places both boys and girls"
            " have a slightly unequal distribution"
        )
        st.write('---')
        # scatter______________________________________
        st.title("Next, I want to see if ethnicity as well as parent education affects test results.")
        df3 = df.loc[(df['MathScore'] >= 80) & (df['WritingScore'] >= 80) & (df['ReadingScore'] >= 80)]
        df3 = df3.sort_values(by='ReadingScore')
        df3 = df3.dropna()
        sp = px.scatter(
            df3, x='WritingScore', y='MathScore', animation_frame='ReadingScore', animation_group='EthnicGroup',
            color='ParentEduc', facet_col='EthnicGroup', size='NrSiblings',
            range_y=[70, 105], range_x=[70, 105], log_x=True, size_max=30, template='plotly_dark'
        )
        pirog = px.pie(df3, names='ParentEduc', template='plotly_dark', title="Parent's education")
        st.plotly_chart(sp, use_container_width=True)
        st.plotly_chart(pirog, use_container_width=True)
        st.title('Microlead')
        st.write(
            "it's noticeable that group A has a predominant concentration of students,"
            " most of whom have parents who graduated from college. Also, the better the score in one subject,"
            "the more likely it is to be higher in the other two.")
        st.write('---')
        # ______________________________________________________________________________________________________________
        st.title('Next thing')
        st.write(
            "The next thing is I want to see the pattern between math and writing test scores "
            "(I consider the reading test to be the easiest one that doesn't require much mental ability,"
            " so I want to compare the two more difficult exams) and also to see if the number of siblings"
            " affects the score."
        )

        fig = px.scatter(
            df3, x='WritingScore', y='MathScore', color='NrSiblings', size='NrSiblings',
            size_max=30, template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        st.title('Microlead')
        st.write(
            "This graph shows that this has no effect on the result, since at almost "
            "any point several points are overlapping,"
            " so the number of siblings has no effect on the math and writing results"
        )
        st.write('---')
        # ____________________________________________________________________________________________
        st.header('Overall')
        st.write(
            "Having analyzed this dataset I can confidently state that exercising definitely improves productivity "
            "and test results as well. I can justify it by the fact that sport disciplines a person"
            " and keeps him mentally healthy. I can also say that the parents' marital status also matters,"
            " because family is where a student spends most of his time, and if there are any problems in the family,"
            " it will affect on the results of studying. I would also like to point out that the type of lunch"
            " and the number of siblings in most cases also has no influence,"
            " but the education of the parent sometimes matters."
        )