import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide", initial_sidebar_state="expanded")


st.title('Dining Data Dashboard: Stars, Categories, and More')
st.write('IE 6600 Project 2 *by Bella Jen*')
         
data = pd.read_csv("/Users/bella/Downloads/cleaned_full_data.csv", encoding="ISO-8859-1")

st.sidebar.header("Filter")
option = data['city'].unique()
option = np.insert(option, 0, 'All') 
selected_category = st.sidebar.selectbox("Select city", options = option)

if selected_category != 'All':
    filtered_data = data[data['city'] == selected_category]
else: 
    filtered_data = data



# # Matplorlib histogram
# st.write("#### Distribution of Restaurant Stars by City")
# fig, ax = plt.subplots()
# ax.hist(filtered_data['star'], bins=30, color="orange", edgecolor = "black")
# ax.set_xlabel("Star")
# ax.set_ylabel ("Frequency")
# st.pyplot(fig) ### use streamlit to display the pyplot object


# # Seaborn density plot 
# st.write('#### Distribution of Restaurant Stars by City')
# fig, ax = plt.subplots()
# fig = sns.displot(filtered_data['star'], color="black", kind='kde', ax=ax, fill=True)
# ax.set_xlabel("Value")
# ax.set_ylabel("Density")
# st.pyplot(fig)

# # Altair scatter plot
# st.write('### Altair Scatter Plot')
# scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
#     x=alt.X('category_1', title='category_1'),
#     y=alt.Y('num_reviews', title='num_reviews'),
#     color=alt.Color('price_range', scale=alt.Scale(scheme='tableau10')),
#     tooltip = ['price_range', 'category_1', 'num_reviews']
# ).properties(
#     width=600,
#     height=400,
#     title="Scatter Plot of Penguins Data"
# ).interactive() # Allows zooming and panning
# st.altair_chart(scatter_plot, use_container_width =True)

# Altair scatter plot
# st.write('### Relationship Between Star Rating and Number of Reviews')
# scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
#     x=alt.X('star', title='star'),
#     y=alt.Y('num_reviews', title='num_reviews'),
#     tooltip = ['star', 'num_reviews']
# ).properties(
#     width=600,
#     height=400,
#     title="Are higher-rated restaurants more likely to have a larger number of reviews?"
# ).interactive() # Allows zooming and panning
# st.altair_chart(scatter_plot, use_container_width =True)



## Plot 1
st.write("#### Are higher-rated restaurants more likely to have a larger number of reviews?")
st.write('*Hypothesis:* Popular restaurants with better reviews may accumulate more feedback.')
scatter_plot = alt.Chart(filtered_data).mark_circle().encode(
    x=alt.X('star', title='star', scale=alt.Scale(domain=[3, 5])), 
    y=alt.Y('num_reviews', title='num_reviews', scale=alt.Scale(domain=[0, 15000])),  
    tooltip = ['star', 'num_reviews']
).properties(
    width=600,
    height=400
).interactive()  

st.altair_chart(scatter_plot, use_container_width=True)
st.write('''
*Outcome:* Based on the plot, we can see that restaurants with ratings around 4.5 stars typically have the highest number of reviews, 
while both lower-rated (below 3.5 stars) and higher-rated restaurants tend to receive fewer reviews. 
Specifically, restaurants with ratings lower than 3.5 stars usually receive the same low number of reviews as those with top ratings. 
This pattern suggests that restaurants at both extremes of the rating scale may struggle to attract reviews. 
For lower-rated restaurants, customers might be less motivated to leave reviews due to poor experiences, 
while top-rated restaurants may have fewer reviews because their reputation precedes them, 
and customers may feel less compelled to add feedback. 
In contrast, restaurants with moderate ratings (around 4.5 stars) may strike a balance between quality and popularity, 
encouraging more customers to leave reviews. 
This suggests that review volume is influenced not just by the rating itself, but also by customer perceptions, 
expectations, and the restaurant's standing in the market.
''')
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")



