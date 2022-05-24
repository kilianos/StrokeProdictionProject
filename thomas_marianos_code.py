#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import Packages and Data / Connect to TWINT

import pandas as pd
import numpy as np
import os
import sys
import re
import datetime
import pprint as pp 
from matplotlib import pyplot as plt
import twint
import nest_asyncio
nest_asyncio.apply()

guns = pd.read_csv("gun-violence-data_01-2013_03-2018 2.csv", sep=',')


# In[4]:


# Clean Data - Remove Columns

del guns['incident_url']
del guns['source_url']
del guns['incident_url_fields_missing']
del guns['latitude']
del guns['location_description']
del guns['longitude']
del guns['participant_age']
del guns['participant_gender']
del guns['participant_relationship']
del guns['participant_status']
del guns['participant_type']
del guns['participant_name']
del guns['sources']
del guns['state_house_district']
del guns['state_senate_district']
del guns['congressional_district']
del guns['n_guns_involved']
del guns['notes']
del guns['participant_age_group']
del guns['address']
del guns['gun_stolen']
del guns['incident_characteristics']


# In[5]:


# Rename incident_id to id | Create year and month columns

guns = guns.rename(columns = {'incident_id':'id'})
guns['year'] = pd.DatetimeIndex(guns['date']).year
guns['month'] = pd.DatetimeIndex(guns['date']).month


# In[6]:


guns.head()


# In[7]:


# Number of incidents per year nationally

usIncidents_year = guns[['id','year']].groupby(['year']).count()
usIncidents_year


# In[8]:


# Number of injuries and deaths per year nationally

usCasualties_year = guns[['n_killed','n_injured','year']].groupby(['year']).sum()
usCasualties_year


# In[9]:


# 2013 and 2018 are at the ends of collection and skew data so drop them

guns.drop(guns.loc[guns['year'] == 2013].index, inplace = True)
guns.drop(guns.loc[guns['year'] == 2018].index, inplace = True)


# In[10]:


usIncidents_year = guns[['id','year']].groupby(['year']).count()
usIncidents_year


# In[11]:


usCasualties_year = guns[['n_killed','n_injured','year']].groupby(['year']).sum()
usCasualties_year


# In[12]:


# States with the highest number of incidents (14-17)

stateIncidents_all = guns[['id','state']].groupby(['state']).count().sort_values(['id'], ascending = False)
stateIncidents_all[:5]


# In[13]:


# States with the highest number of casualties (14-17)

state_casualities = guns[['n_killed','n_injured','state']].groupby(['state']).sum().sort_values(['n_injured'], ascending = False)
state_casualities[:5]


# In[14]:


# States with the highest number of incidents 2014

guns_14 = guns[guns['year'] == 2014]
state_14_highest = guns_14[['id','state']].groupby(['state']).count().sort_values(['id'], ascending = False)
state_14_highest[:5]


# In[15]:


# States with the highest number of incidents 2015

guns_15 = guns[guns['year'] == 2015]
state_15_highest = guns_15[['id','state']].groupby(['state']).count().sort_values(['id'], ascending = False)
state_15_highest[:5]


# In[16]:


# States with the highest number of incidents 2016

guns_16 = guns[guns['year'] == 2016]
state_16_highest = guns_16[['id','state']].groupby(['state']).count().sort_values(['id'], ascending = False)
state_16_highest[:5]


# In[17]:


# States with the highest number of incidents 2017

guns_17 = guns[guns['year'] == 2017]
state_17_highest = guns_17[['id','state']].groupby(['state']).count().sort_values(['id'], ascending = False)
state_17_highest[:5]


# In[18]:


# Illinois incident data

il_guns = guns[guns['state'] == 'Illinois']
il_guns_all = il_guns[['id','year']].groupby(['year']).count()
il_guns_all


# In[19]:


# California incident data

ca_guns = guns[guns['state'] == 'California']
ca_guns_all = ca_guns[['id','year']].groupby(['year']).count()
ca_guns_all


# In[20]:


# Texas incident data

