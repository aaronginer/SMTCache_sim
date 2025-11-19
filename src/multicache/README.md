# Guide to using the Parse-Tool and the MultiCache testbed on AWS servers

### AWS machine setup

- The preferred Linux version is **Ubuntu 20.04**. Other versions/distros have not been tested and may not work.

##### Server

- For simplicity, use a security group (preferably a custom) that has all traffic enabled.
    1) "Edit inbound rules"
    2) "Add Rule":
        - Type: "All Traffic"
        - Source: "Anywhere-IPv4" + 0.0.0.0/0
    3) "Save Rules"

##### Client

- Default installation should be sufficient (other settings like memory according to needs)

### AWS server install installation

- Clone multicache repository: **https://extgit.iaik.tugraz.at/coresec_students/2021_bachelor_giner_cachesim.git**
- `cd ~/2021_bachelor_giner_cachesim/code/kernel && sudo ./installKernel.sh`
    - Server will reboot after the process has finished
- `cd ~/2021_bachelor_giner_cachesim/code/multicache/testbed && sudo ./installServer.sh`
    - After updates are done and dialog is installed, choose the server configuration you want in the dialog window
    - If you choose to install the smbd server (file-server), you will be asked for a password: enter "password"
    - The mail server installation will popup some additional options; always use default option

### AWS client install installation

- Clone multicache repository: **https://extgit.iaik.tugraz.at/coresec_students/2021_bachelor_giner_cachesim.git**
- `cd ~/2021_bachelor_giner_cachesim/code/multicache/testbed && sudo ./installClient.sh`
    - The mail server installation will popup some additional options; always use default option

### Benchmarking and recording traces

##### Benchmarks

- Client-side
- `cd ~/2021_bachelor_giner_cachesim/code/multicache/testbed`
- Try running `./runBencharks` to see the necessary parameters
    - **IP**: local IP-address of the server
    - **timeout**: benchmarking time, format in seconds or minutes. (**2m** = **60s**)
    - **user**: mandatory, only used when testing the file-server. Has to be equivalent to the **server** user. The AWS-default is "ubuntu"
- You have the following options for benchmarking: **app**, **db**, **file**, **mail**, **stream**, and **web**
    - Example: `./runBencharks 127.0.0.1 30s ubuntu app db web` to run the app, db and web benchmarks for 30 seconds for address 127.0.0.1 (localhost).
    - **Important**: Use the local network address instead of the public address; otherwise the mail-benchmark will not work.

##### Tracing

- Server-side event tracing (SSV=sched_switch_verbose)
- `cd ~/2021_bachelor_giner_cachesim/code/multicache/testbed`
- Try running `sudo ./trace` to see the necessary parameters
    - **event**: l1e{2-6} / ssv
    - **buffer_size_kb**: the size of the trace buffer for each CPU-core should be as high as possible. The entire buffer lives in RAM, so choose according to RAM capacity.
    - **tracing_cpumask**: bitmask for which CPU traces to enable/save - ff -> all enabled, 1 -> only CPU 0 enabled.
    - **timeout**: trace time, same format as with benchmarking
    - **file**: absolute path to output-file (buffer will be copied to that location). Recommended: `~/2021_bachelor_giner_cachesim/code/multicache/scripts`
    - Example: `sudo ./trace ssv 50000 8 2m ../scripts/trace.x`

### Using the SSV Parser

- `cd ~/2021_bachelor_giner_cachesim/code/multicache/scripts`
- Try running `python3 parse_ssv.py --help` to see available options. The most important options include:
    - **--cpc**: number of caches per physical core
    - **--pc**: number of physical cores
    - **--lc**: number of logical cores (total, not per physical)
    - **--file**: trace file
    - **--pinfo**: show full list of process trace information
    - Example: `python3 parse_ssv.py --cpc 5 --pc 1 --lc 1 --file trace.x`

### Using the L1E Parser

- `cd ~/2021_bachelor_giner_cachesim/code/multicache/scripts`
- Try running `python3 parse_l1e.py --help` to see available options. The most important options include:
    - **--cores**: number of logical cpu cores
    - **--events**: list of PMC events traced (space seperated)
    - **--file**: trace file
    - **--export**: export results
    - **--target_cores**: list of target CPUs
    - Example: `python3 parse_l1e.py --file trace.x --cores 8 --events miss hit inst --target_core 3 7 --export`