## Plot 2
# Apply filter otherwise the plot gets squeezed to aside
plot2 = filtered_data[(filtered_data['star'] >= 3) & (filtered_data['star'] <= 5)] 
plot2 = plot2.dropna(subset=['price_range', 'star'])
plot2 = plot2[['price_range', 'star']]

st.write("#### Do restaurants with a higher price range tend to receive higher or lower ratings?")
st.write('*Hypothesis:* High-end restaurants may offer better service or food, leading to higher ratings.')

boxplot = alt.Chart(plot2).mark_boxplot(size=30).encode(
    x=alt.X(
        'star:Q',
        title='Star Rating',
        scale=alt.Scale(domain=[3, 5]),  
        axis=alt.Axis(labelAngle=0)  
    ),
    y=alt.Y(
        'price_range:N',
        title='Price Range',
        sort=['$', '$$', '$$$', '$$$$']  
    ),
    color=alt.Color('price_range:N', legend=None)
).properties(
    title="Impact of Price Range on Star Ratings",
    width=800,  
    height=400  
).configure_axis(
    labelFontSize=10,
    titleFontSize=14
).configure_title(
    fontSize=16
).configure_view(
    strokeOpacity=0 
)

st.altair_chart(boxplot, use_container_width=True)
st.write('''
*Outcome:* In general, restaurants with two dollar signs ($$) tend to have the highest ratings. 
         On the other hand, high-end restaurants with three or four dollar signs ($$$, $$$$) show a decreasing trend in their 
         ratings. One possible explanation for this is that customers have higher expectations for these 
         more expensive restaurants, and when the experience does not meet those expectations, they are more likely 
         to leave lower ratings as a way to warn others.
''')
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")


### plot 3    
st.write("#### Do certain types of cuisines have higher or lower ratings compared to others?")
st.write('*Hypothesis:* Popular or more sophisticated cuisines (e.g., French, Japanese) may receive higher ratings.')


plot3 = filtered_data.dropna(subset=['cuisine', 'star', 'num_reviews'])
plot3 = plot3[['cuisine', 'star', 'num_reviews']]
plot3 = plot3.groupby('cuisine', as_index=False).agg(
    mean_star=('star', 'mean'),         
    total_reviews=('num_reviews', 'sum') 
)

bar_chart = alt.Chart(plot3).mark_bar().encode(
    x=alt.X('cuisine:N', title='Cuisine Type', sort='-y', axis=alt.Axis(labelAngle=0, labelFontSize=12)),  
    y=alt.Y('mean_star:Q', title='Average Star Rating'),                                    
    color=alt.Color('cuisine:N', legend=None)                                          
)

text_stars = alt.Chart(plot3).mark_text(
    align='center',
    baseline='middle',
    dy=50, 
    fontSize=12,
    color = 'white'
).encode(
    x=alt.X('cuisine:N', sort='-y'),                 
    y=alt.Y('mean_star:Q'),  
    text=alt.Text('mean_star:Q', format='.2f')         
)

text_reviews = alt.Chart(plot3).mark_text(
    align='center',
    baseline='middle',
    dy=70, 
    fontSize=10,
    color='white'  
).encode(
    x=alt.X('cuisine:N', sort='-y'),  
    y=alt.Y('mean_star:Q'), 
    text=alt.Text('total_reviews:Q', format=',.0f')  
)

combined_chart = (bar_chart + text_stars + text_reviews).properties(
    title="Average Star Ratings and Total Reviews by Cuisine Type",
    width=600,
    height=400
).configure_axis(
    labelFontSize=10,
    titleFontSize=14
).configure_title(
    fontSize=16
)

st.altair_chart(combined_chart, use_container_width=True)


