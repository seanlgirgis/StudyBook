# AI Lab PC Diagnostics Report

Generated: 2026-05-21 12:54:11 -05:00
Host Context: ASUSPC / shareuser


## Basic System

```text
asuspc
asuspc\shareuser

WindowsProductName    : Windows 10 Pro
WindowsVersion        : 2009
OsBuildNumber         : 26200
CsManufacturer        : ASUSTeK COMPUTER INC.
CsModel               : ROG STRIX G15CF_G15CF
CsProcessors          : {12th Gen Intel(R) Core(TM) i7-12700F}
CsTotalPhysicalMemory : 68523835392
```

## CPU

```text

Name                      : 12th Gen Intel(R) Core(TM) i7-12700F
NumberOfCores             : 12
NumberOfLogicalProcessors : 20
MaxClockSpeed             : 2100
```

## RAM

```text

BankLabel Manufacturer    Capacity Speed PartNumber
--------- ------------    -------- ----- ----------
BANK 0    Corsair      34359738368  2133 CMK64GX4M2E3200C16  
BANK 0    Corsair      34359738368  2133 CMK64GX4M2E3200C16
```

## Disks

```text

Number FriendlyName                   SerialNumber                                     BusType MediaType           Size
------ ------------                   ------------                                     ------- ---------           ----
     1 TOSHIBA DT01ACA100                        913KL4YMS                             SATA               1000204886016
     3 JMicron Generic                0123456789ABCDEF                                 USB                1000204886016
     0 NVMe Micron_3400_MTFDKBA512TFH 0000_0000_0000_0001_00A0_7521_330E_377E.         NVMe                512110190592
     2 Seagate Expansion HDD              00000000NT172DVN                             USB               14000519642624
```

## Volumes

```text

DriveLetter FileSystemLabel FileSystem           Size  SizeRemaining
----------- --------------- ----------           ----  -------------
          C OS              NTFS         487072272384   143169257472
          D DATA            NTFS        1000203087872   842951294976
          F Docking         NTFS        1000186310656   940004442112
          E Expansion       exFAT      14000072949760 13947558952960
                            NTFS            914354176       85606400
            MYASUS          FAT32           205520896      147171328
            RESTORE         NTFS          23622316032     7901380608
```

## GPU NVIDIA-SMI

