
```win-shell
Get-NetTCPConnection -LocalPort 8765

LocalAddress                        LocalPort RemoteAddress                       RemotePort State       AppliedSetting OwningProcess
------------                        --------- -------------                       ---------- -----       -------------- -------------
0.0.0.0                             8765      0.0.0.0                             0          Listen                     23324
```

# so if want to release 8765

```
Stop-Process -Id 23324 -Force
```