from typing import Union
from sqlalchemy.orm import Session
import pandas as pd

from . import models


def save_bills(df : pd.DataFrame, db : Session):
    df = __preprocess_data(df)
    bills_count = 0
    for _, row in df.iterrows():
        if __validate_row(row):
            try:
                org = db.query(models.Org).filter(models.Org.name == row['client_org']).first()
                if org is None:
                    org = models.Org(name=row['client_org'], client_name=row['client_name'])
                    db.add(org)
                    db.flush()
                bill = models.Bill(org=org, number=row['№'], sum=row['sum'], date=row['date'], services=row['service'])
                db.add(bill)
                db.commit()
                bills_count += 1
            except:
                db.rollback()
    return bills_count

def __get_bills(db : Session, org_name : Union[list[str], None], client_name : Union[list[str], None] = None):
    q = db.query(models.Bill)
    if not org_name is None:
        q = q.filter(models.Bill.org.has(models.Org.name.in_(org_name)))
    if not client_name is None:
        q = q.filter(models.Bill.org.has(models.Org.client_name.in_(client_name)))
    return q.all()

def get_bills_dto(db : Session, org_name : Union[str, None], client_name : Union[str, None] = None):
    bills = __get_bills(db, org_name, client_name)
    bills_dto = []
    for bill in bills:
        bills_dto.append({
            "client_name": bill.org.client_name,
            "client_org": bill.org.name,
            "№": bill.number,
            "sum": bill.sum,
            "date": bill.date,
            "service": bill.services
        })
    return bills_dto

def __validate_row(row: pd.Series):
    if row['client_name'] == '':
        return False
    if row['client_org'] == '':
        return False
    if row['service'] in ('', '-'):
        return False
    return True

def __preprocess_data(df: pd.DataFrame):
    df['№'] = pd.to_numeric(df['№'], errors='coerce', downcast='integer')
    df['sum'] = pd.to_numeric(df['sum'].str.replace(',', '.'), errors='coerce', downcast='float')
    df['sum'] = df['sum'].apply(lambda x: round(x, 2))
    df['client_name'] = df['client_name'].astype(str)
    df['client_org'] = df['client_org'].astype(str)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format="%d.%m.%Y")
    df['service'] = df['service'].astype(str)
    df.dropna(axis=0, how='any', inplace=True)
    return df
