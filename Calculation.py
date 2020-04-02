# Data Handling
import pandas as pd
import numpy as np

# Disable SettingWithCopyWarning
pd.options.mode.chained_assignment = None

# Typing
from typing import Tuple


class Calculation:

    # Static properties
    column = 'quota'

    def __init__(
            self,
            fund_file: str,
            cdi_file: str,
            start_date: str,
            end_date: str
    ):
        """
        :param fund_file: path and file name to the fund data
        :param cdi_file: path and file name to the cdi data
        :param start_date: string start date to filter
        :param end_date: string end date to filter
        """

        # Class properties
        self.fund_file = fund_file
        self.cdi_file = cdi_file
        self.start_date = start_date
        self.end_date = end_date

        # Get data
        self.fund_data = self.read_fund()
        self.cdi_data = self.read_cdi()


    def __str__(self):
        return 'A finance class calculation'


    def __repr__(self):
        return f'{self.__class__.__name__}({self.fund_file}, {self.cdi_file})'


    @staticmethod
    def read_data(file: str) -> pd.DataFrame:
        """
        Read xlsx or csv file and return pandas dataframe
        :param file: string with file path and file name
        :return: pandas dataframe
        """

        # Get extension
        _, extension = file.split('.')

        # Read data according extension
        if extension == 'csv':
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)

        return data


    def read_cdi(self) -> pd.DataFrame:
        """
        This function reads and format CDI data
        :return: pandas dataframe
        """

        # Read data
        data = Calculation.read_data(self.cdi_file)

        # Rename columns
        data = data.rename(
            columns={'taxa anualizada': 'annualized_rate',
                     'variação diária': 'returns'}
        )

        # Format percentage column
        data['returns'] = data['returns'].replace('\%', '', regex=True)

        # Convert columns to float
        cols = ['returns', 'annualized_rate']
        data[cols] = data[cols].astype(float)

        # Convert date column to date format
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

        # Change scale returns
        data['returns'] = data['returns'] / 100

        # Set date column as index
        data.index = data['date']

        # Drop date column
        data = data.drop(['date'], axis=1)

        return data


    def read_fund(self) -> pd.DataFrame:
        """
        This function reads and format fund data
        :return: pandas dataframe
        """

        # Read data
        data = Calculation.read_data(self.fund_file)

        # Rename column
        data = data.rename(
            columns={'cota': 'quota', 'pl': 'net_equity', 'data': 'date'}
        )

        # Convert columns to float
        cols = ['quota', 'net_equity']
        data[cols] = data[cols].astype(float)

        # Convert date column to date format
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

        # Set date column as index
        data.index = data['date']

        # Drop date column
        data = data.drop(['date'], axis=1)

        return data


    @staticmethod
    def returns_calculation(data: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        This functions adds the return column
        :param data: pandas dataframe with quota and date values
        :param column: column to calculate the returns
        :return:  pandas dataframe with return column add
        """

        # Add returns column
        data['returns'] = data[column].pct_change()

        # Drop Na values (usually) the first value in the dataframe
        data = data.dropna()

        return data


    def calculate_min_max_returns(self) -> Tuple[float, float, float, float]:
        """
        This function returns the date and value of the min and max returns in a
        selected period
        :return: max, min values and the dates
        """

        # Return calculation
        data = Calculation.returns_calculation(
            self.fund_data, self.__class__.column)

        # Filter data
        data = data[self.start_date:self.end_date]

        # Reset Index
        data = data.reset_index()

        # Minimum value
        min_value = data['returns'].min()

        # Max value
        max_value = data['returns'].max()

        # Get min date
        min_date = data.loc[data['returns'] == min_value, 'date']

        # Get max date
        max_date = data.loc[data['returns'] == max_value, 'date']

        # Format value
        min_value = min_value * 100
        max_value = max_value * 100

        # Format dates
        min_date = min_date.to_list()[0].strftime('%Y-%m-%d')
        max_date = max_date.to_list()[0].strftime('%Y-%m-%d')

        return min_value, min_date, max_value, max_date

    @staticmethod
    def cumulative_returns(
            start_date: str,
            end_date: str,
            data: pd.DataFrame) -> pd.DataFrame:
        """
        This function returns a series with the cumulative returns

        :param data: dataframe with the fund data
        :param start_date: string start date to filter
        :param end_date: string end date to filter
        :return: dataframe with cumulative series
        """

        # Filter data
        data = data[start_date:end_date]

        # Calculate cumulative returns
        data['cumulative_ret'] = np.cumprod(1 + data['returns']) - 1

        # Mulitply by 100 to change the scale
        data['cumulative_ret'] = data['cumulative_ret'] * 100

        # Reset index
        data = data.reset_index()

        return data[['date', 'cumulative_ret']]


    def calculate_cumulative_returns_value(self) -> float:
        """
        This function calculates the cumulative returns of the fund
        :return: float
        """

        # Return calculation
        data = Calculation.returns_calculation(
            self.fund_data, self.__class__.column)

        data = Calculation.cumulative_returns(
            self.start_date, self.end_date, data
        )

        return data.iloc[-1, -1]


    def calculate_cumulative_returns_table(self) -> float:
        """
        This function calculates the cumulative returns of the fund
        :return: dict
        """

        # Return calculation
        data = Calculation.returns_calculation(
            self.fund_data, self.__class__.column)

        data = Calculation.cumulative_returns(
            self.start_date, self.end_date, data
        )

        # rename columns
        data.columns = ['Data', 'Retorno Acumulado']

        return data


    def calculate_relative_return(self) -> float:
        """
        This function calculate the relative return of the fund using cdi as
        reference
        :return: float number with the
        """

        # Caculate return
        cdi = Calculation.cumulative_returns(
            self.start_date,self.end_date, self.cdi_data
        )

        # Return calculation
        fund = Calculation.returns_calculation(
            self.fund_data, self.__class__.column)

        fund = Calculation.cumulative_returns(
            self.start_date,self.end_date, fund
        )

        # Last value of each cumulative returns
        cdi = cdi.iloc[-1, 1]
        fund = fund.iloc[-1, 1]

        # calculate relative return
        ret = (fund / cdi) * 100

        return ret


    def calculate_net_equity(self) -> float:
        """
        This function calculates the net equity growth in the specified period
        :return: float number with the net equity growth
        """

        # Fund data
        data = self.fund_data

        # Add reference column
        data['reference'] = range(data.shape[0])

        # Get reference, since it's necessary to get the value before the
        # start_date this reference works as reference for the row before the
        # start_date
        reference = data.loc[self.start_date:self.end_date, 'reference'][0]-1

        # Net equity values
        start_value = data.loc[data['reference'] == reference, 'net_equity']
        end_value = data.loc[self.end_date:self.end_date, 'net_equity']

        # Calculate net equity for the period
        net_equity = end_value.values[0] - start_value.values[0]

        return net_equity


    def check_date(self) -> bool:
        """
        This functions check if the start_date received is greater than end_date
        :return: true if start_date is greater than end_date
        """

        # Convert dates to datetime obj
        start_date = pd.to_datetime(self.start_date, format='%Y-%m-%d')
        end_date = pd.to_datetime(self.end_date, format='%Y-%m-%d')

        return start_date >= end_date