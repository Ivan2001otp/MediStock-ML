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


for _ in range(num_orders) :
    supply_vendor_choice = vendor_supply_attrs_df.sample(1).iloc[0]

    supply_id = supply_vendor_choice['supply_id']
    vendor_id = supply_vendor_choice['vendor_id']
    unit_price = supply_vendor_choice['unit_price']
    