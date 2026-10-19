# CV source (the only source of facts for /cv/)

Compiled 2026-10-19 from the owner's CV and LinkedIn profile. **Every claim on the CV page must come from this file
(or from the site's own data for "Selected public work").** Do not add facts, numbers, dates, awards or skills that
are not here. Rewording for clarity and layout is fine. Deliberately excluded: home address, phone number, email
and any covering letter.

## Identity and links

- Name: Brendan Lynskey
- Location: Leeds, England, UK
- LinkedIn: https://www.linkedin.com/in/brendan-lynskey-a891705
- GitHub: https://github.com/BrendanJamesLynskey
- Portfolio: https://brendanjameslynskey.github.io
- Email: not published (contact through LinkedIn)

## Headline

Experienced engineer working in AI systems (LLMs, agents, MCP, Python) with a background in FPGA, DSP, hardware and
power.

## Profile

- Engineer with over 25 years' experience across hardware, FPGA, SoC, DSP and software.
- Much of that time was spent designing and verifying FPGA and SoC systems: packet switching, high-speed serial
  links, cable modem PHY/MAC, CPU debug, broadcast video and cryptography.
- Then came board-level hardware for AI accelerators at Blaize, including power delivery, signal integrity and DDR.
- Has always combined hardware work with software development.
- For the last two years has worked almost entirely in software, mainly Python, building agentic AI systems with
  LangGraph and MCP. Uses AI coding tools (Claude Code, OpenCode) every day.
- Often works where digital hardware meets analogue physics. Particular interests: SI/PI, power delivery for
  demanding accelerator SoCs, high-speed serial links, thermal, mathematics, and cryptography (including FHE).
- Keen to work where a hardware background counts, such as new compute architectures.
- Values clear communication and good working relationships; adaptable; enjoys automation that improves the
  development process.

## Experience

### Staff Engineer, Blaize (formerly Thinci), Leeds — July 2018 to present

Blaize makes energy-efficient SoCs for machine learning and computer vision. Dual role: software/AI engineering
and hardware systems engineering.

- Building an agentic analytics system in Python with LangGraph, MCP, vLLM and Qwen models on DGX Spark, including
  automated evaluation regression-test suites; video analytics; accelerated development using Claude.
- Responsible for the System-on-Module that won the 2022 Edge AI and Vision Product of the Year award and a 2022
  Sacramento Business Journal Innovation Award, plus its commercial and industrial variants.
- Power delivery (multiphase DC-DC, PoE, flyback), SI/PI and thermal for PCIe accelerator cards and modules with
  PCIe Gen3, USB 3.0, MIPI and LPDDR4, from concept through layout (HDI), bring-up, environmental test, conformal
  coating and EMC pre-compliance.
- Simulated and measured power networks, high-speed serial links and DDR interfaces in the time and frequency
  domains (Cadence Sigrity tools, 3D extraction). Reviewed SoC FC-BGA substrates.
- Analysed SoC SystemVerilog as part of system debug; built a Zynq UltraScale+ MPSoC prototype (PetaLinux);
  analysed competitor systems; ML development and benchmarking in Python.
- Tooling: a Python utility that derives PI requirements from raw power-simulation data using STFT analysis;
  PowerShell/SKILL release tools for Cadence; VS Code extensions in TypeScript.
- EDA: Cadence suite (DE, Allegro, PowerSI, SystemSI, PowerDC, OptimizePI), LTspice/LTpowerCAD II, SIMetrix/SIMPLIS.

### Senior Design Engineer, Imagination Technologies / MIPS, Leeds — September 2014 to July 2018

Debug and probes team.

- High-performance CPU debug systems on Xilinx 7 Series: AXI, PCIe bus mastering, DDR3, Aurora, XADC analogue
  capture, embedded Linux (U-Boot, Buildroot).
- FPGA prototyping platforms for IP cores on UltraScale and AWS EC2 F1 (UltraScale+), covering the whole stack
  from RTL to Linux device driver.
- On-chip instrumentation cores, and software transactors that drove RTL simulation and emulation over TCP/IP
  (Verilog/C VPI PCIe transactors).

### Senior Consultant, Red Embedded, Saltaire — May 2011 to September 2014

Consultancy across hardware, FPGA and software.

- FPGA broadcast product using Xilinx video IP (3G-SDI, scaler), AXI and embedded Linux (VHDL, C).
- Two FPGA DSP projects with Sagentia, for geophysics and medical applications (Verilog, VHDL, System Generator).
- High-performance PC-based DSP (video processing) for professional broadcast (Python, C++); automated RF testing
  for powerline comms (Python).

### Principal Engineer, Pace, Saltaire — July 2005 to June 2011

Delivered complete FPGA systems for cable headend and transmodulator products.

- High-performance packet classifiers and switches, with DDR interfaces, an on-chip bus and large FIFO structures.
- DOCSIS QPSK/16-QAM burst receiver and J.83 64/256-QAM modulator PHY and MAC layers; Gigabit Ethernet;
  high-speed inter-FPGA links; embedded MicroBlaze/PowerPC systems; clock-domain crossings.
- Overhauled the group's verification strategy.
- Also a CableCARD (M-Card) interface and a BER instrument for satellite receivers.

### Senior Engineer, Comodo, Bradford — June 2002 to July 2005

Front-end design of a 0.18 µm cryptographic SoC (TPM / security token). Designed and integrated an in-house crypto
processor (RSA, SHA-1, 3DES, AES, PRNG) with an 8051 CPU, USB, smartcard and LPC interfaces.

### Engineer, Pace, Saltaire — October 1998 to June 2002

Built Pace's first hard-disk MPEG-2 prototype (PCB, FPGA) and FPGA blocks (DVB, UDMA-66) for a 3DES-protected PVR,
which won the company's Most Inspiring Invention award in 2000. Also an ADSL–HPNA set-top-box bridge, and an IrDA
handset for speech/speaker recognition.

### Hardware Engineer, Thales, Stockport — July 1994 to August 1997

Designed the Sonar 2076 data transceiver (1 Gbit/s fibre optics, ECL serial datapath, Fibre Channel, SHARC
processors); worked on a DSP co-processor ASIC.

## Education

- MSc Low Power Systems Integration, University of Manchester (part-time, 2003–2008)
- Diploma in Mathematics, The Open University (part-time, 2010–2013)
- MSc Music Technology (DSP), University of York (1997–1998)
- BEng (Hons) Electronic Engineering, University of Manchester (1991–1994)

## Certifications (selected; full list on LinkedIn)

- Xilinx Certified Engineer
- Accelerated Computer Science Fundamentals Specialization
- Digital Signal Processing Specialization (and others in DSP)
- AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents
- MCP Crash Course: Complete Model Context Protocol (and others in AI and MCP)
- Cadence: SiP Layout v17.2 exam; Celsius Thermal Solver v2021 exam (and others)

## Skills

- Software: Python (NumPy, SciPy, Jupyter), C, C++, TypeScript, Bash, PowerShell, Perl, Tcl, Git
- AI: LangGraph, MCP, vLLM, open-weights LLMs, agent evaluation, Claude Code and other coding agents
- Simulation and modelling: MATLAB/Simulink, SPICE (LTspice, SIMetrix/SIMPLIS), Cadence Sigrity SI/PI, SimPy
- RTL and FPGA: VHDL, Verilog, SystemVerilog, Xilinx (Vivado, up to UltraScale+), Altera; Synopsys, Cadence and
  Mentor simulation and synthesis tools
- Systems: AMBA (APB/AHB/AXI), Arm, MIPS, embedded CPU, embedded Linux (U-Boot, Buildroot, device drivers), DDR,
  PCIe, USB, Ethernet, high-speed serial links
- Hardware: schematic design, PCB stackup and layout, Cadence tools, power delivery, thermal
- Application areas: AI/ML, SoC debug, audio/video, datacomms and networking, DSP, cryptography
