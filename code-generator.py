import re
import requests
from bs4 import BeautifulSoup
import os

URLS = [
    'https://developers.binance.com/docs/binance-spot-api-docs',
    'https://developers.binance.com/docs/derivatives/change-log',
    'https://developers.binance.com/docs/margin_trading/change-log',
    'https://developers.binance.com/docs/algo/change-log',
    'https://developers.binance.com/docs/wallet/change-log',
    'https://developers.binance.com/docs/copy_trading/change-log',
    'https://developers.binance.com/docs/convert/change-log',
    'https://developers.binance.com/docs/sub_account/change-log',
    'https://developers.binance.com/docs/binance_link/change-log',
    'https://developers.binance.com/docs/auto_invest/change-log',
    'https://developers.binance.com/docs/staking/change-log',
    'https://developers.binance.com/docs/dual_investment/change-log',
    'https://developers.binance.com/docs/mining/change-log',
    'https://developers.binance.com/docs/crypto_loan/change-log',
    'https://developers.binance.com/docs/vip_loan/change-log',
    'https://developers.binance.com/docs/c2c/change-log',
    'https://developers.binance.com/docs/fiat/change-log',
    'https://developers.binance.com/docs/nft/change-log',
    'https://developers.binance.com/docs/gift_card/change-log',
    'https://developers.binance.com/docs/rebate/change-log',
    'https://developers.binance.com/docs/simple_earn/change-log',
    'https://developers.binance.com/docs/pay/change-log'
]

# Map endpoint prefixes to client.py's request methods
PREFIX_MAP = {
    '/api': '_request_api',
    '/sapi': '_request_margin_api',
    '/papi': '_request_papi_api',
    '/fapi': '_request_futures_api',
    '/dapi': '_request_futures_coin_api',
    '/eapi': '_request_options_api',
    '/wapi': '_request_website'
}

DEPRECATED_PREFIXES = [
    '/wapi',
]

# Some request methods do not require a version argument
NO_VERSION_FUNCTIONS = [
    '_request_options_api',
    '_request_futures_data_api'
]

def fetch_endpoints():
    """Fetch endpoints from the provided Binance doc URLs, filtering duplicates."""
    endpoints = set()
    deprecated_endpoints = set()
    for url in URLS:
        print(f'Fetching {url}')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_code_blocks = soup.find_all('code')

        for code in all_code_blocks:
            code_text = code.get_text().strip()
            parts = code_text.split(' ')
            
            if len(parts) >=2:
                parts[0] = parts[0].strip()
                parts[1] = parts[1].strip().split('?')[0]
            # Basic check for lines that look like: GET /path or POST /path etc.
            if len(parts) >= 2 and parts[0] in ['GET', 'POST', 'PUT', 'DELETE'] and parts[1] is not None and parts[1] != '':
                method = parts[0]
                endpoint = parts[1]
                # Ensure endpoint starts with /
                if not endpoint.startswith('/'):
                    endpoint = '/' + endpoint
                if any(endpoint.startswith(prefix) for prefix in DEPRECATED_PREFIXES):
                    deprecated_endpoints.add((method, endpoint))
                # Use a tuple of (method, endpoint) for uniqueness
                endpoints.add((method, endpoint))
    print(f'Found {len(deprecated_endpoints)} deprecated endpoints in the docs.')
    print(f'Found {len(endpoints)} unique endpoints in the docs.')
    
    # Filter endpoints that don't start with any known prefix
    valid_endpoints = {
        (method, endpoint) for method, endpoint in endpoints 
        if any(endpoint.startswith(prefix) for prefix in PREFIX_MAP.keys())
    }
    
    filtered_count = len(endpoints) - len(valid_endpoints)
    print(f'Filtered out {filtered_count} endpoints that don\'t match known prefixes')
    print(f'Remaining endpoints: {len(valid_endpoints)}')
    
    return valid_endpoints