tx_guns = guns[guns['state'] == 'Texas']
tx_guns_all = tx_guns[['id','year']].groupby(['year']).count()
tx_guns_all


# In[22]:


# Top states compared to national stats

total_us = guns[['id']].count()
total_il = il_guns[['id']].count()
total_ca = ca_guns[['id']].count()
total_tx = tx_guns[['id']].count()

print('2014 - 2017:')
print('Total Gun Incidents: ')
print('U.S. - ', total_us['id'])
print('California - ', total_ca['id'])
print('Illinois - ', total_il['id'])
print('Texas - ', total_tx['id'])
print('-----')
print('% of National Incidents: ')
print('Illinois - ', (total_il['id'] / total_us['id'])*100, "%")
print('California - ', (total_ca['id'] / total_us['id'])*100, "%")
print('Texas - ', (total_tx['id'] / total_us['id'])*100, "%")


# In[21]:


# Top cities with most incidents

cityShootings_all = guns[['id','city_or_county']].groupby(['city_or_county']).count().sort_values(['id'], ascending = False)
cityShootings_all[:5]


# In[22]:


chi_guns = il_guns[il_guns['city_or_county'] == 'Chicago']


# In[23]:


# Compare Chigaco stats to Illinois

total_il = il_guns[['id']].count()
total_chi = chi_guns[['id']].count()
print('2014 - 2017:')
print('Total Shootings:')
print('Illinois - ', total_il['id'])
print('Chicago - ', total_chi['id'])
print('-----')
print('% of State Shootings - ', (total_chi['id'] / total_il['id'])*100, "%")


# In[24]:


# Gather Top 5 cities for California

ca_cities = ca_guns[['id','city_or_county']].groupby(['city_or_county']).count().sort_values(['id'], ascending = False)
ca_cities[:5]


# In[25]:


# City data

oak_guns = ca_guns[ca_guns['city_or_county'] == 'Oakland']
total_oak = oak_guns[['id']].count()

los_guns = ca_guns[ca_guns['city_or_county'] == 'Los Angeles']
total_los = los_guns[['id']].count()

fres_guns = ca_guns[ca_guns['city_or_county'] == 'Fresno']
total_fres = fres_guns[['id']].count()

bak_guns = ca_guns[ca_guns['city_or_county'] == 'Bakersfield']
total_bak = bak_guns[['id']].count()

sto_guns = ca_guns[ca_guns['city_or_county'] == 'Stockton']
total_sto = sto_guns[['id']].count()


# In[26]:


# Compare city stats to California

print('2014 - 2017:')
print('Total Incidences: ')
print('California - ', total_ca['id'])
print('-----')
print('% of State Incidences: ')
print('Oakland - ', (total_oak['id'] / total_ca['id'])*100, "%")
print('Los Angeles - ', (total_los['id'] / total_ca['id'])*100, "%")
print('Fresno - ', (total_fres['id'] / total_ca['id'])*100, "%")
print('Bakersfield - ', (total_bak['id'] / total_ca['id'])*100, "%")
print('Stockton - ', (total_sto['id'] / total_ca['id'])*100, "%")


# In[27]:


# Gather Top 5 cities for Texas

tx_cities = tx_guns[['id','city_or_county']].groupby(['city_or_county']).count().sort_values(['id'], ascending = False)
tx_cities[:5]


# In[28]:


# City data

hou_guns = tx_guns[tx_guns['city_or_county'] == 'Houston']
total_hou = hou_guns[['id']].count()

san_guns = tx_guns[tx_guns['city_or_county'] == 'San Antonio']
total_san = san_guns[['id']].count()

dal_guns = tx_guns[tx_guns['city_or_county'] == 'Dallas']
total_dal = dal_guns[['id']].count()

cor_guns = tx_guns[tx_guns['city_or_county'] == 'Corpus Christi']
total_cor = cor_guns[['id']].count()

au_guns = tx_guns[tx_guns['city_or_county'] == 'Austin']
total_au = au_guns[['id']].count()


# In[29]:


# Compare city stats to Texas

