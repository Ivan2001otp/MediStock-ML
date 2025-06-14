import pandas as pd
import numpy as np
import os
from enum import Enum

class Category(Enum):
    CUSTOM=1
    WOUND_CARE=2
    PPE=3
    SURGICAL_INSTRUMENT = 4
    INFUSION=5
    INJECTION=6


print("Preparing all mock data !")
#mock supplies
supplies_data : list[dict] = [
    {"id":1, "name":"Disposable Gloves", "category":Category.PPE},
    {"id":2, "name":"Syringes", "category":Category.INJECTION.name},
    {"id":3, "name":"Bandages", "category":Category.PPE},
    {"id":4, "name":"N95 Masks", "category":Category.PPE},
    {"id":5, "name":"IV Drips", "category":Category.INFUSION},
    {"id":6, "name":"Forceps", "category":Category.SURGICAL_INSTRUMENT.name},

]

supplies_df = pd.DataFrame(supplies_data)


# Mock Vendors
vendors_data : list[dict] = [
    {"id": 101, "name": "MediCare Direct"},
    {"id": 102, "name": "QuickSupply Medical"},
    {"id": 103, "name": "Budget Pharma Solutions"},
    {"id": 104, "name": "Apex Medical Supplies"},
    {"id": 105, "name": "Pristine Healthcare"},
    {"id": 106, "name": "Discount Med"},
    {"id": 107, "name": "Essential Medicals"},
    {"id": 108, "name": "Global Health Solutions"},
    {"id": 109, "name": "Clinic Basics"},
    {"id": 110, "name": "Safety First Supply"},
    {"id": 111, "name": "ProGuard PPE"},
    {"id": 112, "name": "Everyday Medical Gear"},
    {"id": 113, "name": "LifeSaver Pharmaceuticals"},
    {"id": 114, "name": "Rapid Infusions"},
    {"id": 115, "name": "Standard IV Solutions"},
    {"id": 116, "name": "Precision Instruments Co."},
    {"id": 117, "name": "General Surgical Tools"},
    {"id": 118, "name": "Basic Clinic Disposables"},
]

vendors_df = pd.DataFrame(vendors_data)


#mock vendor-supply prices and attributes

vendor_supply_attrs = [
  # Disposable Gloves (Supply ID 1)
    {"supply_id": 1, "vendor_id": 101, "unit_price": 450, "quality_rating": 5, "avg_delivery_days": 2},
    {"supply_id": 1, "vendor_id": 102, "unit_price": 400, "quality_rating": 4, "avg_delivery_days": 1},
    {"supply_id": 1, "vendor_id": 103, "unit_price": 380, "quality_rating": 3, "avg_delivery_days": 3},

    # Syringes (Supply ID 2)
    {"supply_id": 2, "vendor_id": 104, "unit_price": 700, "quality_rating": 4, "avg_delivery_days": 2},
    {"supply_id": 2, "vendor_id": 105, "unit_price": 780, "quality_rating": 5, "avg_delivery_days": 3},
    {"supply_id": 2, "vendor_id": 106, "unit_price": 650, "quality_rating": 3, "avg_delivery_days": 4},

    # Bandages (Supply ID 3)
    {"supply_id": 3, "vendor_id": 107, "unit_price": 120, "quality_rating": 4, "avg_delivery_days": 2},
    {"supply_id": 3, "vendor_id": 108, "unit_price": 150, "quality_rating": 5, "avg_delivery_days": 3},
    {"supply_id": 3, "vendor_id": 109, "unit_price": 100, "quality_rating": 3, "avg_delivery_days": 1},

    # N95 Masks (Supply ID 4)
    {"supply_id": 4, "vendor_id": 110, "unit_price": 600, "quality_rating": 5, "avg_delivery_days": 2},
    {"supply_id": 4, "vendor_id": 111, "unit_price": 550, "quality_rating": 4, "avg_delivery_days": 1},
    {"supply_id": 4, "vendor_id": 112, "unit_price": 480, "quality_rating": 3, "avg_delivery_days": 3},

    # IV Drips (Supply ID 5)
    {"supply_id": 5, "vendor_id": 113, "unit_price": 300, "quality_rating": 5, "avg_delivery_days": 3},
    {"supply_id": 5, "vendor_id": 114, "unit_price": 280, "quality_rating": 4, "avg_delivery_days": 2},
    {"supply_id": 5, "vendor_id": 115, "unit_price": 250, "quality_rating": 3, "avg_delivery_days": 4},

    # Forceps (Supply ID 6)
    {"supply_id": 6, "vendor_id": 116, "unit_price": 850, "quality_rating": 5, "avg_delivery_days": 3},
    {"supply_id": 6, "vendor_id": 117, "unit_price": 780, "quality_rating": 4, "avg_delivery_days": 2},
    {"supply_id": 6, "vendor_id": 118, "unit_price": 700, "quality_rating": 3, "avg_delivery_days": 4},

]

