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
       b.name             client,
       c.name             category,
       dd.status          status,
       dd.solic_date      solic_date,
       (e.address
            || d.localizacao
            || ' : '
            || e.user
            || ' @ '
           || e.password) last_location,

       b.div_id

FROM dashboard_clientcategoryrelation a
         LEFT JOIN dashboard_cliente b ON b.id = a.client_id
         LEFT JOIN dashboard_clientcategory c ON a.categorie_id = c.id
         LEFT JOIN dashboard_clientbackup d ON a.id = d.client_id AND d.id = (
    SELECT MAX(x.id)
    FROM dashboard_clientbackup x
    WHERE
          x.client_id = a.id
      AND x.status = 'F') --- LOCAL DO ÚLTIMO BACKUP
         LEFT JOIN dashboard_backupdestination e ON d.destination_id = e.id
         LEFT JOIN dashboard_clientbackup dd ON a.id = dd.client_id AND dd.id = (
    SELECT MAX(x.id)
    FROM dashboard_clientbackup x
    WHERE
        x.client_id = a.id
)


ORDER BY b.name, c.name;
            """
    with connection.cursor() as cursor:
        cursor.execute(querie)
        return dictfetchall(cursor)    