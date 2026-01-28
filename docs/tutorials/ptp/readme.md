# IMX8 PTP Hardware support

## Table of Contents

- [IMX8 PTP Hardware support](#imx8-ptp-hardware-support)
  - [Table of Contents](#table-of-contents)
  - [1. Summary](#1-summary)
    - [References](#references)
    - [Links](#links)
  - [2. Enabling PTP Support](#2-enabling-ptp-support)
    - [2.1. Understand the Hardware Capabilities](#21-understand-the-hardware-capabilities)
    - [2.2. Prepare the Linux Kernel](#22-prepare-the-linux-kernel)
    - [2.3. Configure and Update Device Tree](#23-configure-and-update-device-tree)
    - [2.4. Install LinuxPTP Tools](#24-install-linuxptp-tools)
    - [2.5. Test and Debug Settings](#25-test-and-debug-settings)
    - [2.6. Explore Advanced Clock Features](#26-explore-advanced-clock-features)
    - [References for Implementation Support](#references-for-implementation-support)
  - [3. PTP Synchronization Tutorial](#3-ptp-synchronization-tutorial)
    - [3.1. Setup the Network](#31-setup-the-network)
    - [3.2. Install Necessary Software](#32-install-necessary-software)
    - [3.3. Verify Hardware Support](#33-verify-hardware-support)
    - [3.4. Configure PTP on the Master Device](#34-configure-ptp-on-the-master-device)
    - [3.5. Configure PTP on the Slave Device](#35-configure-ptp-on-the-slave-device)
    - [3.6. Synchronize the System Clock](#36-synchronize-the-system-clock)
    - [3.7. Verify Synchronization](#37-verify-synchronization)
    - [3.8. Debugging and Optimization](#38-debugging-and-optimization)
      - [Check Clock Quality:](#check-clock-quality)
      - [Configuration Fine-Tuning:](#configuration-fine-tuning)
    - [3.9. Optional: Set Static IPs](#39-optional-set-static-ips)
    - [3.10. Summary Configuration](#310-summary-configuration)
  - [4. Building and Running the PTP Test Application](#4-building-and-running-the-ptp-test-application)
    - [4.1. Setting up the Yocto SDK](#41-setting-up-the-yocto-sdk)
    - [4.2. Prerequisites](#42-prerequisites)
    - [4.3. Compilation](#43-compilation)
    - [4.4. Deploying to Target](#44-deploying-to-target)
    - [4.5. Usage](#45-usage)

## 1. Summary

The NXP i.MX8 family—specifically the **i.MX 8M Plus** processor used in the Advantech **RSB-3720**—features dedicated hardware support for time synchronization protocols.

The NXP i.MX8 processor series, which powers the Advantech RSB-3720, has partial support for time synchronization protocols like TSN (Time-Sensitive Networking) and IEEE 1588 Precision Time Protocol. However, the support depends on the specific i.MX8 model and its integrated Ethernet controller.

- **TSN and IEEE 1588 Support in i.MX8**: Select members of the i.MX8 family, specifically the i.MX 8M Plus, integrate dual Gigabit Ethernet interfaces that feature TSN and IEEE 1588 support. This makes them suitable for demanding real-time applications in industrial and IoT scenarios, supporting time-critical networking and synchronized operations across devices[[1]](https://www.nxp.com/products/i.MX8MPLUS).

- **Advantech RSB-3720 and TSN/IEEE 1588**: The Advantech RSB-3720 is built on the NXP i.MX8M Plus, which the official NXP datasheet confirms includes dual Ethernet with both TSN and IEEE 1588 hardware timestamping capability[[1]](https://www.nxp.com/products/i.MX8MPLUS).

- **Documentation and Features**: Per the NXP i.MX 8M Plus datasheet, the processor specifically supports:
  - Time Sensitive Networking (TSN): This includes features like time-aware shaper and frame preemption for deterministic Ethernet communication.
  - IEEE 1588: Built-in hardware support for clock synchronization over Ethernet (PTP).
  
- **Use in Industrial Applications**: These features are highlighted as beneficial for industrial automation, robotics, and smart factory applications, where precise time synchronization across networked devices is required.[[1]](https://www.nxp.com/products/i.MX8MPLUS)[[2]](https://advcloudfiles.advantech.com/cms/68b06aa1-1a32-4a48-a247-ea8b6d4af80f/eDM%20HTML%20Zip%20File/Content/0619_imx8%20edm/index.html)

- **Caveats**: Not all i.MX8 variants have this feature set. For example, older i.MX8M or i.MX8M Mini/Solo/Nano families may have Gigabit Ethernet, but not necessarily with TSN or full IEEE 1588 hardware support; always check the specific processor block diagram and features list in the datasheet to confirm[[3]](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-8-applications-processors:IMX8-SERIES)[[4]](https://www.mouser.com/pdfDocs/NXP_IMX8FAMFS.pdf).

**Conclusion**:  
The Advantech RSB-3720 with NXP i.MX8M Plus does support TSN and IEEE 1588, making it well-suited for precise, synchronized, time-sensitive networking applications. Always refer to the specific board and SoC datasheets for confirmation of exact features and hardware support.

### References

- NXP i.MX 8M Plus Datasheet: TSN and IEEE 1588 support[[1]](https://www.nxp.com/products/i.MX8MPLUS)
- Advantech and general i.MX 8M Plus solution overview[[2]](https://advcloudfiles.advantech.com/cms/68b06aa1-1a32-4a48-a247-ea8b6d4af80f/eDM%20HTML%20Zip%20File/Content/0619_imx8%20edm/index.html)
- Additional confirmation on the presence and benefit of these features for industrial/IoT uses[[3]](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-8-applications-processors:IMX8-SERIES)[[4]](https://www.mouser.com/pdfDocs/NXP_IMX8FAMFS.pdf).

### Links

1. [i.MX 8M Plus | Cortex-A53/M7 | NXP Semiconductors](https://www.nxp.com/products/i.MX8MPLUS)
2. [NXP i.MX 8 Solutions Empower Embedded Applications to the ... - Advantech](https://advcloudfiles.advantech.com/cms/68b06aa1-1a32-4a48-a247-ea8b6d4af80f/eDM%20HTML%20Zip%20File/Content/0619_imx8%20edm/index.html)
3. [i.MX 8 Advanced Multicore Applications Processors | NXP Semiconductors](https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-8-applications-processors:IMX8-SERIES)
4. [i.MX 8 Family Fact Sheet - Mouser Electronics](https://www.mouser.com/pdfDocs/NXP_IMX8FAMFS.pdf)

## 2. Enabling PTP Support

To use embedded PTP (Precision Time Protocol, IEEE 1588) support in NXP i.MX8 processors—in particular, those that provide hardware timestamping support such as the i.MX8M Plus—follow these steps:

### 2.1. Understand the Hardware Capabilities
- **IEEE 1588 Hardware Timestamping**: The i.MX8M Plus includes Ethernet controllers (ENET and ENET_QOS) capable of hardware timestamping for PTP.
- **Clock Resolution**: The ENET timer provides a 32-bit counter for timestamps. Since it has limited range, synchronization software is used to track time overflows and extend time resolution.

### 2.2. Prepare the Linux Kernel
Ensure your Linux kernel has the following configurations enabled:
- `CONFIG_1588=y`
- `CONFIG_PTP_1588_CLOCK=y` (to enable PTP hardware clock support)
- Network support for PTP-enabled Ethernet drivers.

You will also need to include support for the Ethernet controllers (ENET/ENET_QOS) of the i.MX8 in your kernel build.

### 2.3. Configure and Update Device Tree

Enable PTP in your device tree. Ensure your Ethernet nodes (e.g., `&fec1`) specify IEEE 1588 support. For example:

```dt
&enet {
    ieee1588;
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_enet>;
};
```

The above might vary depending on your hardware; refer to the i.MX8 datasheets.

### 2.4. Install LinuxPTP Tools
For user-space management:
- Use `ptp4l` to synchronize the hardware clock with a PTP master clock. Example:
  ```bash
  ptp4l -i eth0 -m
  ```
- Use `phc2sys` to sync the system clock to the PTP hardware clock:
  ```bash
  phc2sys -s /dev/ptp0 -c CLOCK_REALTIME -O 0 -m
  ```

### 2.5. Test and Debug Settings
- Use `ethtool` to confirm timestamping capabilities are enabled for your network interface:
  ```bash
  ethtool -T eth0
  ```
- Modify `/etc/linuxptp/ptp4l.conf` for additional configurations, such as delay mechanisms and clock quality.

### 2.6. Explore Advanced Clock Features
- For nanosecond-level accuracy, configure the hardware to generate a 1PPS (pulse per second) signal. The ENET timer can provide this output.
- Handle 1588 overflow through software to keep timestamps continuous over long operations.

### References for Implementation Support
1. [NXP Community Discussion on i.MX8 Plus PTP Support](https://community.nxp.com/t5/i-MX-Processors/IMX8-PLUS-PTP-support/m-p/1829691)
2. [AN12149: NXP IEEE 1588 Implementation Guide](https://www.nxp.com/docs/en/nxp/application-notes/AN12149.pdf)
3. Additional resources on i.MX-specific implementations: [AN12149 Documentation](https://docs.nxp.com/bundle/AN12149/page/topics/ieee_1588_implementation_for_imx_rt.html)

To synchronize the time between two Advantech RSB-3720 devices using PTP (Precision Time Protocol), you can configure one as the **PTP master** and the other as the **PTP slave**. Below are the key steps:

---

## 3. PTP Synchronization Tutorial

### 3.1. Setup the Network
- Connect the two RSB-3720 devices with a direct Ethernet cable, or use an Ethernet switch that doesn’t interfere with PTP packets. To ensure the best precision:
  - Use Gigabit Ethernet to minimize jitter and latency.
  - Opt for a dedicated isolated network for PTP.

### 3.2. Install Necessary Software
- **Linux PTP (linuxptp)**: Ensure that both devices have the `linuxptp` package installed:
  ```bash
  sudo apt-get install linuxptp
  ```

### 3.3. Verify Hardware Support
On both devices, check if the Ethernet interface supports hardware timestamping:
```bash
ethtool -T eth0
```
You should see `SOF_TIMESTAMPING_TX_HARDWARE` and `SOF_TIMESTAMPING_RX_HARDWARE` in the output, indicating hardware timestamping is supported.

### 3.4. Configure PTP on the Master Device
- The master device sends synchronization messages to the slave device. Run the following command on the master:
  ```bash
  sudo ptp4l -i eth0 -m --slaveOnly=0
  ```
  - `-i eth0`: Define the Ethernet interface.
  - `-m`: Print the log messages to the console.
  - `--slaveOnly=0`: Set this device as a master.

### 3.5. Configure PTP on the Slave Device
- The slave device receives synchronization messages from the master and adjusts its clock to the master's time. Run the following command on the slave:
  ```bash
  sudo ptp4l -i eth0 -m --slaveOnly=1
  ```
  - `--slaveOnly=1`: Set this device as a slave.


### 3.6. Synchronize the System Clock
On the slave device, synchronize the system clock to the PTP hardware clock using `phc2sys`:
```bash
sudo phc2sys -s eth0 -c CLOCK_REALTIME -O 0 -m
```
- `-s eth0`: Use the hardware clock of the specified interface.
- `-c CLOCK_REALTIME`: Synchronize the system clock (CLOCK_REALTIME).
- `-O 0`: Specifies an optional offset.

On the master device, this is optional. You can also run `phc2sys` to ensure its system clock matches its hardware clock if needed.

### 3.7. Verify Synchronization
Use the following on the slave device to verify synchronization:
```bash
ptp4l -i eth0 -m
```
Look for logs indicating that the slave clock is synchronized with the master clock (e.g., offset values close to 0).

### 3.8. Debugging and Optimization

#### Check Clock Quality:
On the slave, use the PTP management client (`pmc`) to inspect clock quality:
```bash
sudo pmc -u -b 0 'GET CURRENT_DATA_SET'
```
Adjust configurations as needed based on the outputs.

#### Configuration Fine-Tuning:
- Edit `/etc/linuxptp/ptp4l.conf` for advanced configurations, such as sync intervals, delay mechanisms, and clock priorities. For example:
  ```ini
  [global]
  tx_timestamp_timeout 1000
  logSyncInterval -2
  logAnnounceInterval 1
  ```

### 3.9. Optional: Set Static IPs
For a more reliable setup, configure both devices with static IP addresses (or without DHCP dependencies):
Example `/etc/network/interfaces` configuration:
```bash
auto eth0
iface eth0 inet static
address 192.168.1.10  # Master
netmask 255.255.255.0
gateway 192.168.1.1
```
On the slave device, adjust the `address` (e.g., `192.168.1.11`).

### 3.10. Summary Configuration
- **Master**:
  - Command: `sudo ptp4l -i eth0 -m --slaveOnly=0`
- **Slave**:
  - Command: `sudo ptp4l -i eth0 -m --slaveOnly=1`
  - Synchronize system clock: `sudo phc2sys -s eth0 -c CLOCK_REALTIME -O 0 -m`

Once configured correctly, the two devices' clocks will synchronize with nanosecond-level precision.

## 4. Building and Running the PTP Test Application

This directory contains a simple C++ test application (`ptp-test`) that demonstrates how to interact with the PTP hardware clock using the Linux PTP API.

### 4.1. Setting up the Yocto SDK
To compile the test application for the target device (i.MX 8M Plus), you need the Yocto SDK. The SDK provides the cross-compilation toolchain and necessary libraries.

1.  **Install the SDK**:
    Locate the SDK installer script (usually a `.sh` file like `poky-glibc-x86_64-Image-aarch64-toolchain-x.y.z.sh`) generated by your Yocto build. Run it to install the SDK:
    ```bash
    ./poky-glibc-x86_64-Image-aarch64-toolchain-x.y.z.sh
    ```
    Follow the prompts to choose an installation directory (e.g., `/opt/fsl-imx-xwayland/6.12-walnascar/`).

2.  **Source the Environment**:
    Before building, source the environment setup script to configure your path and build variables (`CC`, `CXX`, etc.):
    ```bash
    source /opt/fsl-imx-xwayland/6.12-walnascar/environment-setup-aarch64-poky-linux
    ```
    *Note: Adjust the path and script name according to your specific SDK installation.*

### 4.2. Prerequisites

To compile the application, you need:
- **CMake** (version 3.10 or higher)
- **Make** or **Ninja** build system.

*When using the Yocto SDK, the C++ Compiler (GCC/G++) and other tools are provided by the environment script.*

### 4.3. Compilation

1. **Create a Build Directory**:
   ```bash
   mkdir build
   cd build
   ```

2. **Configure with CMake**:
   - For **Cross-Compilation** (using Yocto SDK):
     Ensure you have sourced the SDK environment script (step 4.1), then run:
     ```bash
     cmake ..
     ```
   - For **Native Compilation** (if compiling directly on the device):
     ```bash
     cmake ..
     ```

3. **Build the Application**:
   ```bash
   make
   ```

   This will generate the `ptp-test` executable.

### 4.4. Deploying to Target
Once built, upload the executable to your RSB-3720 device using `scp`:
```bash
scp ptp-test user@<target-ip>:/home/user/
```

### 4.5. Usage

Run the compiled application on the target device. The application accepts the PTP device path as an optional argument. If not provided, it defaults to `/dev/ptp0`.

```bash
# Run with default device (/dev/ptp0)
./ptp-test

# Run with a specific device
./ptp-test /dev/ptp1
```

*Note: You likely need `sudo` privileges to interact with the PTP character devices.*

The application performs three main checks:
1. **Reads current PTP time**: Displays the time from the PHC.
2. **Adjusts PTP time**: Adds a small offset (10s, 500ns) to test write capabilities.
3. **Enables PPS**: Attempts to enable the PPS (Pulse Per Second) feature for simple offset measurement verification.
