from utils import data_processing as dp
from utils import read_data

df = read_data.read_data_from_excel()

a = dp.prepare_offer_from(df)
