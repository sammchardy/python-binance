// Usage: node utils/generate_missing_methods.js from the root directory

const fs = require('fs');
const { parse } = require('path');

const SOURCE_FILES = {
    'spot': './utils/spot_docs.txt',
    'futures': './utils/futures_docs.txt',
    'coin': './utils/coin_docs.txt',
    'options': './utils/options_docs.txt',
    'portfolio': './utils/portfolio_docs.txt',
}

const ENPOINTS_FILES = {
    'spot': './utils/spot_endpoints_list.txt',
    'futures': './utils/futures_endpoints_list.txt',
    'coin': './utils/coin_endpoints_list.txt',
    'options': './utils/options_endpoints_list.txt',
    'portfolio': './utils/portfolio_endpoints_list.txt',
}
const BINANCE_FILE = './binance/client.py'
const BINANCE_CALLS = [
    '_get',
    '_post',
    '_put',
    '_delete',
    '_request_margin_api',
    '_request_futures_api',
    '_request_futures_data_api',
    '_request_futures_coin_api',
    '_request_futures_coin_data_api',
    '_request_options_api',
    '_request_papi_api',
]
const TARGET_FILE_NAME = './utils/missing_endponts.txt'

const SPECIFIC_CALLS = {
    'spot': {
        'sapi': '_request_margin_api'
    },
    'futures': {
        'fapi': '_request_futures_api',
        'futures/data': '_request_futures_data_api',
    },
    'coin': {
        'dapi': '_request_futures_coin_api',
        'futures/data': '_request_futures_coin_data_api',
    },
    'options': {
        'eapi': '_request_options_api'
    },
    'portfolio': {
        'papi': '_request_papi_api',
        'fapi': '_request_futures_api'
    }
}

const PREFIXES = {
    'spot': {
        'sapi': 'margin',
    },
    'futures': {
        'fapi': 'futures',
        'futures/data': 'futures_data',
    },
    'coin': {
        'dapi': 'futures_coin',
        'futures/data': 'futures_coin_data',
    },
    'options': {
        'eapi': 'options',
    },
    'portfolio': {
        'papi': 'portfolio',
        'fapi': 'futures',
    }
}

const SPOT_API_VERSIONS = {
    'v1': 'self.PUBLIC_API_VERSION',
    'v3': 'self.PRIVATE_API_VERSION'
}

const OTHER_API_VERSIONS = {
    'v1': '1',
    'v2': '2',
    'v3': '3',
    'v4': '4'
}

const DEPRECATED = [
    'GET /fapi/v1/ticker/price',
    'GET /fapi/v1/pmExchangeInfo',
    'POST /api/v3/order/oco',
    'POST /sapi/v1/eth-staking/eth/stake',
    'GET /sapi/v1/eth-staking/account',
    'GET /sapi/v1/portfolio/interest-rate',
    'GET /api/v1/order',
    'GET /api/v1/openOrders',
    'POST /api/v1/order',
    'DELETE /api/v1/order',
    'GET /api/v1/allOrders',
    'GET /api/v1/account',
    'GET /api/v1/myTrades',
    'POST /sapi/v1/loan/flexible/borrow',
    'GET /sapi/v1/loan/flexible/ongoing/orders',
    'GET /sapi/v1/loan/flexible/borrow/history',
    'POST /sapi/v1/loan/flexible/repay',
    'GET /sapi/v1/loan/flexible/repay/history',
    'POST /sapi/v1/loan/flexible/adjust/ltv',
    'GET /sapi/v1/loan/flexible/ltv/adjustment/history',
    'GET /sapi/v1/loan/flexible/loanable/data',
    'GET /sapi/v1/loan/flexible/collateral/data'
]

function parseEndpoint (data, type) {
    const parts = data.split (' ')
    const method = parts[0].toLowerCase ()
    const endpoint = parts[1]
    let path = endpoint
    let api = undefined
    let version = undefined
    let splitSymbols = 'v1/'
    if (endpoint.indexOf ('futures/data') !== -1) {
        api = 'futures/data'
        splitSymbols = 'data/'
    } else {
        splittedEndpoint = endpoint.split ('/')
        api = splittedEndpoint[1]
        version = splittedEndpoint[2]
        splitSymbols = version + '/'
    }
    path = endpoint.split (splitSymbols)[1]
    const result = {
        'endpoint': method.toUpperCase() + ' ' + endpoint,
        'type': type,
        'method': method,
        'path': path,
        'api': api,
        'version': version
    }
    const methodName = generateMethodName (result)
    result['methodName'] = methodName
    const call = generateMethodCall (result)
    result['call'] = call
    return result
}