def get_request_function_and_path(endpoint: str):
    """
    Given an endpoint (e.g. '/sapi/v1/userInfo'), determine which _request_*_api
    function is appropriate in the client, remove the recognized prefix plus any
    version segments (e.g. /v1/), parse out any version (v1, v2, etc.), 
    and return (request_function, stripped_path, version).

    Example:
        endpoint = '/sapi/v1/exchangeInfo'
        -> returns ('_request_margin_api', 'exchangeInfo', 1)

    If no recognized prefix is found, return (None, None, None).
    If no version is found, version will be None.
    """
    # Sort prefixes by length descending to match the longest prefix first
    sorted_prefixes = sorted(PREFIX_MAP.keys(), key=len, reverse=True)
    request_func = None

    # Identify which prefix is present, if any
    matched_prefix = None
    for prefix in sorted_prefixes:
        if endpoint.startswith(prefix):
            request_func = PREFIX_MAP[prefix]
            matched_prefix = prefix
            break

    # If no recognized prefix, return null
    if not request_func:
        return None, None, None

    # Extract the portion after removing the matched prefix
    stripped = endpoint[len(matched_prefix):]

    # Attempt to parse out the version, e.g. '/v1/', '/v2/'
    version_match = re.search(r'/v(\d+)/', stripped)
    version = None
    if version_match:
        # Convert the matched text into an integer
        version = int(version_match.group(1))

    # Remove version segments like /v1/, /v2/
    stripped = re.sub(r'/v\d+/', '/', stripped)

    # Strip leading/trailing slashes
    stripped = stripped.strip('/')

    return request_func, stripped, version

def check_in_client_py(method, endpoint, file_name):
    """
    Return True if a function for this endpoint likely exists in client.py.
    Uses get_request_function_and_path to find the correct request function,
    path, and version for the internal call.
    """
    if not os.path.isfile(file_name):
        print(f'{file_name} does not exist')
        return False

    func_name, stripped_path, version = get_request_function_and_path(endpoint)
    # If no known request function is found, we consider it not found.
    if not func_name:
        print(f'No known request function for endpoint: {endpoint}')
        return False

    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any leftover version tokens from the path
    stripped_path = re.sub(r'^v\d+/', '', stripped_path)
    stripped_path = re.sub(r'/v\d+/', '/', stripped_path)

    # Construct a regex pattern to match across multiple lines/spaces
    # e.g. _request_margin_api("get","exchangeInfo"...
    pattern_main = re.compile(
        rf'{re.escape(func_name)}\(\s*"{re.escape(method.lower())}"\s*,\s*"{re.escape(stripped_path)}"',
        re.DOTALL
    )

    # Also check for potential helper method usage (like _get, _post) if func_name == "_request_api"
    pattern_alt = None
    if func_name == "_request_api":
        alt_method = f"_{method.lower()}"
        pattern_alt = re.compile(
            rf'{re.escape(alt_method)}\(\s*"{re.escape(stripped_path)}"',
            re.DOTALL
        )

    if pattern_main.search(content):
        return True

    if pattern_alt and pattern_alt.search(content):
        return True

    return False

def convert_to_function_name(method: str, endpoint: str) -> str:
    """
    Convert an endpoint path to a consistent function name format with appropriate prefix and version.
    Examples:
        GET, /api/v3/ticker/tradingDay -> v3_get_ticker_trading_day
        GET, /sapi/v1/margin/order -> margin_v1_get_order
        GET, /fapi/v1/ticker/price -> futures_v1_get_ticker_price
        GET, /dapi/v1/ticker/price -> futures_coin_v1_get_ticker_price
        GET, /vapi/v1/ticker -> options_v1_get_ticker
    """
    # Get the request function and path info
    request_function, cleaned_endpoint, version = get_request_function_and_path(endpoint)
    
    # Map request functions to their prefix in the function name
    PREFIX_NAME_MAP = {
        '_request_margin_api': 'margin',
        '_request_papi_api': 'papi',
        '_request_futures_api': 'futures',
        '_request_futures_coin_api': 'futures_coin',
        '_request_options_api': 'options'
    }
    
    # Remove known prefixes and version segments first
    cleaned_endpoint = endpoint
    sorted_prefixes = sorted(PREFIX_MAP.keys(), key=len, reverse=True)
    for prefix in sorted_prefixes:
        if cleaned_endpoint.startswith(prefix):
            cleaned_endpoint = cleaned_endpoint[len(prefix):]
            break

    # Remove version segments and leading/trailing slashes
    cleaned_endpoint = re.sub(r'/v\d+/', '/', cleaned_endpoint)
    cleaned_endpoint = cleaned_endpoint.strip('/')

    # Split on slashes and process each part
    parts = cleaned_endpoint.split('/')
    processed_parts = []
    
    for part in parts:
        # Replace hyphens with underscores
        part = part.replace('-', '_')
        part = part.replace('.', '_')
        
        # Insert underscore before capital letters in camelCase
        part = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', part)
        
        # Convert to lowercase
        part = part.lower()
        
        # Remove any duplicate underscores
        part = re.sub(r'_+', '_', part)
        
        processed_parts.append(part)

    # Join all parts with underscores
    base_name = '_'.join(processed_parts)
    base_name = re.sub(r'_+', '_', base_name)  # Remove any duplicate underscores

    # Add version to the name (default to v1 if no version found)
    version_str = f"v{version if version else ''}"

    # Prepend the appropriate prefix if this is a special endpoint
    if request_function in PREFIX_NAME_MAP:
        prefix = PREFIX_NAME_MAP[request_function]
        return f"{prefix}_{version_str}_{method.lower()}_{base_name}"
    
    # Default case (for _request_api)
    return f"{version_str}_{method.lower()}_{base_name}"

