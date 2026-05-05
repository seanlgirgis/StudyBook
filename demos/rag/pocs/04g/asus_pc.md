(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> # NVIDIA SMI — driver, memory, GPU usage
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> nvidia-smi
Tue May  5 01:51:14 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 581.95                 Driver Version: 581.95         CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060      WDDM  |   00000000:01:00.0  On |                  N/A |
| 40%   38C    P8             17W /  170W |    2139MiB /  12288MiB |      5%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A            2436    C+G   ...crosoft\OneDrive\OneDrive.exe      N/A      |
|    0   N/A  N/A            6472    C+G   C:\Windows\explorer.exe               N/A      |
|    0   N/A  N/A            6788    C+G   ...2txyewy\CrossDeviceResume.exe      N/A      |
|    0   N/A  N/A            8568    C+G   ...lus\logioptionsplus_agent.exe      N/A      |
|    0   N/A  N/A            8892    C+G   ...indows\System32\ShellHost.exe      N/A      |
|    0   N/A  N/A            9080    C+G   ...hSmith\Snagit 13\Snagit32.exe      N/A      |
|    0   N/A  N/A           14584    C+G   ...t\Edge\Application\msedge.exe      N/A      |
|    0   N/A  N/A           14764    C+G   ...yb3d8bbwe\WindowsTerminal.exe      N/A      |
|    0   N/A  N/A           15468    C+G   C:\Windows\explorer.exe               N/A      |
|    0   N/A  N/A           17956    C+G   ...Toys\PowerToys.FancyZones.exe      N/A      |
|    0   N/A  N/A           19664    C+G   ....0.3912.98\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           20092    C+G   ..._cw5n1h2txyewy\SearchHost.exe      N/A      |
|    0   N/A  N/A           20100    C+G   ...y\StartMenuExperienceHost.exe      N/A      |
|    0   N/A  N/A           20744    C+G   ...Local\PowerToys\PowerToys.exe      N/A      |
|    0   N/A  N/A           21356    C+G   ...pps\PowerToys.QuickAccess.exe      N/A      |
|    0   N/A  N/A           22216    C+G   ...xyewy\ShellExperienceHost.exe      N/A      |
|    0   N/A  N/A           22284    C+G   ....0.3912.98\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           22984    C+G   ....0.3912.98\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           25436    C+G   ...8bbwe\Microsoft.CmdPal.UI.exe      N/A      |
|    0   N/A  N/A           26188    C+G   ...s\PowerToys.AdvancedPaste.exe      N/A      |
|    0   N/A  N/A           26392    C+G   ...s\PowerToys.ColorPickerUI.exe      N/A      |
|    0   N/A  N/A           27396    C+G   ...5n1h2txyewy\TextInputHost.exe      N/A      |
|    0   N/A  N/A           27452    C+G   ...UI3Apps\PowerToys.Peek.UI.exe      N/A      |
|    0   N/A  N/A           27636    C+G   ....0.3912.98\msedgewebview2.exe      N/A      |
|    0   N/A  N/A           28100    C+G   ...s\PowerToys.PowerLauncher.exe      N/A      |
|    0   N/A  N/A           28540    C+G   ...indows\System32\ShellHost.exe      N/A      |
|    0   N/A  N/A           29972    C+G   ...__2p2nqsd0c76g0\app\Codex.exe      N/A      |
|    0   N/A  N/A           30656    C+G   ...al\Programs\Notion\Notion.exe      N/A      |
|    0   N/A  N/A           32072    C+G   ...8wekyb3d8bbwe\M365Copilot.exe      N/A      |
|    0   N/A  N/A           32124    C+G   ...t\Edge\Application\msedge.exe      N/A      |
|    0   N/A  N/A           32876    C+G   ...Files\Bitwarden\Bitwarden.exe      N/A      |
|    0   N/A  N/A           35152    C+G   ...Chrome\Application\chrome.exe      N/A      |
|    0   N/A  N/A           35172    C+G   ...th\Snagit 13\SnagitEditor.exe      N/A      |
|    0   N/A  N/A           36360    C+G   ...ass\app-1.36.1\ProtonPass.exe      N/A      |
|    0   N/A  N/A           37988    C+G   C:\Windows\explorer.exe               N/A      |
|    0   N/A  N/A           38580    C+G   ...r\frontend\Docker Desktop.exe      N/A      |
|    0   N/A  N/A           41516    C+G   ...Files\Notepad++\notepad++.exe      N/A      |
|    0   N/A  N/A           43708    C+G   ...x64__8wekyb3d8bbwe\Photos.exe      N/A      |
|    0   N/A  N/A           43760    C+G   ...x64__8wekyb3d8bbwe\Photos.exe      N/A      |
|    0   N/A  N/A           44996    C+G   ...8bbwe\PhoneExperienceHost.exe      N/A      |
|    0   N/A  N/A           46120    C+G   ...Chrome\Application\chrome.exe      N/A      |
+-----------------------------------------------------------------------------------------+
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device count:', torch.cuda.device_count()); print('Device name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU'); print('PyTorch version:', torch.__version__)"
CUDA available: False
Device count: 0
Device name: No GPU
PyTorch version: 2.10.0+cpu
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> # Number of logical processors and cores
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors

Name                                 NumberOfCores NumberOfLogicalProcessors
----                                 ------------- -------------------------
12th Gen Intel(R) Core(TM) i7-12700F            12                        20

(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> # Total physical memory
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> Get-WmiObject Win32_ComputerSystem | Select-Object TotalPhysicalMemory

TotalPhysicalMemory
-------------------
        68523835392

(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> # Free memory
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> Get-WmiObject Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize

FreePhysicalMemory TotalVisibleMemorySize
------------------ ----------------------
          34376024               66917808

(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> python --version
Python 3.12.9
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> pip list
Package                            Version
---------------------------------- -----------
accelerate                         1.13.0
aiohappyeyeballs                   2.6.1
aiohttp                            3.13.3
aiosignal                          1.4.0
annotated-doc                      0.0.4
annotated-types                    0.7.0
anyio                              3.7.1
argon2-cffi                        25.1.0
argon2-cffi-bindings               25.1.0
arrow                              1.4.0
asttokens                          3.0.1
async-lru                          2.1.0
attrs                              25.4.0
babel                              2.18.0
beautifulsoup4                     4.14.3
bitsandbytes                       0.49.2
black                              26.1.0
bleach                             6.3.0
certifi                            2026.1.4
cffi                               2.0.0
charset-normalizer                 3.4.4
click                              8.3.1
colorama                           0.4.6
comm                               0.2.3
debugpy                            1.8.20
decorator                          5.2.1
defusedxml                         0.7.1
distro                             1.9.0
dnspython                          2.8.0
docx2pdf                           0.1.8
email-validator                    2.3.0
executing                          2.2.1
faiss-cpu                          1.13.2
fastapi                            0.111.0
fastapi-cli                        0.0.24
fastjsonschema                     2.21.2
filelock                           3.20.3
fqdn                               1.5.1
frozenlist                         1.8.0
fsspec                             2026.2.0
googleapis-common-protos           1.72.0
grpcio                             1.76.0
h11                                0.16.0
hf-xet                             1.2.0
httpcore                           1.0.9
httptools                          0.7.1
httpx                              0.28.1
huggingface_hub                    1.4.1
idna                               3.11
importlib_metadata                 8.7.1
ipykernel                          7.1.0
ipython                            9.10.0
ipython_pygments_lexers            1.1.1
ipywidgets                         8.1.8
isoduration                        20.11.0
isort                              7.0.0
jedi                               0.19.2
Jinja2                             3.1.6
jiter                              0.13.0
joblib                             1.5.3
json5                              0.13.0
jsonpointer                        3.0.0
jsonschema                         4.26.0
jsonschema-specifications          2025.9.1
jupyter                            1.1.1
jupyter_client                     8.8.0
jupyter-console                    6.6.3
jupyter_core                       5.9.1
jupyter-events                     0.12.0
jupyter-lsp                        2.3.0
jupyter_server                     2.17.0
jupyter_server_terminals           0.5.4
jupyterlab                         4.5.3
jupyterlab_pygments                0.3.0
jupyterlab_server                  2.28.0
jupyterlab_widgets                 3.0.16
lark                               1.3.1
Levenshtein                        0.27.3
librt                              0.7.8
lxml                               6.0.2
markdown-it-py                     4.0.0
MarkupSafe                         3.0.3
matplotlib-inline                  0.2.1
mdurl                              0.1.2
mistune                            3.2.0
mpmath                             1.3.0
multidict                          6.7.1
mypy                               1.19.1
mypy_extensions                    1.1.0
nbclient                           0.10.4
nbconvert                          7.17.0
nbformat                           5.10.4
nest-asyncio                       1.6.0
networkx                           3.6.1
nltk                               3.9.4
notebook                           7.5.3
notebook_shim                      0.2.4
numpy                              2.4.2
openai                             1.2.3
opentelemetry-api                  1.39.1
opentelemetry-sdk                  1.39.1
opentelemetry-semantic-conventions 0.60b1
orjson                             3.11.8
packaging                          25.0
pandas                             3.0.0
pandocfilters                      1.5.1
parso                              0.8.5
pathspec                           1.0.4
pip                                26.0
platformdirs                       4.5.1
prometheus_client                  0.24.1
prompt_toolkit                     3.0.52
propcache                          0.4.1
protobuf                           6.33.5
psutil                             7.2.2
psycopg2-binary                    2.9.11
pure_eval                          0.2.3
pyaml                              25.7.0
pycparser                          3.0
pydantic                           2.12.5
pydantic_core                      2.41.5
Pygments                           2.19.2
python-dateutil                    2.9.0.post0
python-docx                        1.2.0
python-dotenv                      1.2.1
python-json-logger                 4.0.0
python-Levenshtein                 0.27.3
python-multipart                   0.0.27
pytokens                           0.4.1
pywin32                            311
pywinpty                           3.0.2
PyYAML                             6.0.3
pyzmq                              27.1.0
RapidFuzz                          3.14.5
referencing                        0.37.0
regex                              2026.1.15
requests                           2.32.5
rfc3339-validator                  0.1.4
rfc3986-validator                  0.1.1
rfc3987-syntax                     1.1.0
rich                               15.0.0
rich-toolkit                       0.19.7
rpds-py                            0.30.0
ruff                               0.15.0
safetensors                        0.7.0
scikit-learn                       1.8.0
scipy                              1.17.0
Send2Trash                         2.1.0
sentence-transformers              5.2.2
setuptools                         80.10.2
shellingham                        1.5.4
six                                1.17.0
sniffio                            1.3.1
soupsieve                          2.8.3
stack-data                         0.6.3
starlette                          0.37.2
sympy                              1.14.0
terminado                          0.18.1
threadpoolctl                      3.6.0
tinycss2                           1.4.0
tokenizers                         0.22.2
torch                              2.10.0
tornado                            6.5.4
tqdm                               4.67.3
traitlets                          5.14.3
transformers                       5.1.0
typer                              0.25.1
typer-slim                         0.21.1
typing_extensions                  4.15.0
typing-inspection                  0.4.2
tzdata                             2025.3
ujson                              5.12.0
uri-template                       1.3.0
urllib3                            2.6.3
uvicorn                            0.23.2
watchfiles                         1.1.1
wcwidth                            0.5.3
webcolors                          25.10.0
webencodings                       0.5.1
websocket-client                   1.9.0
websockets                         16.0
widgetsnbextension                 4.0.15
xai-sdk                            1.6.1
yarl                               1.22.0
zipp                               3.23.0
(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs> Get-PSDrive C | Select-Object Used, Free, Provider, Root

        Used        Free Provider                             Root
        ----        ---- --------                             ----
431301480448 55770615808 Microsoft.PowerShell.Core\FileSystem C:\

(JobSearch) PS D:\Workarea\StudyBook\demos\rag\pocs>