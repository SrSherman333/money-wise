"""
Table format.

Specific template or format for the data in the Categories and Transactions tables

- dataclasses: To create simple classes that automatically locate the data
"""

from dataclasses import dataclass

@dataclass
class Category:
    """
    Class with the format for the data in the Categories table
    """
    
    category_name: str = ""
    category_type: str = ""
    
@dataclass
class Transaction:
    """
    Class with the format for the data in the Transactions tables
    """
    
    date: str = ""
    concept: str = ""
    amount: float = 0.0
    category_id: str = ""