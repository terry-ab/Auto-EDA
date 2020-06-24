import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(rc={'figure.figsize':(11.7,8.27)})
st.title("Exploratory Data Analysis")
st.warning("Note: This is just a prototype to explain EDA.")

data=st.file_uploader("Upload a file or Dataset...(limit=200MB)",type=["csv","text"])

def files(data):
    if data is not None:
        df=pd.read_csv(data)
        st.dataframe(df.head())
        if st.checkbox("Show Shape"):
            st.write(df.shape)
        if st.checkbox("Show Columns"):
            st.write(df.columns)
        if st.checkbox("Show Full dataframe"):
            pd.set_option("display.max_rows", None, "display.max_columns", None)
            st.write(df)
        if st.checkbox("Show Statistics"):
            st.write(df.describe())
        if st.checkbox("Show Selected Columns"):
            mult_col=st.multiselect("Select Columns",df.columns)
            cols=df[mult_col]
            st.write(cols)
        if st.checkbox("Show Count of Unique values"):
            st.write(df.nunique().to_frame('counts'))
        if st.checkbox("Show Value Counts"):
            option=st.selectbox("Select Columns",df.columns)
            for i in df.columns:
                if i==option:
                    st.write(df[i].value_counts().rename_axis('unique values').to_frame('counts'))
        if st.checkbox("Check Null values"):
            st.write(df.isnull().sum())
            var=["Numerical","Categorical"]
            st.info("Handle Missing values")
            select=st.selectbox("Select Varaibles",var)
            if var[0]==select:
                    opt=st.radio("Fill with ",("Mean","Median"))
                    if opt=="Mean":
                        st.write(df.fillna(df.mean))
                    else:
                        st.write(df.fillna(df.median))
            else:
                    opt=st.radio("Fill with ",("Most common class","Unknown variable"))
                    if opt=="Most common class":
                        st.write(df.apply(lambda x : x.fillna(x.value_counts().index[0])))
                    else:
                        text=st.text_input("Enter a variable or text to fill")
                        st.write(df.fillna(text))
        if st.checkbox("Correlation Plot"):
            st.write(sns.heatmap(df.corr(),annot=True))
            st.pyplot()

        st.subheader("Plots")

        def plots(df):
            type_of_plot = st.selectbox("Select Type of Plot",["Area","Bar","Line","Hist","Box"])
            selected_columns_names = st.multiselect("Select Columns To Plot",df.columns)
            if st.button("Plot"):
                st.success("Plotted {} plot for {}".format(type_of_plot,selected_columns_names))
                if type_of_plot == 'Area':
                    cust_data = df[selected_columns_names]
                    st.area_chart(cust_data)

                elif type_of_plot == 'Bar':
                    cust_data = df[selected_columns_names]
                    st.bar_chart(cust_data)

                elif type_of_plot == 'Line':
                    cust_data = df[selected_columns_names]
                    st.line_chart(cust_data)

                elif type_of_plot:
                    cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
                    st.write(cust_plot)
                    st.pyplot()

            st.markdown("#### Relationship")
            plot_type = st.selectbox("Select Type of Plot",["Count","Box","Violin","Swarm"])
            column1 = st.selectbox("Select the x axis",df.columns)
            column2 = st.selectbox("Select the y axis",df.columns)
            if st.button("Generate Plot"):
                st.success("Plotted {} plot".format(type_of_plot))
                if plot_type == "Count":
                    st.warning("Note: You dont need to select y axis for this plot")
                    st.write(sns.countplot(data=df,x=column1))
                    st.pyplot()
                elif plot_type == "Box":
                    st.write(sns.boxplot(data=df,x=column1,y=column2))
                    st.pyplot()
                elif plot_type == "Violin":
                    st.write(sns.violinplot(data=df,x=column1,y=column2))
                    st.pyplot()
                else:
                    st.write(sns.swarmplot(data=df,x=column1,y=column2))
                    st.pyplot()
        plots(df)

df=files(data)
