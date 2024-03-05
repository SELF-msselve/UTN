from utils_db import *
engine = connect_to_db(
    'pipeline.conf', 'mysql', 'mysql+pymysql'
    )
get_metadata_db(engine)
df_customers = extract_full_data(engine, 'customers')
# Veamos los primeros registros de los datos
df_customers.head()