function parseEndpoints (data) {
    const result = {}
    const types = Object.keys (data)
    for (let type of types) {
        const endpoints = data[type]
        result[type] = {}
        for (let endpoint of endpoints) {
            const parsed = parseEndpoint (endpoint, type)
            result[type][endpoint] = parsed
        }
    }
    return result
}


function generateMethodCall (endpoint) {
    const { type, method, path, api, version } = endpoint
    const isSpot = type === 'spot'
    const apiVersions = isSpot ? SPOT_API_VERSIONS : OTHER_API_VERSIONS
    let func = 'self.'
    if (isSpot && api !== 'sapi') {
        func += '_' + method + '(' + '"' + path + '", ' + 'version=' + apiVersions[version] + ', data=params' + ')'
    } else {
        func += SPECIFIC_CALLS[type][api] + '(' + '"' + method + ', "' + path + '", ' + 'version=' + apiVersions[version] + ', data=params' + ')'
    }
    return func
}

function generateListsOfEndpoints (writeFiles = false) {
    const result = {}
    for (let type in SOURCE_FILES) {
        let file = SOURCE_FILES[type]
        const methodMatch = /(GET|POST|PUT|DELETE) (\/[^ ][\w\/-]+)/g
        const data = fs.readFileSync (file, 'utf8')
        const mathces = [... new Set (data.match (methodMatch))]
        for (let i = 0; i < DEPRECATED.length; i++) {
            let index = mathces.indexOf (DEPRECATED[i])
            if (index !== -1) {
                mathces.splice (index, 1)
            }
        }
        result[type] = mathces
        const targetData = mathces.join ('\n')
        const targetFile = ENPOINTS_FILES[type]
        if (writeFiles) {
            fs.writeFile (targetFile, targetData, (err) => {
                if (err) {
                    console.error (err)
                    return
                }
                console.log (targetFile + ' file is generated')
            })
        }
    }
    return result
}

function getCallsFromBinanceFile () {
    const data = fs.readFileSync (BINANCE_FILE, 'utf8').replace (/\s/g, '')
    const matchTemplate = /self._\w+\("[^\)]+\)/g
    const matches = data.match (matchTemplate)
    matches.forEach ((m, i) => matches[i] = m.replace ('self.', ''))
    return matches
}

function parseCall (call) {
    const parts = call.split ('(')
    const func = parts[0]
    const argsString = parts[1].replaceAll ('"', '').replace(')', '')
    const args = argsString.split (',')
    const [ type, api ] = parseTypeAndApi (func)
    if (type === undefined) {
        return { func, args }
    }
    let method = args[0]
    let path = args[1]
    if (type === 'spot' && func !== '_request_margin_api') {
        method = func.replace ('_', '')
        path = args[0]
    }
    let versionString = ''
    let version = undefined
    if (api !== 'future/data') {
        version = parseVersion (argsString, args, api)
        versionString = version + '/'
    }
    const endpoint = method.toUpperCase () + ' /' + api + '/' + versionString + '' + path
    return { endpoint, type, method, path, api, version, call }
}

function parseVersion (argsString, args, api) {
    let v = 'v1'
    let version = undefined
    const vMatch = /version=([^,]+),/
    const vMatchResult = argsString.match (vMatch)
    if (vMatchResult) {
        version = vMatchResult[1]
    } else if (args.length > 3 && api !== 'api') {
        version = args[3]
    }
    const versionTypes = {
        '1': 'v1',
        '2': 'v2',
        '3': 'v3',
        '4': 'v4',
        'PUBLIC_API_VERSION': 'v1',
        'PRIVATE_API_VERSION': 'v3'
    }
    if (versionTypes[version]) {
        v = versionTypes[version]
    }
    return v
}

function parseTypeAndApi (func) {
    const funcs = {
        '_get': {
            'type': 'spot',
            'api': 'api'
        },
        '_post': {
            'type': 'spot',
            'api': 'api'
        },
        '_put': {
            'type': 'spot',
            'api': 'api'
        },
        '_delete': {
            'type': 'spot',
            'api': 'api'
        },
        '_request_margin_api': {
            'type': 'spot',
            'api': 'sapi'
        },
        '_request_futures_api': {
            'type': 'futures',
            'api': 'fapi'
        },
        '_request_futures_data_api': {
            'type': 'futures',
            'api': 'futures/data'
        },
        '_request_futures_coin_api': {
            'type': 'coin',
            'api': 'dapi'
        },
        '_request_futures_coin_data_api': {
            'type': 'coin',
            'api': 'futures/data'
        },
        '_request_options_api': {
            'type': 'options',
            'api': 'eapi'
        },
        '_request_papi_api': {
            'type': 'portfolio',
            'api': 'papi'
        }
    }
    const result = funcs[func]
    return result ? [ result['type'], result['api'] ] : [ undefined, undefined ]
}

function compareEndpoints (docs, binance) {
    let missingInDocs = {}
    let missingInBinance = {}
    for (let type in docs) {
        missingInDocs[type] = []
        missingInBinance[type] = []
        const d = docs[type]
        const b = binance[type]
        const docsEndpoints = Object.keys (d)
        const binanceEndpoints = Object.keys (b)
        let found = false
        for (let key of docsEndpoints) {
            const dEntry = d[key]
            found = endpointIsInObject (dEntry, b)
            if (!found) {
                missingInBinance[type].push (dEntry)
            }
        }
        for (let key of binanceEndpoints) {
            const bEntry = b[key]
            found = endpointIsInObject (bEntry, d)
            if (!found) {
                missingInDocs[type].push (bEntry)
            }
        }
        console.log (type + '\nmissing in docs: ' + missingInDocs[type].length, '\nmissing in binance: ' + missingInBinance[type].length + '\ntotal in docs', docsEndpoints.length, '\ntotal in binance', binanceEndpoints.length)
    }
    return { missingInDocs, missingInBinance }
}

function endpointIsInObject (endpoint, object) {
    let found = false
    if (object[endpoint]) {
        found = true
    }
    const keys = Object.keys (object)
    for (let key of keys) {
        const entry = object[key]
        if (entry.method === endpoint.method &&
            entry.path === endpoint.path &&
            entry.api === endpoint.api) {
            found = true
            break
        }
    }
    return found
}

function parsePath (path) {
    path = path.replaceAll ('-', '_').replaceAll ('/', '_')
    const capitalMatch = /[A-Z]/g
    const capitalMatches = path.match (capitalMatch)
    if (capitalMatches) {
        for (let match of capitalMatches) {
            path = path.replace (match, '_' + match.toLowerCase ())
        }
    }
    return path
}

function generateMethodName (parsedEndpoint) {
    let { type, method, path, api } = parsedEndpoint
    let prefix = PREFIXES[type][api]
    if (prefix) {
        prefix += '_'
    } else { // if spot api
        prefix = ''
    }
    const methods = {
        'get': 'get_',
        'post': 'create_',
        'put': 'modify_',
        'delete': 'cancel_'
    }
    method = methods[method]
    if (method === 'get_' && api !== 'api') {
        method = ''
    }
    path = parsePath (path)
    return prefix + method + path
}

function generateMethodString (parsedEndpoint) {
    let result =
        parsedEndpoint.methodName + ' (self, **params):\n' + '    """\n    ' +
        parsedEndpoint.endpoint + '\n    """\n' +
        '    return ' + parsedEndpoint.call + '\n'
    return result
}

function main (generateNewEndpoints = false, writeNewFiles = false) {
    let endpoints = {}
    if (generateNewEndpoints) {
        const endpoints = generateListsOfEndpoints (writeNewFiles)
    } else {
        for (let type in ENPOINTS_FILES) {
            let file = ENPOINTS_FILES[type]
            const data = fs.readFileSync (file, 'utf8')
            endpoints[type] = data.split ('\n')
        }
    }
    const calls = getCallsFromBinanceFile ()
    const binanceMethods = {}
    calls.forEach ((call) => {
        const parsedCall = parseCall (call)
        if (parsedCall.type) {
            if (!binanceMethods[parsedCall.type]) {
                binanceMethods[parsedCall.type] = {}
            }
            binanceMethods[parsedCall.type][parsedCall.endpoint] = parsedCall
        }
    })
    const docsMethods = parseEndpoints (endpoints)
    const { missingInDocs, missingInBinance } = compareEndpoints (docsMethods, binanceMethods)
    let targetData = ''
    let total = 0
    for (let type in missingInBinance) {
        targetData += '#' + type + ' ====================\n\n'
        for (let method of missingInBinance[type]) {
            targetData += generateMethodString (method) + '\n'
            total++
        }
    }
    console.log ('Total missing in Binance: ' + total)
    fs.writeFile (TARGET_FILE_NAME, targetData, (err) => {
        if (err) {
            console.error (err)
            return
        }
        console.log (TARGET_FILE_NAME + ' file is generated')
    })
}

main ()
