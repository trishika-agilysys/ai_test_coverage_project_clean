# Comprehensive Test Generation Summary Report
Generated on: 2025-06-23 10:40:32

## Overall Statistics
- **Total Endpoints**: 57
- **Total Test Scenarios**: 653
- **Average Scenarios per Endpoint**: 11.5

## Test Scenario Breakdown
- **all_required**: 53 (8.1%)
- **concurrent_requests**: 57 (8.7%)
- **expired_auth**: 57 (8.7%)
- **invalid_auth**: 57 (8.7%)
- **large_payload**: 57 (8.7%)
- **missing_required**: 85 (13.0%)
- **no_auth**: 57 (8.7%)
- **optional_combination**: 2 (0.3%)
- **rate_limit**: 57 (8.7%)
- **sql_injection**: 57 (8.7%)
- **timeout_test**: 57 (8.7%)
- **xss_test**: 57 (8.7%)

## Endpoint Details
### GET /v1.5/health
- **Operation ID**: Health_GetHealth
- **Summary**: Performs a basic health check to verify the rGuest Pay Agent is running and
actively accepting connections
- **Required Parameters**: 0
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 1
- **Test Scenarios**: 9

#### Test Scenarios:
1. **no_auth**: Test without authentication headers
2. **invalid_auth**: Test with invalid authentication token
3. **expired_auth**: Test with expired authentication token
4. **sql_injection**: Test for SQL injection vulnerabilities
5. **xss_test**: Test for XSS vulnerabilities
6. **rate_limit**: Test rate limiting behavior
7. **large_payload**: Test with large request payload
8. **concurrent_requests**: Test concurrent request handling
9. **timeout_test**: Test timeout behavior

### GET /v1.5/health/detail
- **Operation ID**: Health_GetHealthDetail
- **Summary**: Performs a detailed health check for the rGuest Pay Agent and returns the
current health status information
- **Required Parameters**: 0
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 2
- **Test Scenarios**: 9

#### Test Scenarios:
1. **no_auth**: Test without authentication headers
2. **invalid_auth**: Test with invalid authentication token
3. **expired_auth**: Test with expired authentication token
4. **sql_injection**: Test for SQL injection vulnerabilities
5. **xss_test**: Test for XSS vulnerabilities
6. **rate_limit**: Test rate limiting behavior
7. **large_payload**: Test with large request payload
8. **concurrent_requests**: Test concurrent request handling
9. **timeout_test**: Test timeout behavior

### GET /v1.5/health/terminal
- **Operation ID**: Health_GetTerminalDetails
- **Summary**: Performs a detailed terminal health check where the rGuest Pay Agent is installed, and 
returns the current terminal information
- **Required Parameters**: 0
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 3
- **Test Scenarios**: 9

#### Test Scenarios:
1. **no_auth**: Test without authentication headers
2. **invalid_auth**: Test with invalid authentication token
3. **expired_auth**: Test with expired authentication token
4. **sql_injection**: Test for SQL injection vulnerabilities
5. **xss_test**: Test for XSS vulnerabilities
6. **rate_limit**: Test rate limiting behavior
7. **large_payload**: Test with large request payload
8. **concurrent_requests**: Test concurrent request handling
9. **timeout_test**: Test timeout behavior

### GET /v1.5/device/list
- **Operation ID**: Device_GetDeviceList
- **Summary**: Returns a list of configured payment devices
- **Required Parameters**: 0
- **Optional Parameters**: 1
- **Has Request Body**: False
- **Response Codes**: 3
- **Test Scenarios**: 10

#### Test Scenarios:
1. **optional_combination**: Test with optional parameters: includeExtendedData
2. **no_auth**: Test without authentication headers
3. **invalid_auth**: Test with invalid authentication token
4. **expired_auth**: Test with expired authentication token
5. **sql_injection**: Test for SQL injection vulnerabilities
6. **xss_test**: Test for XSS vulnerabilities
7. **rate_limit**: Test rate limiting behavior
8. **large_payload**: Test with large request payload
9. **concurrent_requests**: Test concurrent request handling
10. **timeout_test**: Test timeout behavior

