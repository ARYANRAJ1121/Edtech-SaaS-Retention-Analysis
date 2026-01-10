# ----------------------------
# Global configuration
# ----------------------------

NUM_USERS = 1500

START_DATE = "2024-01-01"
DAYS_SPAN = 180  # signup spread across ~6 months

RANDOM_SEED = 42

# Acquisition channel distribution
ACQUISITION_CHANNELS = {
    "organic": 0.45,
    "paid_ads": 0.25,
    "referral": 0.15,
    "social": 0.15
}

# Country distribution
COUNTRIES = {
    "India": 0.60,
    "US": 0.20,
    "UK": 0.10,
    "Other": 0.10
}
