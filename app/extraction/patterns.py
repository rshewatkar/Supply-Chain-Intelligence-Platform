"""
patterns.py

Centralized dictionaries and regex patterns used by the
entity extraction module.

These values are based on the companies currently included
in metadata.csv.
"""

import re

# ==========================================================
# Entity Types
# ==========================================================

ENTITY_TYPES = [
    "COMPANY",
    "SUPPLIER",
    "CUSTOMER",
    "PRODUCT",
    "COUNTRY",
    "INDUSTRY",
    "LOCATION",
    "PERSON",
    "ORGANIZATION",
    "TECHNOLOGY",
]

# ==========================================================
# Companies
# ==========================================================

COMPANIES = {
    "AMD",
    "Apple",
    "Broadcom",
    "Flex",
    "Foxconn",
    "Intel",
    "Jabil",
    "NVIDIA",
    "Qualcomm",
    "TSMC",
}

# ==========================================================
# Suppliers
#
# Initial supply-chain mapping for this dataset.
# This list can grow as additional suppliers are identified.
# ==========================================================

SUPPLIERS = {
    "Foxconn",
    "Flex",
    "Jabil",
    "TSMC",
}

# ==========================================================
# Customers
#
# Empty for now.
# Customer relationships will be extracted later from
# the documents themselves.
# ==========================================================

CUSTOMERS = set()

# ==========================================================
# Products
#
# Initial product dictionary.
# This will expand as more products are discovered.
# ==========================================================

PRODUCTS = {
    "EPYC",
    "iPhone",
    "GeForce",
    "H100",
    "Instinct",
    "MI300",
    "Ryzen",
    "Snapdragon",
    "Tensor Core",
    "Xeon",
}

# ==========================================================
# Countries
# ==========================================================

COUNTRIES = {
    "Singapore",
    "Taiwan",
    "USA",
}

# ==========================================================
# Industries
# ==========================================================

INDUSTRIES = {
    "Consumer Electronics",
    "Electronics Manufacturing",
    "Semiconductor",
    "Semiconductor Foundry",
}

# ==========================================================
# Technologies
#
# These are common AI and semiconductor technologies
# likely to appear across the documents.
# ==========================================================

TECHNOLOGIES = {
    "AI",
    "CUDA",
    "Deep Learning",
    "GPU",
    "LLM",
    "Machine Learning",
    "NLP",
    "RAG",
}

# ==========================================================
# Regular Expressions
# ==========================================================

YEAR_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}\b"
)

MONEY_PATTERN = re.compile(
    r"\$\s?\d+(?:,\d{3})*(?:\.\d+)?"
)

PERCENT_PATTERN = re.compile(
    r"\d+(?:\.\d+)?%"
)

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

URL_PATTERN = re.compile(
    r"https?://\S+"
)

# ==========================================================
# Relationship Keywords
#
# These will be used later by relationship_extractor.py.
# ==========================================================

RELATIONSHIP_KEYWORDS = {
    "SUPPLIED_BY": [
        "supplier",
        "supplied by",
        "manufactured by",
        "fabricated by",
    ],
    "CUSTOMER_OF": [
        "customer",
        "purchased by",
        "sold to",
    ],
    "PARTNERS_WITH": [
        "partner",
        "partnership",
        "collaboration",
    ],
    "OPERATES_IN": [
        "located in",
        "headquartered in",
        "operates in",
    ],
    "PRODUCES": [
        "manufactures",
        "develops",
        "produces",
        "designs",
    ],
}