print('2014 - 2017:')
print('Total Incidents: ')
print('Texas - ', total_tx['id'])
print('-----')
print('% of State Incidents: ')
print('Houston - ', (total_hou['id'] / total_tx['id'])*100, "%")
print('San Antonio - ', (total_san['id'] / total_tx['id'])*100, "%")
print('Dallas - ', (total_cor['id'] / total_tx['id'])*100, "%")
print('Corpus Christi - ', (total_dal['id'] / total_tx['id'])*100, "%")
print('Austin - ', (total_au['id'] / total_tx['id'])*100, "%")


# In[30]:


# All California data
ca_14 = ca_guns[ca_guns['year'] == 2014]
ca_14_mon = ca_14[['id','month']].groupby(['month']).count()

ca_15 = ca_guns[ca_guns['year'] == 2015]
ca_15_mon = ca_15[['id','month']].groupby(['month']).count()

ca_16 = ca_guns[ca_guns['year'] == 2016]
ca_16_mon = ca_16[['id','month']].groupby(['month']).count()

ca_17 = ca_guns[ca_guns['year'] == 2017]
ca_17_mon = ca_17[['id','month']].groupby(['month']).count()


# In[31]:


ca_14_mon


# In[32]:


ca_15_mon


# In[33]:


ca_16_mon


# In[34]:


ca_17_mon


# In[24]:


# Configure TWINT and pull 2014 tweets into a JSON file

c = twint.Config()
c.Search = "@JerryBrownGov"
c.Lang = "en"
c.Since = "2014-01-01"
c.Until = "2014-12-31"
c.Store_json = True
c.Output = "tweets_14.json"

twint.run.Search(c)


# In[21]:


# Load tweets into panda data frame

tweetlist_14 = pd.read_json('tweets_14.json', lines=True)


# In[22]:


# Clean data: Remove unneeded columns

del tweetlist_14['conversation_id']
del tweetlist_14['created_at']
del tweetlist_14['timezone']
del tweetlist_14['user_id']
del tweetlist_14['mentions']
del tweetlist_14['urls']
del tweetlist_14['photos']
del tweetlist_14['cashtags']
del tweetlist_14['link']
del tweetlist_14['retweet']
del tweetlist_14['quote_url']
del tweetlist_14['video']
del tweetlist_14['thumbnail']
del tweetlist_14['source']
del tweetlist_14['user_rt_id']
del tweetlist_14['user_rt']
del tweetlist_14['retweet_id']
del tweetlist_14['reply_to']
del tweetlist_14['retweet_date']
del tweetlist_14['translate']
del tweetlist_14['trans_src']
del tweetlist_14['trans_dest']
del tweetlist_14['near']
del tweetlist_14['geo']


# In[23]:


# Focus on english tweets

tweetlist_14 = tweetlist_14[tweetlist_14['language'] == 'en']

# Make tweets lowercase for analysis purposes

tweetlist_14['tweet']=tweetlist_14['tweet'].str.lower()

# Reformat and break out the date information

tweetlist_14['date'] = pd.to_datetime(tweetlist_14['date']).dt.date
tweetlist_14['year'] = pd.DatetimeIndex(tweetlist_14['date']).year
tweetlist_14['month'] = pd.DatetimeIndex(tweetlist_14['date']).month


# In[24]:


tweetlist_14.head()


# In[25]:


# Create a function to count the number of times a specific word(s) appear in the tweetlist

def wordCount(word,dataframe):
    count = 0
    total = 0
    for w in word:
        count = len(dataframe[dataframe['tweet'].str.contains(w, na=False)])
        total = total + count
    print(total)


# In[23]:


# Look at tweets by month

tweets_14_mon = tweetlist_14[['id','month']].groupby(['month']).count()
tweets_14_mon


# In[26]:


# Total tweets sampled

tweets_total_14 = tweetlist_14[['id']].count()
tweets_total_14


# In[27]:


# Number of times 'gun control' appeared in the Tweetlist

wordCount('gun control', tweetlist_14)


# In[28]:


# Number of times 'gun rights' appeared in the Tweetlist

