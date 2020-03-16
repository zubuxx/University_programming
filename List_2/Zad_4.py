import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
class Statistics():
    '''
    Object that generates and stores statistics of changes in selected directory.
    It can also generate a plot of changes.

    '''

    def __init__(self, file_path):
        '''



        :param file_path: str
        ---------------------
        Path to Directory or file we want to get statistics.
        '''
        self.path = file_path
        self.df = None
        self.occurring = None

    def get_statistics(self):
        """
        Retruns Statictics of all file contained in the folder passsed as 'file_path' in Pandas DataFrame format.





        :return: DataFrame object
        ---------------------
        returns Statistics as DataFrame object
        """
        if self.df is not None:
            return self.df
        name = []
        formats = []
        creation_time = []
        paths = []
        modfication_time = []
        for path, dirs, files in os.walk(self.path):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            name.append(path.split('/')[-1])
            formats.append('Directory')
            paths.append(path)
            modfication_time.append(datetime.fromtimestamp(os.path.getmtime(path)).date())
            creation_time.append(datetime.fromtimestamp(os.stat(path).st_birthtime).date())
            for file in files:
                name.append(file)
                modfication_time.append(datetime.fromtimestamp(os.path.getmtime(path + '/' + file)).date())
                formats.append(os.path.splitext(file)[1][1:])
                paths.append(path + '/' + file)
                creation_time.append(datetime.fromtimestamp(os.stat(path + '/' + file).st_birthtime).date())
        data = {'fileName': name, 'fileFormat':formats, 'creationTime': creation_time, 'lastModificationTime': modfication_time, 'paths': paths}
        self.df = pd.DataFrame(data)
        totalCreationsThatDay = []
        totalModificationsThatDay = []
        for row in self.df.iterrows():
            totalModificationsThatDay.append(self.df[self.df['lastModificationTime'] == row[1][3]]['lastModificationTime'].count())
            totalCreationsThatDay.append(self.df[self.df['creationTime'] == row[1][2]]['creationTime'].count())

        self.df['totalCreations'] = totalCreationsThatDay
        self.df['totalModifications'] = totalModificationsThatDay
        return self.df

    def save_stats(self, name: str=datetime.now().strftime("%Y-%m-%d %H:%M")):
        '''
        Saves statistics in the same directory, where the selected file was in csv format.
        Name of new file can be passed as a 'name' paramter. (Current date by default)


        :param name: str
        ---------------------
        Name of csv file with statistics.
        :return:
        '''


        if self.df is None:
            self.get_statistics()
        if len(os.path.dirname(self.path))>0:
            name = '/' + name
        self.df.to_csv(os.path.dirname(self.path) + name + '.csv')

    def changesThatDay(self, year = datetime.now().year):
        '''
        Generates Pandas DataFrame object with statistics of changes each day.
        :param year: int
        ---------------------
        From which year we want to get statistics.
        :return: Pandas DataFrame
        ---------------------
        Retruns object with all needed statistics to generate plot.
        '''

        if self.df is None:
            self.get_statistics()
        unique_dates = list(set(list(self.df['creationTime'])+list(self.df['lastModificationTime'])))
        dates=[]
        creat=[]
        modif = []
        for date in unique_dates:
            dates.append(date)
            if not self.df[self.df['creationTime']==date].empty:
                creat.append(self.df[self.df['creationTime'] == date].iat[0, 5])
            else:
                creat.append(0)

            if not self.df[self.df['lastModificationTime']==date].empty:
                modif.append(self.df[self.df['lastModificationTime'] == date].iat[0, 6])
            else:
                modif.append(0)
        occrs = {'Date': dates, 'Creations_that_day': creat, 'Modifications_that_day': modif}
        self.occurring = pd.DataFrame(occrs)
        self.occurring.sort_values(by=['Date'], inplace=True)
        self.occurring['Total_changes'] = self.occurring['Creations_that_day'] + self.occurring['Modifications_that_day']
        self.occurring = self.occurring[self.occurring['Date'].apply(lambda x: x.year == year)]
        return self.occurring
    def hist_plot(self, year = datetime.now().year):
        if self.df is None:
            self.get_statistics()
        mod_dates = self.df['creationTime'].append(self.df['lastModificationTime'])
        mod_dates = mod_dates[mod_dates.apply(lambda x: x.year == year)]
        mod_dates = mod_dates.apply(lambda x: x.month)
        plt.hist(mod_dates)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.xticks(range(1,13), months)
        plt.title('Monthly histogram')
        plt.xlabel('Month')
        plt.ylabel('Amount of changes')
        plt.show()



    def daily_plot(self, year = datetime.now().year):
        '''
        Generates plot of changes in the directory passed as file_path in selected year.
        (current year by default)
        :param year: int
        ---------------------
        From which year we want to visualize data.

        :return:
        '''
        if self.occurring is None:
            self.changesThatDay(year)
        plt.plot(self.occurring['Date'], self.occurring['Creations_that_day'], label='Number of crated files')
        plt.plot(self.occurring['Date'], self.occurring['Modifications_that_day'], label = 'Number of modifications')
        plt.plot(self.occurring['Date'], self.occurring['Total_changes'], label = 'Number of all changes')
        plt.xlim(self.occurring['Date'].iloc[0], self.occurring['Date'].iloc[-1])
        ticksx = self.occurring['Date'].apply(lambda x: x.strftime('%d.%m'))
        plt.xticks(self.occurring['Date'], ticksx)
        plt.ylim(0, max(self.occurring['Total_changes'].max(), self.occurring['Creations_that_day'].max(), self.occurring['Modifications_that_day'].max()))
        plt.xlabel('Date')
        plt.ylabel('Changes made that day')
        plt.title('Daily plot of changes')
        plt.legend()
        plt.show()






