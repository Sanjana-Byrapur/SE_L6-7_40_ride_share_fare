# Lab 7: Fuzz testing ride-share fares

The functions in `ride_share_fare.py` return `None` for invalid inputs. Valid
trip distances, fares, and promo values must be non-negative and finite. Fare
lists contain non-negative integers; their average is rounded down. The
payable fare is the original fare plus 18% tax, less the promo, with a minimum
of zero. Integer fare fields are limited to 1,000 characters.

Install and run the tests from this directory:

```sh
python3 -m pip install hypothesis pytest
python3 -m pytest test_ride_share_fare.py -q
python3 ride_share_fare.py
```

For the example application run, enter `sedan:12`, `120,95,210`, and
`250|30` at the three prompts.

## Reproducing the original failures

The following commands retrieve the original Lab 7 application from the
parent repository into a temporary directory, leaving the fixed code intact:

```sh
tmpdir=$(mktemp -d)
curl -fsSL 'https://raw.githubusercontent.com/SETAPESU26/L6_L7_40_ride_share_fare/main/Lab%207/ride_share_fare.py' -o "$tmpdir/ride_share_fare.py"
cp test_ride_share_fare.py "$tmpdir/"
python3 "$tmpdir/ride_share_fare.py"
python3 -m pytest "$tmpdir/test_ride_share_fare.py" -q --tb=no
```

Capture the original application output and failing tests, then the fixed
application output and passing tests, for the handout's screenshot PDF.
