"""
Fill the Rye Electric New Hire Packet PDF with employee data.
Usage: python fill_packet.py <input.pdf> <output.pdf> [--json <data.json>]
Or import fill_pdf(data_dict, input_pdf, output_pdf)
"""

import sys
import json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, ArrayObject

def fill_pdf(data: dict, input_path: str, output_path: str):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.append(reader)

    # Map our data fields to PDF field names
    today = data.get('submitted_at', '')[:10] if data.get('submitted_at') else ''
    full_name = f"{data.get('first_name','')} {data.get('middle_initial','')} {data.get('last_name','')}".strip()
    full_name_no_mi = f"{data.get('first_name','')} {data.get('last_name','')}".strip()

    field_values = {
        # Page 1 - New Hire Record
        'Last Name': data.get('last_name', ''),
        'First Name': data.get('first_name', ''),
        'Middle': data.get('middle_initial', ''),
        'Address': data.get('address', ''),
        'City': data.get('city', ''),
        'State': data.get('state', ''),
        'Zip': data.get('zip', ''),
        'Home Phone': data.get('phone', ''),
        'Cell': data.get('cell', ''),
        'Email': data.get('email', ''),
        'Soc. Sec. #': data.get('i9_ssn', ''),
        'Birth Date': data.get('date_of_birth', ''),
        'Emergency Contact': data.get('ec_name', ''),
        'Contact Phone #': data.get('ec_phone', ''),
        'Contact Relation': data.get('ec_relationship', ''),
        'Position/Trade Title': data.get('job_title', ''),
        'Hire Date': data.get('start_date', ''),

        # W-4 fields
        'topmostSubform[0].Page1[0].Step1a[0].f1_01[0]': data.get('first_name', ''),
        'topmostSubform[0].Page1[0].Step1a[0].f1_02[0]': data.get('last_name', ''),
        'topmostSubform[0].Page1[0].Step1a[0].f1_03[0]': data.get('address', ''),
        'topmostSubform[0].Page1[0].Step1a[0].f1_04[0]': f"{data.get('city','')} {data.get('state','')} {data.get('zip','')}",
        'topmostSubform[0].Page1[0].f1_05[0]': data.get('i9_ssn', ''),
        'topmostSubform[0].Page1[0].Step3_ReadOrder[0].f1_06[0]': str(data.get('w4_dependent_credits', '')),
        'topmostSubform[0].Page1[0].Step3_ReadOrder[0].f1_07[0]': '',
        'topmostSubform[0].Page1[0].f1_09[0]': str(data.get('w4_other_income', '')),
        'topmostSubform[0].Page1[0].f1_10[0]': '',
        'topmostSubform[0].Page1[0].f1_11[0]': str(data.get('w4_extra_withholding', '')),
        'topmostSubform[0].Page1[0].f1_12[0]': 'Rye Electric, Inc.',
        'topmostSubform[0].Page1[0].f1_13[0]': data.get('start_date', ''),
        'topmostSubform[0].Page1[0].f1_14[0]': '',
        'topmostSubform[0].Page1[0].f1_15[0]': '',

        # DE 4 fields
        'Name 1': full_name,
        'Social Security Number 1': data.get('i9_ssn', ''),
        'Address 1': data.get('address', ''),
        'City#1': data.get('city', ''),
        'State#1': data.get('state', ''),
        'ZIP Code': data.get('zip', ''),
        '1a': str(data.get('de4_allowances', '')),
        '1b': '',
        '1c': str(data.get('de4_allowances', '')),
        '2': str(data.get('de4_extra_withholding', '')),
        'Date Employee Signed': today,
        'Employer\'s Name and Address': 'Rye Electric, Inc.',
        'California Employer Payroll Tax Account Number': '',

        # Direct Deposit
        'COMPANY NAME': 'Rye Electric, Inc.',
        'EMPLOYEE BANK NAME': data.get('bank1_name', ''),
        'BANK ROUTING #': data.get('bank1_routing', ''),
        'ACCOUNT #': data.get('bank1_account', ''),
        'PERCENTAGE OR DOLLAR AMT': data.get('bank1_deposit_amount', '100%'),
        'EMPLOYEE BANK NAME#0.1': data.get('bank2_name', ''),
        'BANK ROUTING': data.get('bank2_routing', ''),
        'ACCOUNT': data.get('bank2_account', ''),
        'Printed Name': full_name_no_mi,
        'Date': today,

        # I-9 Section 1
        'Last Name (Family Name)': data.get('last_name', ''),
        'First Name Given Name': data.get('first_name', ''),
        'Employee Middle Initial (if any)': data.get('middle_initial', ''),
        'Employee Other Last Names Used (if any)': '',
        'Address Street Number and Name': data.get('address', ''),
        'City or Town': data.get('city', ''),
        'ZIP Code#1': data.get('zip', ''),
        'Date of Birth mmddyyyy': data.get('date_of_birth', ''),
        'US Social Security Number': data.get('i9_ssn', ''),
        'Employees E-mail Address': data.get('email', ''),
        'Telephone Number': data.get('phone', ''),
        'Signature of Employee': data.get('e_signature', ''),
        'Today\'s Date mmddyyy': today,

        # Policy signatures
        'Print Name': data.get('e_signature', ''),
        'Print Name#1': data.get('e_signature', ''),
        'Print Name#2': data.get('e_signature', ''),
        'Print Name#3': data.get('e_signature', ''),
        'Print Name#4': data.get('e_signature', ''),
        'Print Name Self-Identification Forn': data.get('e_signature', ''),
        'Date#1': today,
        'Date#2': today,
        'Date#3': today,
        'Date#4': today,
        'Date#5': today,
        'Date#6': today,

        # Motor Vehicle Record
        'Name as it appears on Driver License': full_name_no_mi,
        'Driver License NumberState of Issuance': data.get('drivers_license', ''),
        'Date of Birth': data.get('date_of_birth', ''),
        'Date 00/00/0000': today,

        # Handbook acknowledgement initials
        'Unlawful Harassment Policy': data.get('first_name', '')[:1] + data.get('last_name', '')[:1],
        'Confidentiality Agreement': data.get('first_name', '')[:1] + data.get('last_name', '')[:1],
        'Drug  Alcohol Policy': data.get('first_name', '')[:1] + data.get('last_name', '')[:1],
        'Standards of Conduct': data.get('first_name', '')[:1] + data.get('last_name', '')[:1],
        'Employee Name Print': full_name_no_mi,
        'Employee Name': data.get('last_name', '') + ', ' + data.get('first_name', ''),
        'Start Date#1': data.get('start_date', ''),
        'Legal Name of Hiring Employer': 'Rye Electric, Inc.',
        'Physical Address of Hiring Employers Main Office': '123 Main St, Anaheim, CA 92801',
        'Hiring Employers Telephone Number': '',
        'PRINT NAME of Employee': full_name_no_mi,
        'PRINT NAME of Employer representative': 'Rye Electric, Inc.',
        'Date_2': today,
    }

    # Checkbox values based on data
    checkbox_values = {}

    # W-4 filing status
    w4_status = data.get('w4_filing_status', '')
    if w4_status == 'single':
        checkbox_values['topmostSubform[0].Page1[0].c1_1[0]'] = True
    elif w4_status == 'married_joint':
        checkbox_values['topmostSubform[0].Page1[0].c1_1[1]'] = True
    elif w4_status == 'hoh':
        checkbox_values['topmostSubform[0].Page1[0].c1_1[2]'] = True

    # DE 4 filing status
    de4_status = data.get('de4_filing_status', '')
    if de4_status == 'single_dual':
        checkbox_values['Filing Status 1'] = True
    elif de4_status == 'married_one':
        checkbox_values['Filing Status 2'] = True
    elif de4_status == 'hoh':
        checkbox_values['Filing Status 3'] = True

    # New hire checkbox
    checkbox_values['New Hire'] = True

    # Employment type
    checkbox_values['Full Time'] = True
    checkbox_values['Hourly'] = True

    # Direct deposit account type
    if data.get('bank1_type') == 'checking':
        checkbox_values['CHECKING ACCT'] = True
    elif data.get('bank1_type') == 'savings':
        checkbox_values['SAVINGS ACCT'] = True

    if data.get('bank2_type') == 'checking':
        checkbox_values['CHECKING ACCT#0.1'] = True
    elif data.get('bank2_type') == 'savings':
        checkbox_values['SAVINGS ACCT#0.1'] = True

    # I-9 citizenship
    i9_status = data.get('i9_citizenship_status', '')
    if i9_status == 'citizen':
        checkbox_values['CB_1'] = True
    elif i9_status == 'national':
        checkbox_values['CB_2'] = True
    elif i9_status == 'lpr':
        checkbox_values['CB_3'] = True
    elif i9_status == 'authorized':
        checkbox_values['CB_4'] = True

    # Marital status
    checkbox_values['Marital Status/Single'] = True

    # Fill text fields
    for field_name, value in field_values.items():
        if value:
            try:
                writer.update_page_form_field_values(None, {field_name: str(value)})
            except Exception as e:
                pass

    # Fill checkboxes
    for page in writer.pages:
        if '/Annots' in page:
            for annot in page['/Annots']:
                obj = annot.get_object()
                field_name = obj.get('/T', '')
                if isinstance(field_name, bytes):
                    field_name = field_name.decode('utf-8', errors='ignore')

                if field_name in checkbox_values and checkbox_values[field_name]:
                    try:
                        obj.update({
                            NameObject('/V'): NameObject('/Yes'),
                            NameObject('/AS'): NameObject('/Yes'),
                        })
                    except Exception:
                        pass

    # Write output
    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f"PDF filled successfully: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python fill_packet.py <input.pdf> <output.pdf> [data.json]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]

    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            data = json.load(f)
    else:
        # Test data
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'middle_initial': 'A',
            'address': '123 Oak Street',
            'city': 'Anaheim',
            'state': 'CA',
            'zip': '92801',
            'phone': '714-555-1234',
            'cell': '714-555-5678',
            'email': 'john.smith@email.com',
            'date_of_birth': '01/15/1990',
            'job_title': 'Electrician',
            'start_date': '07/01/2026',
            'ec_name': 'Jane Smith',
            'ec_relationship': 'Spouse',
            'ec_phone': '714-555-9999',
            'w4_filing_status': 'single',
            'w4_dependent_credits': 0,
            'w4_other_income': 0,
            'w4_extra_withholding': 0,
            'de4_filing_status': 'single_dual',
            'de4_allowances': 1,
            'de4_extra_withholding': 0,
            'bank1_name': 'Chase Bank',
            'bank1_routing': '021000021',
            'bank1_account': '123456789',
            'bank1_type': 'checking',
            'bank1_deposit_amount': '100%',
            'i9_citizenship_status': 'citizen',
            'i9_ssn': '123-45-6789',
            'ack_confidentiality': True,
            'ack_drug_alcohol': True,
            'ack_harassment': True,
            'ack_at_will': True,
            'ack_arbitration': True,
            'ack_handbook': True,
            'e_signature': 'John A Smith',
            'drivers_license': 'CA D1234567',
            'submitted_at': '2026-06-26T00:00:00Z',
        }

    fill_pdf(data, input_pdf, output_pdf)
