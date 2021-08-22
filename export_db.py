import psycopg2

def get_data():
    myConnection = psycopg2.connect(
        host="localhost",
        database="cellline",
        user="postgres",
        password="postgres",
        port=5432)
    cur = myConnection.cursor()
    cur.execute('SELECT "no", "product_category", "organism", "age", "gender", "ethnicity", "biopsy_site", "tissue", "cancer_type", "growth_properties", "stock", "img" FROM public.cellline')
    cellline_data = cur.fetchall()
    cur.close
    myConnection.close
    return cellline_data