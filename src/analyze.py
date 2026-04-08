import json 
import pandas as pd
from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection
from src.functional_utils import filter_sales_by_category, filter_sales_by_client, total_amount

def generate_report():
    # LECTURA DE DATOS
    with open("data/clients.json", "r") as f:
        clients_data = json.load(f)
    
    sales_df = pd.read_csv("data/sales.csv")
    
    # CREAR OBJETOS
    clients = [Client(**c) for c in clients_data]
    sales = [Sale(
        row["sale_id"],
        row["client_id"],
        row["product"],
        row["category"],
        row["amount"],
        row["date"]
    ) for _, row in sales_df.iterrows()]
    
    client_col = ClientCollection(clients)
    sales_col = SalesCollection(sales)
    
    # 1: NUMERO TOTAL DE CLIENTES
    total_clients = len(clients)
    
    # 2: NUMERO TOTAL DE VENTAS
    total_sales = len(sales)
    
    # TOTAL DE INGRESOS (para el summary)
    total_revenue = round(total_amount(sales), 2)
    
    
    # 3: TOTAL DE INGRESOS POR CLIENTE
    # 4: NUMERO DE VENTAS POR CLIENTE
    # 5: INGRESO PROMEDIO POR VENTA DE CADA CLIENTE
    # 8: CLIENTE CON MAS VENTAS EN UNA CATEGORIA ESPECIFICA
    clients_report = []
    for c in clients:
        client_sales = filter_sales_by_client(sales, c.client_id)
        total_spent = round(total_amount(client_sales), 2)
        sale_count = len(client_sales)
        average_sale = round(total_spent / sale_count, 2) if sale_count > 0 else 0
        
        clients_report.append({
            "client_id": c.client_id,
            "name": c.name,
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale
        })
        
    # 6: CLIENTE CON MAYOR GASTO POR PAIS
    top_client_by_country = {}
    countries = set(c.country for c in clients)
    for country in countries:
        clients_in_country = client_col.clients_by_country(country)
        top = max(clients_in_country, key=lambda c: sales_col.total_amount_by_client(c.client_id))
        top_client_by_country[country] = top.name 
    
    
    # 7: TOTAL DE VENTAS POR CATEGORIA
    sales_by_category = sales_df.groupby("category")["amount"].sum().round(2).to_dict()
    
    
    # 9: NUMERO DE CLIENTES QUE SUPERAN GASTO DE 500€
    high_spending_clients = [
        c.name for c in clients
        if sales_col.total_amount_by_client(c.client_id) > 500
    ]
    
    # 10: VENTAS ACUMULADAS POR MES
    sales_df["date"] = pd.to_datetime(sales_df["date"])
    sales_df["month"] = sales_df["date"].dt.to_period("M").astype(str)
    monthly_sales = sales_df.groupby("month")["amount"].sum().round(2).to_dict()
    
    return {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": total_revenue
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }