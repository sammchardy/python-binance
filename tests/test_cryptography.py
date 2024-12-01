from binance.client import Client

test_cases = [
    {
        "description": "Unencrypted PKCS8 ed22519 private key",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIPQmzwVKJETqVd7L9E/DFbkvrOigy1tLL+9QF0mSn6dV\n-----END PRIVATE KEY-----\n",
        "password": None,
        "expected_signature": "a4Pm3p02D2HXtNfo3DBaVCe9Ov7kledewgYtGjekotFmZ5wXa3mC5AtLB7CpAphyNjeyovIuDP+9fyjYmsojCw==",
    },
    {
        "description": "Unencrypted PKCS8 ed22519 private key in bytes",
        "private_key": b"-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIPQmzwVKJETqVd7L9E/DFbkvrOigy1tLL+9QF0mSn6dV\n-----END PRIVATE KEY-----\n",
        "password": None,
        "expected_signature": "a4Pm3p02D2HXtNfo3DBaVCe9Ov7kledewgYtGjekotFmZ5wXa3mC5AtLB7CpAphyNjeyovIuDP+9fyjYmsojCw==",
    },
    {
        "description": "Encrypted PKCS8 RSA private key",
        "private_key": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFNTBfBgkqhkiG9w0BBQ0wUjAxBgkqhkiG9w0BBQwwJAQQWW+iEMYYCPUntrPq\nZ2RCMAICCAAwDAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEEIw3ViSuTp8JeN43\n5VGlHt0EggTQBvEzd2w2F561CzU+MDouZDOPj4RTIStC471z0/bxTgYqH3gYchoe\nOfi2lsLuD8B+ivIRuXB8GT66BIseIOMV8t/tiMe97rFI/cV4h6DrBO1xlmSrBG97\nvFF9qPA5yPRlrHtWKkGxhXteNVsT3w/7Y7KsulO/gA2KpsOElMElOhUP462Yd0Wl\nOxAIV3+knl2niozws2Kq3EdzTF3N6hlavUPryiU/w4RRsPN5qgjchVVLq/sYRYhx\nN8uWJbkjhCcHsULkD5KkdgddR0VOhpQPXIdY+gPkSBJq1ltRWy/TYdXiU2fEBNZW\nhFUVrxnS76+u2R3vukY2IAX8zTC6h2AbCBG+r4XXzgk/l/4peySKHsPQRzQ0in39\na9o5sctOmUNeD4uJ6cClXDdqyEwXhnPmRKZjJ8qeH4D9wl7HOG7iQsYiyfJe/igi\nFEXVRZOtLBdbwX45rU6wiWWjxzY+mDnw4BXE31ZBPwgtoh+CLTyK8NI8LnCV/CgO\nzOY4sm/KDWmbfTTZjLSdYRFj7wEpOdUWjZ13viDFZqnmy/o1auvLmBcqbRrCyW+B\nOMI7aHE0mZ/52vEFQYU1tH0BxMmRfWXUCJj0TjwxDY6BQmmW4YlhsrgGNekLFDo1\n6phFd0pA4UPqGXfNLzHp1dtLhUEb4YzcpDn+HMzMf1gfez7qeqU28nNFg/AwwqHZ\nTWdGclCFjiah7SfvOslob4vdLGwkUhgCBKQUQoU1DltX2GOgIv9SNY3q6X0NwdZG\nL5gqk225WVUwIRzmi5nfUEXlbaTvyHg3BuGedUKJ91IhRCW1ZjvU8GQcfVsu8bse\nTCKMdr7wi/zEZXSldCza6vL4m3tmBLtWkHVOW8bcDWvoVwRswbFHfleHzckl7EeC\n9C4TRa66gA5UOv14SrpC8noQUNpSegg+1KI4BSNvwaheiSUqjQbisb0qYCxML0ZP\nmQodwVsXG6LYo+Y6y6CpHbT7UYkfa59q/CGOZByL1bEzzgd98ZHwjihOjHVaV6sY\nBW018AvGxr7kjEU4LNqIteydTp0o31ZJN/qK78w5EQFfJxfImrx/E4nYKtg4higj\nKOQCgJALKIveidqQEFsbGWsulYrMXwnu0nPThofR1D8eCJZpdTxvOh2nIrNrAeY8\nZMAwG1uQos5A0yEZ1auHxz+rb4errnk92OnVlWnElf1TwwlkFFNLdNDl8VpiMP40\n6en9VtlOfgH8AwB03WsoeuEQsxYTIcRKWZZPRsLx3hd0BsOw0FcYDSX2XIGPkVVW\niYf9hzFSQsWV3d6utloIm4nG8XONfNaRimGECbUSZyHZimrO1m4Gga5pE3LKuDri\nJKR2lR7b6XPR7+FS+lG1zq5KY7onAVQY1oABfTjpJRju6pQGWt70hairo6EaVC3u\nrBy8UkLwBbfDuigSvsVk+sF2+Ic0IzX6IniU0F5kMe+MKqGB4aicXP6FFGBpPFTe\nv6yHD+DYAu1rnlXrqmFL50CfutTF78uPPJ9D2Sm0DcGPFj+6IrCigj48uxoHR9Qb\nFeNzfsmVwoFAWWq/MpkPbX6Aql8ddCbpMxDUUkybwVV9rJmEMTLil44FrxKAKFhP\n0Av7JeFvdz15pfnf/IQ3IOvVhHGFChFS13sbYSvFHMQF3P0BiyvjhBI=\n-----END ENCRYPTED PRIVATE KEY-----\n",
        "password": "testpwd",
        "expected_signature": "S4l9IONXGHIdt4NjwmpCIhawDTitjUQls73d+mi0HJTSbTGyn95NabX5hC9+n6HsTqLcWPvxKgTvLFMnTaf6Jxl+xwQMbu9/6mw88KF7i1pEQizerKcr91rPUPVBQ4OY10Q018QEamIAymRgo/eoRYSm7CqCdeibGyO0XfXZBaJnVGFJ9hgrPIwSKHgeUnfK8qMenULvL0qKMEJ6ziYPiqh7k9xX3xIV7lGIpokk+ekqlFd01f/Lov45osJCFuccJO4xuUUZewZnVGF7Uw6Rim3UsKhXKZUN9WZWa5RT+dpBIJ5DTBIXBSvowwj3GZC3j+XvWw8Sn0Ls9836l89BXw==",
    },
    {
        "description": "Encrypted PKCS8 RSA private key in bytes",
        "private_key": b"-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFNTBfBgkqhkiG9w0BBQ0wUjAxBgkqhkiG9w0BBQwwJAQQWW+iEMYYCPUntrPq\nZ2RCMAICCAAwDAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEEIw3ViSuTp8JeN43\n5VGlHt0EggTQBvEzd2w2F561CzU+MDouZDOPj4RTIStC471z0/bxTgYqH3gYchoe\nOfi2lsLuD8B+ivIRuXB8GT66BIseIOMV8t/tiMe97rFI/cV4h6DrBO1xlmSrBG97\nvFF9qPA5yPRlrHtWKkGxhXteNVsT3w/7Y7KsulO/gA2KpsOElMElOhUP462Yd0Wl\nOxAIV3+knl2niozws2Kq3EdzTF3N6hlavUPryiU/w4RRsPN5qgjchVVLq/sYRYhx\nN8uWJbkjhCcHsULkD5KkdgddR0VOhpQPXIdY+gPkSBJq1ltRWy/TYdXiU2fEBNZW\nhFUVrxnS76+u2R3vukY2IAX8zTC6h2AbCBG+r4XXzgk/l/4peySKHsPQRzQ0in39\na9o5sctOmUNeD4uJ6cClXDdqyEwXhnPmRKZjJ8qeH4D9wl7HOG7iQsYiyfJe/igi\nFEXVRZOtLBdbwX45rU6wiWWjxzY+mDnw4BXE31ZBPwgtoh+CLTyK8NI8LnCV/CgO\nzOY4sm/KDWmbfTTZjLSdYRFj7wEpOdUWjZ13viDFZqnmy/o1auvLmBcqbRrCyW+B\nOMI7aHE0mZ/52vEFQYU1tH0BxMmRfWXUCJj0TjwxDY6BQmmW4YlhsrgGNekLFDo1\n6phFd0pA4UPqGXfNLzHp1dtLhUEb4YzcpDn+HMzMf1gfez7qeqU28nNFg/AwwqHZ\nTWdGclCFjiah7SfvOslob4vdLGwkUhgCBKQUQoU1DltX2GOgIv9SNY3q6X0NwdZG\nL5gqk225WVUwIRzmi5nfUEXlbaTvyHg3BuGedUKJ91IhRCW1ZjvU8GQcfVsu8bse\nTCKMdr7wi/zEZXSldCza6vL4m3tmBLtWkHVOW8bcDWvoVwRswbFHfleHzckl7EeC\n9C4TRa66gA5UOv14SrpC8noQUNpSegg+1KI4BSNvwaheiSUqjQbisb0qYCxML0ZP\nmQodwVsXG6LYo+Y6y6CpHbT7UYkfa59q/CGOZByL1bEzzgd98ZHwjihOjHVaV6sY\nBW018AvGxr7kjEU4LNqIteydTp0o31ZJN/qK78w5EQFfJxfImrx/E4nYKtg4higj\nKOQCgJALKIveidqQEFsbGWsulYrMXwnu0nPThofR1D8eCJZpdTxvOh2nIrNrAeY8\nZMAwG1uQos5A0yEZ1auHxz+rb4errnk92OnVlWnElf1TwwlkFFNLdNDl8VpiMP40\n6en9VtlOfgH8AwB03WsoeuEQsxYTIcRKWZZPRsLx3hd0BsOw0FcYDSX2XIGPkVVW\niYf9hzFSQsWV3d6utloIm4nG8XONfNaRimGECbUSZyHZimrO1m4Gga5pE3LKuDri\nJKR2lR7b6XPR7+FS+lG1zq5KY7onAVQY1oABfTjpJRju6pQGWt70hairo6EaVC3u\nrBy8UkLwBbfDuigSvsVk+sF2+Ic0IzX6IniU0F5kMe+MKqGB4aicXP6FFGBpPFTe\nv6yHD+DYAu1rnlXrqmFL50CfutTF78uPPJ9D2Sm0DcGPFj+6IrCigj48uxoHR9Qb\nFeNzfsmVwoFAWWq/MpkPbX6Aql8ddCbpMxDUUkybwVV9rJmEMTLil44FrxKAKFhP\n0Av7JeFvdz15pfnf/IQ3IOvVhHGFChFS13sbYSvFHMQF3P0BiyvjhBI=\n-----END ENCRYPTED PRIVATE KEY-----\n",
        "password": "testpwd",
        "expected_signature": "S4l9IONXGHIdt4NjwmpCIhawDTitjUQls73d+mi0HJTSbTGyn95NabX5hC9+n6HsTqLcWPvxKgTvLFMnTaf6Jxl+xwQMbu9/6mw88KF7i1pEQizerKcr91rPUPVBQ4OY10Q018QEamIAymRgo/eoRYSm7CqCdeibGyO0XfXZBaJnVGFJ9hgrPIwSKHgeUnfK8qMenULvL0qKMEJ6ziYPiqh7k9xX3xIV7lGIpokk+ekqlFd01f/Lov45osJCFuccJO4xuUUZewZnVGF7Uw6Rim3UsKhXKZUN9WZWa5RT+dpBIJ5DTBIXBSvowwj3GZC3j+XvWw8Sn0Ls9836l89BXw==",
    },
]


def test_encryption():
    data = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "quantity": 1,
        "timestamp": 1631234567890,
        "price": 50000,
    }

    for case in test_cases:
        client = Client(
            api_key="api_key",
            api_secret="api_secret",
            private_key=case["private_key"],
            private_key_pass=case["password"],
            ping=False,
        )
        signature = client._generate_signature(data, False)
        assert signature == case["expected_signature"], (
            f"Test failed: {case['description']}"
        )
