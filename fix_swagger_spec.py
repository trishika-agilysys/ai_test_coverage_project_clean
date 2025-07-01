import json

def fix_swagger_spec(input_file='data/raw/swagger_fixed.json', output_file='data/raw/swagger_fixed.json'):
    """
    Fixes common issues in Swagger specification:
    1. Empty schemes array
    2. Duplicate operation IDs for:
       - Card balance endpoints
       - Token creation endpoints
       - Sale transaction endpoints
       - Auth transaction endpoints
       - Force capture endpoints
       - Credit transaction endpoints
    """
    # Read the input swagger file
    with open(input_file, 'r') as f:
        swagger = json.load(f)

    # Fix schemes array
    if 'schemes' in swagger and not swagger['schemes']:
        swagger['schemes'] = ['https']

    # Define all endpoint updates
    endpoint_updates = {
        # Card balance endpoints
        '/v1.5/card/balance/device/{deviceGuid}': 'Card_CardBalanceOnDevice',
        '/v1.5/card/balance/token/{token}': 'Card_CardBalanceWithToken',
        '/v1.5/card/balance': 'Card_CardBalanceWithCardData',

        # Token creation endpoints
        '/v1.5/token/create/device/{deviceGuid}': 'Token_CreateTokenOnDevice',
        '/v1.5/token/create': 'Token_CreateTokenWithCardData',

        # Sale transaction endpoints
        '/v1.5/transaction/sale/device/{deviceGuid}': 'Transaction_SaleOnDevice',
        '/v1.5/transaction/sale/token/{token}': 'Transaction_SaleWithToken',
        '/v1.5/transaction/sale': 'Transaction_SaleWithCardData',

        # Auth transaction endpoints
        '/v1.5/transaction/auth/device/{deviceGuid}': 'Transaction_AuthOnDevice',
        '/v1.5/transaction/auth/token/{token}': 'Transaction_AuthWithToken',
        '/v1.5/transaction/auth': 'Transaction_AuthWithCardData',
        '/v1.5/transaction/auth/transaction/state': 'Transaction_AuthWithTransactionState',

        # Force capture endpoints
        '/v1.5/transaction/forcecapture/token/{token}': 'Transaction_ForceCaptureWithToken',
        '/v1.5/transaction/forcecapture': 'Transaction_ForceCaptureWithCardData',
        '/v1.5/transaction/forcecapture/transaction/state': 'Transaction_ForceCaptureWithTransactionState',

        # Credit transaction endpoints
        '/v1.5/transaction/credit/device/{deviceGuid}': 'Transaction_CreditOnDevice',
        '/v1.5/transaction/credit/token/{token}': 'Transaction_CreditWithToken',
        '/v1.5/transaction/credit': 'Transaction_CreditWithCardData',
        '/v1.5/transaction/credit/transaction/state': 'Transaction_CreditWithTransactionState'
    }

    # Update operation IDs
    paths = swagger['paths']
    for path, new_operation_id in endpoint_updates.items():
        if path in paths:
            paths[path]['post']['operationId'] = new_operation_id

    # Fix $ref with siblings warning by moving properties to the referenced definition
    if 'definitions' in swagger:
        definitions = swagger['definitions']
        
        # Fix CancellationToken waitHandle property
        if 'CancellationToken' in definitions:
            token_def = definitions['CancellationToken']
            if 'properties' in token_def and 'waitHandle' in token_def['properties']:
                wait_handle = token_def['properties']['waitHandle']
                if '$ref' in wait_handle and 'readOnly' in wait_handle:
                    # Get the referenced definition
                    ref_name = wait_handle['$ref'].split('/')[-1]
                    if ref_name in definitions:
                        # Add readOnly to the referenced definition
                        if 'readOnly' not in definitions[ref_name]:
                            definitions[ref_name]['readOnly'] = wait_handle['readOnly']
                        # Keep only the reference
                        token_def['properties']['waitHandle'] = {'$ref': wait_handle['$ref']}

        # Fix any other properties that might have $ref with siblings
        def fix_ref_siblings(obj):
            if isinstance(obj, dict):
                for key, value in list(obj.items()):
                    if isinstance(value, dict) and '$ref' in value and len(value) > 1:
                        # Get the referenced definition
                        ref_name = value['$ref'].split('/')[-1]
                        if ref_name in definitions:
                            # Add additional properties to the referenced definition
                            for k, v in value.items():
                                if k != '$ref' and k not in definitions[ref_name]:
                                    definitions[ref_name][k] = v
                            # Keep only the reference
                            obj[key] = {'$ref': value['$ref']}
                    else:
                        fix_ref_siblings(value)
            elif isinstance(obj, list):
                for item in obj:
                    fix_ref_siblings(item)

        # Apply the fix recursively to all definitions
        fix_ref_siblings(definitions)

    # Write the updated swagger to output file
    with open(output_file, 'w') as f:
        json.dump(swagger, f, indent=2)

    print(f"Successfully fixed Swagger specification and saved to {output_file}")

if __name__ == "__main__":
    # You can specify different input/output files if needed
    fix_swagger_spec()