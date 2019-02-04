
# coding: utf-8

# In[1]:


import relative_kinase

p1, p2, data=relative_kinase.relative_kinase_activity("az20_500.tsv", 1.0, 0.05, 1, "AZ20")



# In[2]:


data


# In[3]:


from bokeh.plotting import show
show(p1)


# In[4]:


show(p2)