```text
Thu May 21 12:54:19 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 581.95                 Driver Version: 581.95         CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060      WDDM  |   00000000:01:00.0  On |                  N/A |
| 40%   40C    P8             17W /  170W |    3917MiB /  12288MiB |      9%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A            2664    C+G   ...r\frontend\Docker Desktop.exe      N/A      |
|    0   N/A  N/A            5356    C+G   ...8bbwe\Microsoft.CmdPal.UI.exe      N/A      |
|    0   N/A  N/A            5392    C+G   ...2txyewy\CrossDeviceResume.exe      N/A      |
|    0   N/A  N/A            7728    C+G   ...8wekyb3d8bbwe\M365Copilot.exe      N/A      |
|    0   N/A  N/A           10400    C+G   ...Toys\PowerToys.FancyZones.exe      N/A      |
|    0   N/A  N/A           10784    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           11728    C+G   ...yb3d8bbwe\WindowsTerminal.exe      N/A      |
|    0   N/A  N/A           14508    C+G   C:\Windows\explorer.exe               N/A      |
|    0   N/A  N/A           14732    C+G   ...lus\logioptionsplus_agent.exe      N/A      |
|    0   N/A  N/A           18564    C+G   ..._cw5n1h2txyewy\SearchHost.exe      N/A      |
|    0   N/A  N/A           18592    C+G   ...y\StartMenuExperienceHost.exe      N/A      |
|    0   N/A  N/A           20172    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           21560    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           21840    C+G   ...Local\PowerToys\PowerToys.exe      N/A      |
|    0   N/A  N/A           22024    C+G   ...th\Snagit 13\SnagitEditor.exe      N/A      |
|    0   N/A  N/A           22300    C+G   ...Files\Notepad++\notepad++.exe      N/A      |
|    0   N/A  N/A           22384    C+G   ...pps\PowerToys.QuickAccess.exe      N/A      |
|    0   N/A  N/A           23140    C+G   ...hSmith\Snagit 13\Snagit32.exe      N/A      |
|    0   N/A  N/A           23528    C+G   ...s\PowerToys.ColorPickerUI.exe      N/A      |
|    0   N/A  N/A           24052    C+G   ...5n1h2txyewy\TextInputHost.exe      N/A      |
|    0   N/A  N/A           24168    C+G   ...t\Edge\Application\msedge.exe      N/A      |
|    0   N/A  N/A           25092    C+G   ...8bbwe\PhoneExperienceHost.exe      N/A      |
|    0   N/A  N/A           25180    C+G   ...UI3Apps\PowerToys.Peek.UI.exe      N/A      |
|    0   N/A  N/A           25716    C+G   ...s\PowerToys.PowerLauncher.exe      N/A      |
|    0   N/A  N/A           28440    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           29172    C+G   ...al\Programs\Notion\Notion.exe      N/A      |
|    0   N/A  N/A           29376    C+G   ...__2p2nqsd0c76g0\app\Codex.exe      N/A      |
|    0   N/A  N/A           31464    C+G   ...t\Edge\Application\msedge.exe      N/A      |
|    0   N/A  N/A           31608    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           32392    C+G   ...4__8wekyb3d8bbwe\ms-teams.exe      N/A      |
|    0   N/A  N/A           36268    C+G   ....0.3967.70\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           36368    C+G   ...crosoft\OneDrive\OneDrive.exe      N/A      |
|    0   N/A  N/A           38180    C+G   ...C\Acrobat\AcroCEF\AcroCEF.exe      N/A      |
|    0   N/A  N/A           45168    C+G   ...indows\System32\ShellHost.exe      N/A      |
+-----------------------------------------------------------------------------------------+
```

## GPU Windows

```text

Name           : NVIDIA GeForce RTX 3060
AdapterRAM     : 4293918720
DriverVersion  : 32.0.15.8195
VideoProcessor : NVIDIA GeForce RTX 3060
```

## Motherboard

```text

Manufacturer : ASUSTeK COMPUTER INC.
Product      : G15CF
SerialNumber : 220199193102216
Version      : 1.0
```

## BIOS

```text

Manufacturer      : American Megatrends Inc.
SMBIOSBIOSVersion : G15CF.300
ReleaseDate       : 1/4/2022 6:00:00 PM
```

## Power Plan

```text
Power Scheme GUID: b0f6ca61-62cb-4b9a-bd4c-bc7b4be1dbe9  (ASUS Recommended)
```

## Virtualization Support

```text
                               [07]: Hyper-V Virtual Ethernet Adapter
Virtualization-based security: Status: Running
                                     Base Virtualization Support
                                     APIC Virtualization
Hyper-V Requirements:          A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```

## WSL Status

```text
D e f a u l t   D i s t r i b u t i o n :   d o c k e r - d e s k t o p 
 
 D e f a u l t   V e r s i o n :   2 
 
 
    N A M E                             S T A T E                       V E R S I O N 
 
 *   d o c k e r - d e s k t o p         R u n n i n g                   2 
 
     U b u n t u                         S t o p p e d                   2 
 
 
```

## Docker Status

