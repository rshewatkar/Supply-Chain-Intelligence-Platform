"""
Relationship patterns used by the rule-based
relationship extractor.

Each relationship type is associated with a list
of keywords or phrases that indicate the
relationship in text.
"""

# ==========================================================
# Company Relationships
# ==========================================================

PARTNERS_WITH = [
    "partners with",
    "partnered with",
    "partnership with",
    "collaborates with",
    "collaborated with",
    "works with",
    "jointly developed",
]

SUPPLIES_TO = [
    "supplies",
    "supplied",
    "supplier to",
    "delivers to",
    "provides products to",
]

CUSTOMER_OF = [
    "customer",
    "customers",
    "purchased from",
    "purchases from",
    "buys from",
]

COMPETES_WITH = [
    "competes with",
    "competitor",
    "competition",
    "rival",
]

ACQUIRES = [
    "acquired",
    "acquires",
    "acquisition of",
    "purchased",
]

INVESTS_IN = [
    "invested in",
    "investment in",
    "invests in",
]

# ==========================================================
# Product Relationships
# ==========================================================

DEVELOPS = [
    "develops",
    "developed",
    "developing",
    "designed",
    "designs",
    "creates",
    "created",
]

MANUFACTURES = [
    "manufactures",
    "manufactured",
    "manufacturing",
    "produces",
    "produced",
    "production of",
]

USES = [
    "uses",
    "used",
    "using",
    "utilizes",
    "powered by",
    "based on",
]

SUPPORTS = [
    "supports",
    "supported",
    "compatible with",
]

# ==========================================================
# Geographic Relationships
# ==========================================================

LOCATED_IN = [
    "located in",
    "headquartered in",
    "based in",
    "operates in",
    "operating in",
]

OPERATES_IN = [
    "operates in",
    "serves",
    "markets",
    "ships to",
    "exports to",
]

# ==========================================================
# Industry Relationships
# ==========================================================

BELONGS_TO = [
    "belongs to",
    "part of",
    "member of",
]

OPERATES_INDUSTRY = [
    "semiconductor industry",
    "technology industry",
    "electronics industry",
]

# ==========================================================
# Technology Relationships
# ==========================================================

POWERED_BY = [
    "powered by",
    "powered using",
    "built on",
]

ENABLES = [
    "enables",
    "enabled",
    "allows",
    "facilitates",
]

# ==========================================================
# Master Dictionary
# ==========================================================

RELATIONSHIP_PATTERNS = {
    "PARTNERS_WITH": PARTNERS_WITH,
    "SUPPLIES_TO": SUPPLIES_TO,
    "CUSTOMER_OF": CUSTOMER_OF,
    "COMPETES_WITH": COMPETES_WITH,
    "ACQUIRES": ACQUIRES,
    "INVESTS_IN": INVESTS_IN,
    "DEVELOPS": DEVELOPS,
    "MANUFACTURES": MANUFACTURES,
    "USES": USES,
    "SUPPORTS": SUPPORTS,
    "LOCATED_IN": LOCATED_IN,
    "OPERATES_IN": OPERATES_IN,
    "BELONGS_TO": BELONGS_TO,
    "OPERATES_INDUSTRY": OPERATES_INDUSTRY,
    "POWERED_BY": POWERED_BY,
    "ENABLES": ENABLES,
}