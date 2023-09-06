# webroot-cli-py
WebRoot Python command-line interface.

Extract informations from WebRoot.


# Usage
```
./webroot-cli.py --help
options:
  -h, --help       show this help message and exit
  --client CLIENT  Choose the GSM key (default: exo)
  --active         Choose active endpoints only (default: False)
  --last           Check not seen for 7 days (default: False)
  --debug          Debug information (default: False)
  --noverbose      Verbose (default: False)


./webroot-cli.py --noverbose
Date: 2023-09-07
Deactivated    DeviceType    OS                                            HostName                  CurrentUser             IPAddress        IPV4            MACAddress         PrimaryBrowser    Workgroup    IsFirewallEnabled    ClientVersion    AttentionRequired    Infected      ActiveThreats  Managed    HasBeenInfected      ThreatsRemoved  ScheduledScansEnabled    LastSeen             LastScan              LastDeepScan
-------------  ------------  --------------------------------------------  ------------------------  ----------------------  ---------------  --------------  -----------------  ----------------  -----------  -------------------  ---------------  -------------------  ----------  ---------------  ---------  -----------------  ----------------  -----------------------  -------------------  --------------------  --------------------
False          Mac           13.5.1                                        LAPTOP01                  Titi01                  Xxx.Xx.XxX.XxX   Xxx.Xx.XxX.XxX  XX:XX:XX:XX:XX:XX  safari            WORKGROUP    False                9.5.8.209        False                False                     0  True       False                             0  True                     2023-09-06T21:33:01  2023-09-06T08:00:34Z  None
False          PC            Windows 11.0 (Build 22621) 64bit              LAPTOP02                  Titi02                  Xxx.Xx.XxX.XxX   Xxx.Xx.XxX.XxX  XX:XX:XX:XX:XX:XX                    WORKGROUP    True                 9.0.35.12        False                False                     0  True       False                             0  True
...

./webroot-cli.py --client exo --active --last --noverbose
```


# History
Still in quick & dirty dev phase!
