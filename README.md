# webroot-cli-py
WebRoot Python command-line interface.

Extract informations from WebRoot.


# Usage
```
./webroot-cli.py --help
options:
  -h, --help       show this help message and exit
  --client CLIENT  Choose the GSM key (default: exo)
  --endpoints      List endpoints (default: False)
  --active         Only active endpoints (default: False)
  --last           Only endpoints not seen for 7 days (default: False)
  --ping           Ping (default: False)
  --version        Version (default: False)
  --subscriptions  List subscriptions (default: False)
  --noheaders      No headers in the output (default: False)
  --debug          Debug information (default: False)
  --verbose        Verbose (default: False)


./webroot-cli.py --verbose
./webroot-cli.py --debug
./webroot-cli.py --ping --debug
./webroot-cli.py --version --debug
./webroot-cli.py --subscriptions --debug

./webroot-cli.py --endpoints
./webroot-cli.py --endpoints --active
./webroot-cli.py --endpoints --active --last
╭─────────────┬────────────┬──────────────────────────────────┬──────────┬─────────────┬─────────────────┬─────────────────┬───────────────────┬──────────────────┬─────────────┬─────────────────────┬─────────────────┬─────────────────────┬────────────┬─────────────────┬───────────┬───────────────────┬──────────────────┬─────────────────────────┬─────────────────────┬──────────────────────┬──────────────────────╮
│ Deactivated │ DeviceType │ OS                               │ HostName │ CurrentUser │ IPAddress       │ IPV4            │ MACAddress        │ PrimaryBrowser   │ Workgroup   │ IsFirewallEnabled   │ ClientVersion   │ AttentionRequired   │ Infected   │   ActiveThreats │ Managed   │ HasBeenInfected   │   ThreatsRemoved │ ScheduledScansEnabled   │ LastSeen            │ LastScan             │ LastDeepScan         │
├─────────────┼────────────┼──────────────────────────────────┼──────────┼─────────────┼─────────────────┼─────────────────┼───────────────────┼──────────────────┼─────────────┼─────────────────────┼─────────────────┼─────────────────────┼────────────┼─────────────────┼───────────┼───────────────────┼──────────────────┼─────────────────────────┼─────────────────────┼──────────────────────┼──────────────────────┤
│ False       │ Mac        │ 13.5.1                           │ LAPTOP01 │ User01      │ XxX.XxX.XxX.XxX │ XxX.XxX.XxX.XxX │ XX:XX:XX:XX:XX:XX │ safari           │ WORKGROUP   │ False               │ 9.5.8.209       │ False               │ False      │               0 │ True      │ False             │                0 │ True                    │ 2023-05-04T12:17:39 │ 2023-05-03T19:17:39Z │ None                 │
│ False       │ PC         │ Windows 11.0 (Build 22621) 64bit │ LAPTOP02 │ User02      │ XxX.XxX.XxX.XxX │ XxX.XxX.XxX.XxX │ XX:XX:XX:XX:XX:XX │                  │ WORKGROUP   │ True                │ 9.0.35.12       │ False               │ False      │               0 │ True      │ False             │                0 │ True                    │ 2023-07-07T15:52:10 │ 2023-07-02T08:00:00Z │ None                 │
│ ...         │            │                                  │          │             │                 │                 │                   │                  │             │                     │                 │                     │            │                 │           │                   │                  │                         │                     │                      │                      │
╰─────────────┴────────────┴──────────────────────────────────┴──────────┴─────────────┴─────────────────┴─────────────────┴───────────────────┴──────────────────┴─────────────┴─────────────────────┴─────────────────┴─────────────────────┴────────────┴─────────────────┴───────────┴───────────────────┴──────────────────┴─────────────────────────┴─────────────────────┴──────────────────────┴──────────────────────╯

./webroot-cli.py --client exo --endpoints --active --last
```


# History
Still in quick & dirty dev phase!