def generate_function_code(method, endpoint, type="sync", file_name="./binance/client.py"):
    """
    Determines which _request_*_api function, path, and version to call based on the endpoint,
    generates a placeholder function to handle the specified method/endpoint.
    If the chosen request function is in NO_VERSION_FUNCTIONS, the code does not pass a 'version' argument.
    If no recognized prefix is found, returns an empty string.
    """
    request_function, cleaned_endpoint, version = get_request_function_and_path(endpoint)

    # If no recognized prefix, skip generating
    if not request_function:
        return ""

    func_name = convert_to_function_name(method, endpoint)
    
    # Build version argument if needed
    if request_function in NO_VERSION_FUNCTIONS or version is None:
        # No version arg is needed
        version_arg = ""
    else:
        # If a version was found, pass version= the integer, else default to 1
        version_arg_val = version if version else 1
        version_arg = f", version={version_arg_val}"

    code_snippet = ""
    if type == "sync":
        code_snippet = f"""
    def {func_name}(self, **params):
        \"\"\"
        Placeholder function for {method.upper()} {endpoint}.
        Note: This function was auto-generated. Any issue please open an issue on GitHub.

        :param params: parameters required by the endpoint
        :type params: dict

        :returns: API response
        \"\"\"
        return self.{request_function}("{method.lower()}", "{cleaned_endpoint}", signed=True, data=params{version_arg})
        """
    elif type == "async":
        code_snippet = f"""
    async def {func_name}(self, **params):
        return await self.{request_function}("{method.lower()}", "{cleaned_endpoint}", signed=True, data=params{version_arg})

    {func_name}.__doc__ = Client.{func_name}.__doc__
        """
    
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(code_snippet)

def write_function_to_endpoints_md(method, endpoint):
    """
    Append a brief reference entry to Endpoints.md, showing the usage example.
    First checks if the entry already exists to avoid duplicates.
    """
    function_name = convert_to_function_name(method, endpoint)
    
    
    # Check if the entry already exists
    with open('Endpoints.md', 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for the exact method and endpoint
        if f"**{method.upper()} {endpoint}" in content:
            return False
    
    # Create the entry we want to add
    md_entry = (
        f"\t- **{method} {endpoint}**\n"
        f"    ```python\n"
        f"    client.{function_name}(**params)\n"
        f"    ```\n\n"
    )

    # If we get here, the entry doesn't exist, so append it
    with open('Endpoints.md', 'a', encoding='utf-8') as f:
        f.write(md_entry)
    
    return True
    
def main():
    endpoints = fetch_endpoints()

    # Write to Endpoints.md
    endpoints_md_created = 0
    for method, endpoint in endpoints:
        success = write_function_to_endpoints_md(method, endpoint)
        if success:
            endpoints_md_created += 1
    print(f"Added {endpoints_md_created} endpoints to Endpoints.md")

    # Filter out endpoints already in client.py
    new_endpoints = []
    for method, endpoint in endpoints:
        if not check_in_client_py(method, endpoint, './binance/client.py'):
            new_endpoints.append((method, endpoint))

    print(f"{len(new_endpoints)} endpoints were added out of {len(endpoints)} scrapped in client.py")


    # Generate placeholder code for these endpoints
    for method, endpoint in new_endpoints:
        generate_function_code(method, endpoint, type="sync", file_name="./binance/client.py")

    # Generate async functions
    new_endpoints_async = []
    for method, endpoint in endpoints:
        if not check_in_client_py(method, endpoint, './binance/async_client.py'):
            new_endpoints_async.append((method, endpoint))

    for method, endpoint in new_endpoints_async:
        generate_function_code(method, endpoint, type="async", file_name="./binance/async_client.py")

    print(f"{len(new_endpoints_async)} endpoints were added out of {len(endpoints)} scrapped in async_client.py")
if __name__ == "__main__":
    main()
