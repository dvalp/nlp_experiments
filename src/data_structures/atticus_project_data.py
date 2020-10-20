from datetime import datetime
from typing import NamedTuple


class AtticusIndividualClause(NamedTuple):
    file_path: str = None
    clause_text: str = None
    document_name: str = None
    parties: str = None
    agreement_date: str = None
    effective_date: str = None
    expiration_date: str = None
    renewal_term: str = None
    termination_term: str = None
    governing_law: str = None
    better_terms: bool = False
    non_compete: bool = False
    exclusivity: bool = False
    customer_solicitation: bool = False
    employee_solicitation: bool = False
    non_disparagement: bool = False
    convenience_termination: bool = False
    first_rights: bool = False
    change_control: bool = False
    anti_assignment: bool = False
    profit_sharing: bool = False
    price_restriction: bool = False
    minimum_commitment: bool = False
    volume_restriction: bool = False
    ip_assignment: bool = False
    joint_ip: bool = False
    license_grant: bool = False
    non_transferable_license: bool = False
    affiliate_licensor: bool = False
    affiliate_licensee: bool = False
    unlimited_usage: bool = False
    perpetual_license: bool = False
    code_escrow: bool = False
    post_termination: bool = False
    audit_rights: bool = False
    uncapped_liability: bool = False
    capped_liability: bool = False
    liquidated_damages: bool = False
    warranty_duration: str = ""
    insurance: bool = False
    outside_claims: bool = False
    third_party: bool = False
    id: int = None

    def __eq__(self, other):
        ignore_fields = {"id"}
        return all((value == other.__dict__[key]) for key, value in self.__dict__.items()
                   if key not in ignore_fields)

    def __ne__(self, other):
        return not self.__eq__(other)


label_mappings = {
    "Document Name": "document_name",
    "Parties": "parties",
    "Agreement Date": "agreement_date",
    "Effective Date": "effective_date",
    "Expiration Date": "expiration_date",
    "Renewal Term": "renewal_term",
    "Notice to Terminate Renewal": "termination_term",
    "Governing Law": "governing_law",
    "Most Favored Nation": "better_terms",
    "Non-Compete": "non_compete",
    "Exclusivity": "exclusivity",
    "No-Solicit of Customers": "customer_solicitation",
    "No-Solicit of Employees": "employee_solicitation",
    "Non-Disparagement": "non_disparagement",
    "Termination for Convenience": "convenience_termination",
    "Right of First Refusal, Offer or Negotiation (ROFR/ROFO/ROFN)": "first_rights",
    "Change of Control": "change_control",
    "Anti-Assignment": "anti_assignment",
    "Revenue/Profit Sharing": "profit_sharing",
    "Price Restriction": "price_restriction",
    "Minimum Commitment": "minimum_commitment",
    "Volume Restriction": "volume_restriction",
    "IP Ownership Assignment": "ip_assignment",
    "Joint IP Ownership": "joint_ip",
    "License Grant": "license_grant",
    "Non-Transferable License": "non_transferable_license",
    "Affiliate IP License-Licensor": "affiliate_licensor",
    "Affiliate IP License-Licensee": "affiliate_licensee",
    "Unlimited/All-You-Can-Eat License": "unlimited_usage",
    "Irrevocable or perpetual License": "perpetual_license",
    "Source Code Escrow": "code_escrow",
    "Post-Termination Services": "post_termination",
    "Audit Rights": "audit_rights",
    "Uncapped liability": "uncapped_liability",
    "Cap on Liability": "capped_liability",
    "Liquidated Damages": "liquidated_damages",
    "Warranty Duration": "warranty_duration",
    "Insurance": "insurance",
    "Covenant not to Sue": "outside_claims",
    "Third Party Beneficiary": "third_party",
}


class AtticusMasterClause(NamedTuple):
    pass