st.write('''*Outcome:* East Asian cuisine has received both the highest ratings and the most 
         reviews among various food categories. This popularity can be attributed to several factors, 
         including Canada's diverse population. Asian immigrants, who make up approximately 20% of the 
         total Canadian population, significantly contribute to the demand for East Asian food.
         Furthermore, many non-Asian customers perceive East Asian cuisine as lighter and healthier compared 
         to other types of food. This perception, coupled with the growing cultural diversity, 
         has led to a rise in the popularity of dishes such as sushi, dim sum, and pho. As a result, 
         East Asian restaurants are not only a staple for immigrants but have also become favorites among 
         the wider Canadian public.''')
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")


### plot 4
st.write("#### Are higher-priced restaurants receiving more reviews? Could this indicate popularity or perceived value?")
st.write('*Hypothesis:* Higher-priced restaurants may have a smaller but more dedicated customer base, resulting in more reviews.')

plot4 = filtered_data
plot4 = filtered_data.dropna(subset=['price_range', 'num_reviews'])
plot4 = plot4[['price_range', 'num_reviews']]


boxplot = alt.Chart(plot4).mark_boxplot(size=30).encode(
    x=alt.X(
        'num_reviews:Q',
        title='Number of Reviews (Log Scale)',
        scale=alt.Scale(type='log', base=10, domain=[1, plot4['num_reviews'].max()]),  # Logarithmic scale with base 10
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y(
        'price_range:N',
        title='Price Range'
    ),
    color=alt.Color('price_range:N', legend=None)
).properties(
    title="Impact of Price Range on Number of Reviews (Logarithmic Scale)",
    width=900,  
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
).configure_view(
    strokeOpacity=0
)

st.altair_chart(boxplot, use_container_width=True)

st.write('''*Outcome:* In most cases, restaurants with one dollar sign ($) typically receive the highest number of reviews. 
         Following them are three dollar sign ($$$) restaurants and two dollar sign ($$) restaurants. Based on the discussion above, 
         restaurants with two dollar signs tend to have the highest ratings. Notably, these restaurants receive fewer reviews on average 
         but maintain the highest ratings. This may suggest that people are more inclined to leave positive reviews after visiting these establishments.''')
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")



## Plot 5
st.write("#### What does the distribution of restaurant star ratings reveal about customer satisfaction and restaurant quality?")
st.write('''*Hypothesis:* Restaurants with higher ratings (4-5 stars) should correlate with positive customer feedback, 
         indicating a strong relationship between higher ratings and customer satisfaction.''')

plot5 = filtered_data.dropna(subset=['star']) 
plot5 = plot5.groupby('star', as_index=False).agg(
    count=('star', 'count')  
)

line_plot = alt.Chart(plot5).mark_line().encode(
    x=alt.X('star:Q', title='Star', scale=alt.Scale(domain=[3, 5])), 
    y=alt.Y('count:Q', title='Restaurant Count', scale=alt.Scale(domain=[0, plot5['count'].max()])), 
    tooltip=['star', 'count']
).properties(
    width=600,
    height=400
).interactive()  

text_labels = alt.Chart(plot5).mark_text(
    align='center',
    baseline='middle',
    dy=-10,  
    fontSize=12,
    color='black'
).encode(
    x=alt.X('star:Q'),  
    y=alt.Y('count:Q'),  
    text=alt.Text('count:Q', format=',.0f')  
)

combined_plot = (line_plot + text_labels).properties(
    title="Restaurant Count by Star Rating",
    width=600,
    height=400
)

st.altair_chart(combined_plot, use_container_width=True)


st.write('''*Outcome:* Through the plot, we can see that ratings between 4 and 4.99 have the most restaurants. 
         Therefore, it is natural to conclude that these restaurants tend to receive the highest levels of customer satisfaction and positive feedback.''')




st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write('''*Reference: https://www.kaggle.com/datasets/satoshiss/food-delivery-in-canada-door-dash?resource=download* ''')
st.write('''*https://www.quora.com/Why-do-most-people-contribute-reviews-of-restaurants-theaters-and-events* ''')
st.write('''*ChatGPT for grammar correction* ''')
