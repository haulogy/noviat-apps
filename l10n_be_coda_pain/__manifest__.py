# Copyright 2009-2023 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CODA Import - ISO 20022 Payment Order Matching",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Noviat",
    "website": "https://www.noviat.com/",
    "category": "Accounting & Finance",
    "complexity": "normal",
    "summary": "CODA Import - ISO 20022 Payment Order Matching",
    "depends": ["l10n_be_coda_advanced", "account_banking_sepa_credit_transfer"],
    "data": ["views/coda_bank_account_views.xml"],
    "installable": True,
}