vendor_supply_attrs_df = pd.DataFrame(vendor_supply_attrs)


# we can increase this if needed
num_orders : int = 500

historical_orders = []

print("generating...")
for _ in range(num_orders) :
    # randomly pick a supply vendor combination
    supply_vendor_choice:dict = vendor_supply_attrs_df.sample(1).iloc[0]

    supply_id:int = supply_vendor_choice['supply_id']
    vendor_id:int = supply_vendor_choice['vendor_id']
    unit_price:float = supply_vendor_choice['unit_price']
    quality_rating:float = supply_vendor_choice['quality_rating']
    avg_delivery_days:int = supply_vendor_choice['avg_delivery_days']


    #introducing some realism and noise for actual price and delivery
    actual_price:float = np.round(unit_price * np.random.uniform(0.95, 1.05), 2) # +/- 5%
    actual_delivery_days : int = max(1, round(avg_delivery_days + np.random.uniform(-1,1))) # +/- 1day

    # this is simplified logic
    normalized_price_score = 1-(actual_price / vendor_supply_attrs_df['unit_price'].max())
    normalized_delivery_score = 1 - (actual_delivery_days / vendor_supply_attrs_df['avg_delivery_days'].max())

    # Linear combination
    # weights : quality, price, delivery time
    outcome_score:float = (quality_rating/5)*0.5 + \
                            normalized_price_score * 0.3 + \
                            normalized_delivery_score*0.2
    
    # Adding noise to outcome to make it less deterministic
    outcome_score:float = np.clip(outcome_score + np.random.uniform((-0.1, 0.1), 0.1))

    historical_orders.append({
        'supply_id': supply_id,
        'vendor_id': vendor_id,
        'unit_price': unit_price, # The base price from vendor_supply_prices
        'quality_rating': quality_rating,
        'avg_delivery_days': avg_delivery_days,
        'actual_price_paid': actual_price,
        'actual_delivery_days': actual_delivery_days,
        'outcome_score': outcome_score # This is our ML target
    })


historical_df = pd.DataFrame(historical_orders)

#mergine supplay and vendor names for better readablity
historical_df = historical_df.merge(supplies_df[['id', 'name']], left_on='supply_id',right_on='id',suffixes=('', '_supply'))
historical_df = historical_df.rename(columns={'name':'supply_name'})

historical_df = historical_df.merge(vendors_df[['id', 'name']], left_on='vendor_id', right_on='id', suffixes=('', '_vendor'))
historical_df = historical_df.rename(columns={'name': 'vendor_name'})
historical_df = historical_df.drop(columns=['vendor_id']) 
historical_df = historical_df.drop(columns=['supply_id'])


#Reorder columns for clarity
historical_df = historical_df[[
     'supply_name',  'vendor_name',
    'unit_price', 'quality_rating', 'avg_delivery_days',
    'actual_price_paid', 'actual_delivery_days', 'outcome_score'
]]


# save to csv
output_dir:str = "./data"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'mock_historical_orders.csv')
historical_df.to_csv(output_path, index=False)

print(f"Generated {num_orders} mock historical orders and saved to {output_path}")
print(historical_df.head())
print(f"\nOutcome score distribution:\n{historical_df['outcome_score'].describe()}")
