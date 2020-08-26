from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def my_custom_sql(querie):
    with connection.cursor() as cursor:
        cursor.execute(querie)
        return dictfetchall(cursor)

def dashClients():
    querie = """
            SELECT a.client_id,
            a.categorie_id,
            b.name client,
            c.name category,
            (SELECT interno.status

            FROM dashboard_clientbackup interno

            WHERE
                interno.client_id = a.id
            ORDER BY interno.solic_date DESC
            LIMIT 1
            ) status,
            (SELECT interno.solic_date

            FROM dashboard_clientbackup interno

            WHERE
                interno.client_id = a.id
            ORDER BY interno.solic_date DESC
            LIMIT 1
            ) solic_date,
            b.div_id

            FROM dashboard_clientcategoryrelation a
                    LEFT JOIN dashboard_cliente b ON b.id = a.client_id
                    LEFT JOIN dashboard_clientcategory c ON a.categorie_id = c.id


            ORDER BY b.name, c.name
            """
    with connection.cursor() as cursor:
        cursor.execute(querie)
        return dictfetchall(cursor)    