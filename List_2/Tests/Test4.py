from Zad_4 import Statistics

#Testing Statistics Module
st = Statistics('examp')
st.hist_plot()
st.save_stats('examp-stats')
st.daily_plot()
my_df = st.get_statistics()
# my_df is DataFrame that contains statistics of 'examp' file.