wordCount('gun rights', tweetlist_14)


# In[29]:


# Number of times 'prop 47' appeared in the Tweetlist

wordCount('prop 47', tweetlist_14)


# In[ ]:


# Configure TWINT and pull 2015 tweets into a JSON file

c = twint.Config()
c.Search = "@JerryBrownGov"
c.Lang = "en"
c.Since = "2015-01-01 20:30:15"
c.Until = "2015-12-31 20:30:15"
c.Store_json = True
c.Output = "tweets_15.json"

twint.run.Search(c)


# In[31]:


# Load tweets into panda data frame

tweetlist_15 = pd.read_json('tweets_15.json', lines=True)


# In[32]:


# Clean data: Remove unneeded columns

del tweetlist_15['conversation_id']
del tweetlist_15['created_at']
del tweetlist_15['timezone']
del tweetlist_15['user_id']
del tweetlist_15['mentions']
del tweetlist_15['urls']
del tweetlist_15['photos']
del tweetlist_15['cashtags']
del tweetlist_15['link']
del tweetlist_15['retweet']
del tweetlist_15['quote_url']
del tweetlist_15['video']
del tweetlist_15['thumbnail']
del tweetlist_15['source']
del tweetlist_15['user_rt_id']
del tweetlist_15['user_rt']
del tweetlist_15['retweet_id']
del tweetlist_15['reply_to']
del tweetlist_15['retweet_date']
del tweetlist_15['translate']
del tweetlist_15['trans_src']
del tweetlist_15['trans_dest']
del tweetlist_15['near']
del tweetlist_15['geo']


# In[33]:


# Focus on english tweets

tweetlist_15 = tweetlist_15[tweetlist_15['language'] == 'en']

# Make tweets lowercase for analysis purposes

tweetlist_15['tweet']=tweetlist_15['tweet'].str.lower()

# Reformat and break out the date information

tweetlist_15['date'] = pd.to_datetime(tweetlist_15['date']).dt.date
tweetlist_15['year'] = pd.DatetimeIndex(tweetlist_15['date']).year
tweetlist_15['month'] = pd.DatetimeIndex(tweetlist_15['date']).month


# In[34]:


tweetlist_15.head()


# In[35]:


# Look at tweets by month

tweets_15_mon = tweetlist_15[['id','month']].groupby(['month']).count()
tweets_15_mon


# In[36]:


# Total tweets sampled

tweets_total_15 = tweetlist_15[['id']].count()
tweets_total_15


# In[37]:


# Number of times 'gun control' appeared in the Tweetlist

wordCount('gun control', tweetlist_15)


# In[38]:


# Number of times 'gun rights' appeared in the Tweetlist

wordCount('gun rights', tweetlist_15)


# In[45]:


# Number of times Firearm Saftey Certificate appeared in the Tweetlist

wordCount('firearm saftey certificate', tweetlist_15)


# In[ ]:


# Configure TWINT and pull 2016 tweets into a JSON file

c = twint.Config()
c.Search = "@JerryBrownGov"
c.Lang = "en"
c.Since = "2016-01-01 20:30:15"
c.Until = "2016-12-31 20:30:15"
c.Store_json = True
c.Output = "tweets_16.json"

twint.run.Search(c)


# In[59]:


# Load tweets into panda data frame

tweetlist_16 = pd.read_json('tweets_16.json', lines=True)


# In[60]:


# Clean data: Remove unneeded columns

del tweetlist_16['conversation_id']
del tweetlist_16['created_at']
del tweetlist_16['timezone']
del tweetlist_16['user_id']
del tweetlist_16['mentions']
del tweetlist_16['urls']
del tweetlist_16['photos']
del tweetlist_16['cashtags']
del tweetlist_16['link']
del tweetlist_16['retweet']
del tweetlist_16['quote_url']
del tweetlist_16['video']
del tweetlist_16['thumbnail']
del tweetlist_16['source']
del tweetlist_16['user_rt_id']
del tweetlist_16['user_rt']
del tweetlist_16['retweet_id']
del tweetlist_16['reply_to']
del tweetlist_16['retweet_date']
del tweetlist_16['translate']
del tweetlist_16['trans_src']
del tweetlist_16['trans_dest']
del tweetlist_16['near']
del tweetlist_16['geo']