```text
Client:
 Version:           29.4.1
 API version:       1.54
 Go version:        go1.26.2
 Git commit:        055a478
 Built:             Mon Apr 20 16:35:45 2026
 OS/Arch:           windows/amd64
 Context:           desktop-linux

Server: Docker Desktop 4.71.0 (225177)
 Engine:
  Version:          29.4.1
  API version:      1.54 (minimum version 1.40)
  Go version:       go1.26.2
  Git commit:       6c91b92
  Built:            Mon Apr 20 16:32:41 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.3
  GitCommit:        77c84241c7cbdd9b4eca2591793e3d4f4317c590
 runc:
  Version:          1.3.5
  GitCommit:        v1.3.5-0-g488fc13e
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
Client:
 Version:    29.4.1
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  agent: Docker AI Agent Runner (Docker Inc.)
    Version:  v1.44.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-agent.exe
  ai: Docker AI Agent - Ask Gordon (Docker Inc.)
    Version:  v1.20.2
    Path:     C:\Program Files\Docker\cli-plugins\docker-ai.exe
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.33.0-desktop.1
    Path:     C:\Program Files\Docker\cli-plugins\docker-buildx.exe
  compose: Docker Compose (Docker Inc.)
    Version:  v5.1.3
    Path:     C:\Program Files\Docker\cli-plugins\docker-compose.exe
  debug: Get a shell into any image or container (Docker Inc.)
    Version:  0.0.47
    Path:     C:\Program Files\Docker\cli-plugins\docker-debug.exe
  desktop: Docker Desktop commands (Docker Inc.)
    Version:  v0.3.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-desktop.exe
  dhi: CLI for managing Docker Hardened Images (Docker Inc.)
    Version:  v0.0.2
    Path:     C:\Program Files\Docker\cli-plugins\docker-dhi.exe
  extension: Manages Docker extensions (Docker Inc.)
    Version:  v0.2.31
    Path:     C:\Program Files\Docker\cli-plugins\docker-extension.exe
  init: Creates Docker-related starter files for your project (Docker Inc.)
    Version:  v1.4.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-init.exe
  mcp: Docker MCP Plugin (Docker Inc.)
    Version:  v0.40.4
    Path:     C:\Program Files\Docker\cli-plugins\docker-mcp.exe
  model: Docker Model Runner (Docker Inc.)
    Version:  v1.1.36
    Path:     C:\Program Files\Docker\cli-plugins\docker-model.exe
  offload: Docker Offload (Docker Inc.)
    Version:  v0.5.85
    Path:     C:\Program Files\Docker\cli-plugins\docker-offload.exe
  pass: Docker Pass Secrets Manager Plugin (beta) (Docker Inc.)
    Version:  v0.0.25
    Path:     C:\Program Files\Docker\cli-plugins\docker-pass.exe
  sandbox: Docker Sandbox (Docker Inc.)
    Version:  v0.12.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-sandbox.exe
  sbom: View the packaged-based Software Bill Of Materials (SBOM) for an image (Anchore Inc.)
    Version:  0.6.0
    Path:     C:\Program Files\Docker\cli-plugins\docker-sbom.exe
  scout: Docker Scout (Docker Inc.)
    Version:  v1.20.4
    Path:     C:\Program Files\Docker\cli-plugins\docker-scout.exe

Server:
 Containers: 5
  Running: 3
  Paused: 0
  Stopped: 2
 Images: 5
 Server Version: 29.4.1
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Discovered Devices:
  cdi: docker.com/gpu=webgpu
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 77c84241c7cbdd9b4eca2591793e3d4f4317c590
 runc version: v1.3.5-0-g488fc13e
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.6.87.2-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 20
 Total Memory: 31.25GiB
 Name: docker-desktop
 ID: 42b4e7dc-b36e-486c-9dae-34276bab2b3f
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 HTTP Proxy: http.docker.internal:3128
 HTTPS Proxy: http.docker.internal:3128
 No Proxy: hubproxy.docker.internal
 Labels:
  com.docker.desktop.address=npipe://\\.\pipe\docker_cli
 Experimental: false
 Insecure Registries:
  hubproxy.docker.internal:5555
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Firewall Backend: iptables
```

## OneDrive Environment

```text

Name             Value
----             -----
OneDrive         D:\Users\shareuser\OneDrive
OneDriveConsumer D:\Users\shareuser\OneDrive

OneDrive=D:\Users\shareuser\OneDrive
OneDriveCommercial=
OneDriveConsumer=D:\Users\shareuser\OneDrive
```