### GET /v1.5/device/{deviceGuid}
- **Operation ID**: Device_GetDeviceInfo
- **Summary**: Returns the device info for the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 1
- **Has Request Body**: False
- **Response Codes**: 2
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **optional_combination**: Test with optional parameters: includeExtendedData
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/device/{deviceGuid}/detach
- **Operation ID**: Device_DetachDevice
- **Summary**: Detaches the rGuest Pay Agent from the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/device/{deviceGuid}/lane/state/{laneState}
- **Operation ID**: Device_SetLaneState
- **Summary**: Sets the lane state to either open or closed
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: laneState
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/device/{deviceGuid}/standby
- **Operation ID**: Device_StandbyDevice
- **Summary**: Resets the specified payment device to the advertising/idle screen and terminates any current device operations
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 3
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### GET /v1.5/ondemand/cardcapture/device/{deviceGuid}
- **Operation ID**: OnDemand_ReadCardData
- **Summary**: Reads the captured card data from the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 5
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/cardcapture/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptCardCapture
- **Summary**: Prompts for card capture on the specified payment device
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### GET /v1.5/ondemand/tipcapture/device/{deviceGuid}
- **Operation ID**: OnDemand_ReadTipAmount
- **Summary**: Reads the captured tip amount data from the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 5
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/tipcapture/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptTipAmount
- **Summary**: Prompts for tip on the specified payment device
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### GET /v1.5/ondemand/signaturecapture/device/{deviceGuid}
- **Operation ID**: OnDemand_ReadSignatureData
- **Summary**: Reads the captured signature data from the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 5
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/signaturecapture/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptSignatureCapture
- **Summary**: Prompts for signature capture on the specified payment device
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/selection/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptSelectionForm
- **Summary**: Prompts for the specified selection form on the specified payment device, and waits for the guest to interact
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/message/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptMessageForm
- **Summary**: Prompts the message form with the specified text on the specified payment device, and returns immediately
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/signature/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptSignatureForm
- **Summary**: Prompts for the specified signature form on the specified payment deivce, and waits for the guest to interact
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/customform/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptCustomForm
- **Summary**: Prompts for the specified custom form on the specified payment device, and waits for the guest to interact
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### GET /v1.5/ondemand/securitycode/device/{deviceGuid}
- **Operation ID**: OnDemand_ReadSecurityCode
- **Summary**: Reads the captured security code from the specified payment device
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 5
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/ondemand/securitycode/device/{deviceGuid}
- **Operation ID**: OnDemand_PromptSecurityCode
- **Summary**: Prompts for security code on the specified payment device.
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/card/info
- **Operation ID**: Card_CardInfo
- **Summary**: Returns the information for a card using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 3
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/card/balance/device/{deviceGuid}
- **Operation ID**: Card_CardBalanceOnDevice
- **Summary**: Returns the available balance on a card using the specified payment device for card capture
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/card/balance/token/{token}
- **Operation ID**: Card_CardBalanceWithToken
- **Summary**: Returns the available balance on a card using the specified token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: token
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/card/balance
- **Operation ID**: Card_CardBalanceWithCardData
- **Summary**: Returns the available balance on a card using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/token/create/device/{deviceGuid}
- **Operation ID**: Token_CreateTokenOnDevice
- **Summary**: Creates a token by using the specified payment device for card capture and exchanging
the encrypted card data for a token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/token/create
- **Operation ID**: Token_CreateTokenWithCardData
- **Summary**: Creates a token by exchanging the specified encrypted card data for a token
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/sale/begin/device/{deviceGuid}
- **Operation ID**: Transaction_BeginSale
- **Summary**: Performs a begin sale transaction using the specified payment device for card capture
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 4
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/sale/device/{deviceGuid}
- **Operation ID**: Transaction_SaleOnDevice
- **Summary**: Performs a sale transaction using the specified payment device for card capture
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/sale/token/{token}
- **Operation ID**: Transaction_SaleWithToken
- **Summary**: Performs a sale transaction using the specified card token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: token
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/sale
- **Operation ID**: Transaction_SaleWithCardData
- **Summary**: Performs a sale transaction using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/device/{deviceGuid}
- **Operation ID**: Transaction_AuthOnDevice
- **Summary**: Performs an authorization transaction using the specified payment device for card capture
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/token/{token}
- **Operation ID**: Transaction_AuthWithToken
- **Summary**: Performs a an authorization transaction using the specified card token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: token
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth
- **Operation ID**: Transaction_AuthWithCardData
- **Summary**: Performs an authorization transaction using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/transaction/state
- **Operation ID**: Transaction_AuthWithTransactionState
- **Summary**: Performs an authorization transaction using the specified transaction state from a prior offline transaction
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/increase/transaction/{transactionId}
- **Operation ID**: Transaction_AuthIncrease
- **Summary**: Increases a previously obtained authorization for the specified transaction identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 9
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/decrease/transaction/{transactionId}
- **Operation ID**: Transaction_AuthDecrease
- **Summary**: Decreases a previously obtained authorization for the specified transaction identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 9
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/auth/reversal/transaction/{transactionId}
- **Operation ID**: Transaction_AuthReversal
- **Summary**: Reverses or voids a previously obtained credit card authorization
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 9
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/capture/transaction/{transactionId}
- **Operation ID**: Transaction_Capture
- **Summary**: Captures a previous authorization for the specified transaction identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/forcecapture/token/{token}
- **Operation ID**: Transaction_ForceCaptureWithToken
- **Summary**: Captures a verbal or offline authorization using the specified token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: token
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/forcecapture
- **Operation ID**: Transaction_ForceCaptureWithCardData
- **Summary**: Captures a verbal or offline authorization using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/forcecapture/transaction/state
- **Operation ID**: Transaction_ForceCaptureWithTransactionState
- **Summary**: Captures a verbal or offline authorization using the specified transaction state
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/refund/transaction/{transactionId}
- **Operation ID**: Transaction_Refund
- **Summary**: Refunds a previously captured transaction for the specified transaction identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/credit/device/{deviceGuid}
- **Operation ID**: Transaction_CreditOnDevice
- **Summary**: Performs a credit transaction using the specified payment device for card capture
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: deviceGuid
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/credit/token/{token}
- **Operation ID**: Transaction_CreditWithToken
- **Summary**: Performs a credit transaction using the specified card token
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: token
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/credit
- **Operation ID**: Transaction_CreditWithCardData
- **Summary**: Performs a credit transaction using the specified encrypted card data
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/credit/transaction/state
- **Operation ID**: Transaction_CreditWithTransactionState
- **Summary**: Performs a credit transaction using the specified transaction state from a prior offline transaction
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 8
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/transaction/void/transaction/{transactionId}
- **Operation ID**: Transaction_Void
- **Summary**: Voids a transaction for the specified transaction identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: transactionId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check
- **Operation ID**: PayAtTable_OpenPayAtTableCheck
- **Summary**: Opens a Pay-at-Table check and returns the Pay-at-Table check identifier
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### PUT /v1.5/payattable/check/{checkId}
- **Operation ID**: PayAtTable_UpdatePayAtTableCheck
- **Summary**: Updates an existing Pay-at-Table check for the specified Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/checks/query
- **Operation ID**: PayAtTable_QueryPayAtTableChecks
- **Summary**: Queries the existing Pay-at-Table checks
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check/{checkId}/query
- **Operation ID**: PayAtTable_QueryPayAtTableCheck
- **Summary**: Queries an existing Pay-at-Table check for the specified Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check/{checkId}/payments/query
- **Operation ID**: PayAtTable_QueryPayAtTableCheckPayments
- **Summary**: Queries the payments applied to an existing Pay-at-Table check for the specified
Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check/{checkId}/payments/acknowledge
- **Operation ID**: PayAtTable_AcknolwedgePayAtTableCheckPayments
- **Summary**: Acknowledges the specified payments applied to an existing Pay-at-Table check for the
specified Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check/{checkId}/payments/updatetransaction
- **Operation ID**: PayAtTable_UpdatePayAtTableCheckPayment
- **Summary**: Pushes payment information to an existing Pay-at-Table check for the
specified Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/payattable/check/{checkId}/close
- **Operation ID**: PayAtTable_ClosePayAtTableCheck
- **Summary**: Closes an existing Pay-at-Table check for the specified Pay-at-Table check identifier
- **Required Parameters**: 2
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 7
- **Test Scenarios**: 12

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: checkId
3. **missing_required**: Test with missing required parameter: request
4. **no_auth**: Test without authentication headers
5. **invalid_auth**: Test with invalid authentication token
6. **expired_auth**: Test with expired authentication token
7. **sql_injection**: Test for SQL injection vulnerabilities
8. **xss_test**: Test for XSS vulnerabilities
9. **rate_limit**: Test rate limiting behavior
10. **large_payload**: Test with large request payload
11. **concurrent_requests**: Test concurrent request handling
12. **timeout_test**: Test timeout behavior

### POST /v1.5/operation/logcapture
- **Operation ID**: Operation_LogCapture
- **Summary**: Returns the response for log capture operation
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior

### POST /v1.5/operation/eodbatchprocess
- **Operation ID**: Operation_EODBatchProcess
- **Summary**: Performs the End Of Day(EOD) signal request for batch process
- **Required Parameters**: 1
- **Optional Parameters**: 0
- **Has Request Body**: False
- **Response Codes**: 6
- **Test Scenarios**: 11

#### Test Scenarios:
1. **all_required**: Test with all required parameters
2. **missing_required**: Test with missing required parameter: request
3. **no_auth**: Test without authentication headers
4. **invalid_auth**: Test with invalid authentication token
5. **expired_auth**: Test with expired authentication token
6. **sql_injection**: Test for SQL injection vulnerabilities
7. **xss_test**: Test for XSS vulnerabilities
8. **rate_limit**: Test rate limiting behavior
9. **large_payload**: Test with large request payload
10. **concurrent_requests**: Test concurrent request handling
11. **timeout_test**: Test timeout behavior