# In[61]:


# Focus on english tweets

tweetlist_16 = tweetlist_16[tweetlist_16['language'] == 'en']

# Make tweets lowercase for analysis purposes

tweetlist_16['tweet']=tweetlist_16['tweet'].str.lower()

# Reformat and break out the date information

tweetlist_16['date'] = pd.to_datetime(tweetlist_16['date']).dt.date
tweetlist_16['year'] = pd.DatetimeIndex(tweetlist_16['date']).year
tweetlist_16['month'] = pd.DatetimeIndex(tweetlist_16['date']).month


# In[62]:


tweetlist_16.head()


# In[63]:


# Look at tweets by month

tweets_16_mon = tweetlist_16[['id','month']].groupby(['month']).count()
tweets_16_mon


# In[64]:


# Total tweets sampled

tweets_total_16 = tweetlist_16[['id']].count()
tweets_total_16


# In[65]:


# Number of times 'gun control' appeared in the Tweetlist

wordCount('gun control', tweetlist_16)


# In[66]:


# Number of times 'gun rights' appeared in the Tweetlist

wordCount('gun rights', tweetlist_16)


# In[67]:


# Number of times new bills related terms appeared in the Tweetlist

wordCount('bills', tweetlist_16)


# In[ ]:


# Configure TWINT and pull 2017 tweets into a JSON file

c = twint.Config()
c.Search = "@JerryBrownGov"
c.Lang = "en"
c.Since = "2017-01-01 20:30:15"
c.Until = "2017-12-31 20:30:15"
c.Store_json = True
c.Output = "tweets_17.json"

twint.run.Search(c)


# In[69]:


# Load tweets into panda data frame

tweetlist_17 = pd.read_json('tweets_17.json', lines=True)


# In[70]:


# Clean data: Remove unneeded columns

del tweetlist_17['conversation_id']
del tweetlist_17['created_at']
del tweetlist_17['timezone']
del tweetlist_17['user_id']
del tweetlist_17['mentions']
del tweetlist_17['urls']
del tweetlist_17['photos']
del tweetlist_17['cashtags']
del tweetlist_17['link']
del tweetlist_17['retweet']
del tweetlist_17['quote_url']
del tweetlist_17['video']
del tweetlist_17['thumbnail']
del tweetlist_17['source']
del tweetlist_17['user_rt_id']
del tweetlist_17['user_rt']
del tweetlist_17['retweet_id']
del tweetlist_17['reply_to']
del tweetlist_17['retweet_date']
del tweetlist_17['translate']
del tweetlist_17['trans_src']
del tweetlist_17['trans_dest']
del tweetlist_17['near']
del tweetlist_17['geo']


# In[71]:


# Focus on english tweets

tweetlist_17 = tweetlist_17[tweetlist_17['language'] == 'en']

# Make tweets lowercase for analysis purposes

tweetlist_17['tweet']=tweetlist_17['tweet'].str.lower()

# Reformat and break out the date information

tweetlist_17['date'] = pd.to_datetime(tweetlist_17['date']).dt.date
tweetlist_17['year'] = pd.DatetimeIndex(tweetlist_17['date']).year
tweetlist_17['month'] = pd.DatetimeIndex(tweetlist_17['date']).month


# In[72]:


tweetlist_17.head()


# In[73]:


# Look at tweets by month

tweets_17_mon = tweetlist_17[['id','month']].groupby(['month']).count()
tweets_17_mon


# In[74]:


# Total tweets sampled

tweets_total_17 = tweetlist_17[['id']].count()
tweets_total_17


# In[75]:


# Number of times 'gun control' appeared in the Tweetlist

wordCount('gun control', tweetlist_17)


# In[76]:


# Number of times 'gun rights' appeared in the Tweetlist

wordCount('gun rights', tweetlist_17)

