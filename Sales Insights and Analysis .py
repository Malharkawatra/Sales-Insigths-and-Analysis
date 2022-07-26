#!/usr/bin/env python
# coding: utf-8

# #                              Sales Insigths and Analysis

# # Importing necessary libraries 
# 

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import os 
#os library is used for creating a directory.


# # Merging 12 months of data into a single file
# (becasue it will be easier to do yearly analysis from 1 file instead of analysing through 12 different files)

# In[2]:


df= pd.read_csv("Sales_April_2019.csv")

df.head()


# ### Reading all files from the directory 

# In[3]:


files = [file for file in os.listdir('Sales_Data')]
for file in files:
    print (file)


# ### Merging all the csv files into a single one 
# (.concat used for merging the data) 

# In[4]:



all_months_data = pd.DataFrame()
for file in files:
    df= pd.read_csv("./Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])
        
all_months_data.head()


# In[5]:



all_months_data = pd.DataFrame()
for file in files:
    df= pd.read_csv("./Sales_Data/"+file)
    all_months_data=pd.concat([all_months_data,df])
all_months_data.to_csv("all_data.csv", index=False)


# ### Reading in updated dataframe 

# In[6]:


all_data=pd.read_csv("all_data.csv")
all_data.head()


# # Cleaning up the data 

# ### Droping the rows which contains any 'NAN' values 

# In[7]:


nan_df=all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[8]:


all_data=all_data.dropna(how='all')
all_data.head()


# ## Adding a 'Month' coloumn to check the monthly analysis,
# 
# for that we will run the below code:
# 
# all_data['month']=all_data['order date'].str[0:2]
# all_data['month']=all_data['month'].astype('int32')
# all_data.head()
# 
# Its giving error because some of rows doesn't have the order date, they are displaying order date as 'order date' , 
# so we should firstly find such rows and delete them.

# In[9]:


temp_df=all_data[all_data['Order Date'].str[0:2]=='Or']
temp_df.head()


#  As you can see these are the orders which have not any defined date , that's why when we running above code it was not able to convert the month coloumn properly into the string. 

# So now we will update the data , focusing only on the data which have a defined date.  

# In[10]:


all_data=all_data[all_data['Order Date'].str[0:2]!='Or']


# ### Adding the month coloumn 

# Taking the first two character of the date coloumn and then with the help of this will make the month coloumn.

# In[11]:


all_data['month']=all_data['Order Date'].str[0:2]
all_data['month']=all_data['month'].astype('int32') #astype used to define the type of the data 
all_data.head()


# # Best month of the sale and how much was earned in that month.

# ### Adding a sales coloumn 

# For sales column, we will multiply the price and the quantity. 

# Firstly we will convert the coloumns to the correct data types. 

# In[12]:


#Using to_numeric to convert into numeric.
all_data['Quantity Ordered']= pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each']) 


# In[13]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# #### What was the best month of the sale and how much was earned that month?

# In[14]:


all_data.groupby('month').sum() 


# We can clearly see that the december month was the best as the sales value is highest in that coloumn.

# ### Chart Representation

# In[15]:


results=all_data.groupby('month').sum() 
months=range(1,13)
plt.bar(months,results['Sales'])  
plt.xticks(months) # Using'xticks' to display every value for the month number in the chart 
plt.xlabel('Month Number ')
plt.ylabel('Sales in USD')
plt.show()


# Now from the above chart we can analyse different things for example may be due to the chirstmas, December sales are highest.

# # City with the highest number of sales.

# #### Firstly we have to add a city coloumn (we will find the city from the address coloumn we have).

# In[16]:


all_data['City']=all_data['Purchase Address'].apply(lambda x : x.split(',')[1]) 

#lamba is used when we require a nameless function for a short period of time.
#It means that x is used for the every value in the coloumn.
#x.split means we are now splitting the purchase column value and whatever value is at the 1st index place,
#we are assigning that value for the city column.


# In[17]:


#We should make a function for this for the easy access.
def get_city(address):
    return address.split(',')[1]
all_data['City']=all_data['Purchase Address'].apply(lambda x : get_city(x)) 
all_data.head()


# We will going to face issues actually with the above dataset , becasue cities can be same in the different states 
# and the different countries. 
# 
# So to solve that we will also include the state name along with city name. 

# In[18]:


def get_state(address):
    return address.split(',')[2]
all_data['City']=all_data['Purchase Address'].apply(lambda x : get_city(x)+get_state(x))
all_data.head()


# There is postal code in the city column ,we will delete it as we don't have the requirement of the postal code. 

# In[19]:


def get_state(address):
    return address.split(',')[2].split(' ')[1]
all_data['City']=all_data['Purchase Address'].apply(lambda x : get_city(x)+' ' + get_state(x))
all_data.head()


# #### What city has the highest number of sales ?

# In[20]:


results=all_data.groupby('City').sum()
results 


# As you can see,if we would not have include the state name along with the city we would have faced some problem as there some similar cities in the different states and countries , for example Portland ME and Portlnad OR.
# 
# Answer to the question - San Francisco has the highest no. of sales data.

# ### Chart Representation

# In[21]:


cities=[City for City, df in all_data.groupby('City')] 
plt.bar(cities,results['Sales']) 
plt.xticks(cities,rotation='vertical',size=8)
plt.xlabel('City Name') 
plt.ylabel('Sales in USD')
plt.show()


# # Best time to run the Advertisments.

# What time should we display advertisements to maximize likelihood of the customer's buying product ?
# We will analyse it with the help of 'Order date' column as the time of Order is also given along with the date.
# 
# But firstly we have to convert the 'Order date' column into 'Datetime' datatype.

# In[22]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data.head()


# ### Adding Hour and the Minute column. 

# In[23]:


all_data['Hour']=all_data['Order Date'].dt.hour #(.date.hour)
all_data['Minute']=all_data['Order Date'].dt.minute
all_data.head ()


# In[24]:


Hours=[Hour for Hour, df in all_data.groupby('Hour')]
all_data.groupby(['Hour']).count().head()


# ### Chart Representation

# In[25]:


Hours=[Hour for Hour, df in all_data.groupby('Hour')]

plt.plot(Hours, all_data.groupby(['Hour']).count()['Quantity Ordered'])
plt.grid()
plt.xticks(Hours)
plt.show()


# Through the chart you can clearly see that the peak times are around 11 am and 7 pm which is making sense becasue 11AM is not too early in the morning and 7PM is not too late in the night.
# So the answer according to me to make advertistments are around 11am and 7pm to generate the peak orders.

# # Products are often Sold together

# #### What are the products which are often solved togther? How we gonna know which orders are ordered together is by seeing there order id, if two different products have the  same order id then we know that they are ordered together. 

# In[26]:


df=all_data[all_data['Order ID'].duplicated( keep= False)]
df.head(20)


# As we can see that there are different products with the same order id 
# now we will group the products with the same order id togthe.

# In[27]:


df=all_data[all_data['Order ID'].duplicated( keep= False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x)) 
#join is an in-built method used to join an iterable's elements(each elements),separated by a string separator,
#which is specified by us.
df.head()


# Now we have grouped the products with the same order id, and now we will drop the duplicate rows.

# In[28]:


df=df[['Order ID','Grouped']].drop_duplicates()
df.head()


# # Products sold most and the reason for that .

# #### Which products are sold the most and what is the reason for that?

# In[29]:


all_data.head()


# In[30]:


product_group=all_data.groupby('Product')

product_group.sum()


# #### Ploting the chart to check which product is sold the most. 

# In[31]:


quantity_ordered = product_group.sum()['Quantity Ordered']
products=[product for product , df in product_group]
plt.bar(products, quantity_ordered)
plt.xticks(products,rotation='vertical',size=8)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.show()


# From the chart we can clearly see that the AAA Batteries are sold the most. 
# 
# The items which are cheap are actually sold the most (but we should have a proof of our hypothesis) so what we can do is, we will overlap this chart with the 'prices of the products' chart and will check whether our hypothesis is correct or not. 

# In[32]:


prices=all_data.groupby('Product').mean()['Price Each'] #avg price of the products sold for 
print (prices )


# Now we will add a second y axis in the upper graph 
# How to do that, (searched from Google) 
# below is the written code for that 
# '
# fig, ax1 = plt.subplots()
# 
# ax2 = ax1.twinx()
# ax1.plot(x, y1, 'g-')
# ax2.plot(x, y2, 'b-')
# 
# ax1.set_xlabel('X data')
# ax1.set_ylabel('Y1 data', color='g')
# ax2.set_ylabel('Y2 data', color='b')
# 
# plt.show()
#             '
# 

# In[33]:


prices=all_data.groupby('Product').mean()['Price Each'] 
fig, ax1=plt.subplots()


ax2 = ax1.twinx()
ax1.bar(products,quantity_ordered, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Prices', color='b')

ax1.set_xticklabels(products,rotation='vertical',size=8)
plt.show()


# From the above chart we can say that our assumption was somewhat correct because where the green graph is high 
# (means where the quantity of the product sold is high), there the blue graph (price of the product) is low and vice versa. 
# But some products like 'Macbook pro' are sold in a good quantity even it is a high priced product, this can be because
# Macbook is used by students, professionals, artists (large no of people use this product).
# 

# In[ ]:




