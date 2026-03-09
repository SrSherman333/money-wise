from dataclasses import dataclass

@dataclass
class Category:
    category_name: str = ""
    category_type: str = ""
    
@dataclass
class Transaction:
    date: str = ""
    concept: str = ""
    amount: float = 0.0
    category_id: str = ""