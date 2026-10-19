"""The hand-written parts of the home page: the hardware hubs, the showcases, the index hubs and the
quotes on the "How I check the numbers" page.

Every quote below is checked against its source page by tools/check_quotes.py (the quote must appear
in the page's text, whitespace normalised). Every link is checked by tools/check_links.py.
"""

GH = "https://github.com/BrendanJamesLynskey"
PG = "https://brendanjameslynskey.github.io"

# The owner's home ground. Thumbnails are screenshots of each hub's first screen (tools/thumbs.js).
HARDWARE = [
    dict(
        key="si", title="Signal Integrity & High-Speed Digital Design",
        href=f"{PG}/Signal_Integrity/",
        text="Getting a signal from one chip to another intact: transmission lines, return paths, "
             "materials, vias, crosstalk, jitter, power integrity, timing budgets, de-embedding and "
             "channel operating margin. Every number is computed by a model and checked against "
             "published worked examples.",
        fact="si",  # filled in from data/counts.json
        links=[("Code and models", f"{GH}/Matrix_Articles"),
               ("Interview notes", f"{GH}/Interview_SI_PI")],
    ),
    dict(
        key="serdes", title="SerDes, SoC and Matrix Methods",
        href=f"{PG}/SerDes_Equalisation/",
        text="One 28 GBd backplane channel taken end to end, from S-parameters through CTLE, FFE "
             "and DFE to a closed link budget; the S-, Z- and Y-parameter and filter theory "
             "underneath it; and a Modern SoC Design series on packaging, chiplets, NoCs and memory.",
        fact_text="The noise budget lands 1.36 dB short of 10⁻¹², and seven remedies are priced in dB.",
        links=[("Matrix Methods in Network Parameters", f"{PG}/Matrix_Methods_Network_Parameters/"),
               ("Matrix Concepts in Digital Filters", f"{PG}/Matrix_Concepts_Digital_Filters/"),
               ("Modern SoC Design", f"{PG}/SoC/")],
    ),
    dict(
        key="svsim", title="RTL: interview challenges and free SystemVerilog simulators",
        href=f"{PG}/SystemVerilog_Simulators/",
        text="Nineteen RTL interview challenges put through Icarus Verilog, Verilator, the Vivado "
             "simulator and slang, construct by construct, with every error message recorded; plus "
             "synthesisable RTL with its own verification suites.",
        fact_text="All nineteen challenges pass (nine in Verilator, ten in xsim).",
        links=[("RTL / LLM accelerator challenges", f"{GH}/Interview_RTL_LLM_Accelerators"),
               ("FPGA challenges", f"{GH}/Interview_FPGA"),
               ("Transformer decoder in RTL", f"{GH}/LLM_Transformer_Decoder_RTL"),
               ("Matrix multiplier units", f"{GH}/AI_MMUL_Unit"),
               ("RISC-V SoC", f"{GH}/RISCV_SoC")],
    ),
    dict(
        key="fhe", title="FHE Accelerator Simulators",
        href=f"{PG}/FHE_Hub_Accelerator_Simulators/",
        text="Simulating a fully homomorphic encryption accelerator running CKKS bootstrapping: the "
             "workload, the anatomy of bootstrapping, a SimPy accelerator model with a live "
             "in-browser simulator, optical NTT engines and the design space.",
        fact_text="Five decks; the simulator has a bit-exact JavaScript port and replays OpenFHE traces.",
        links=[("FHE_Accelerator_Sim (code)", f"{GH}/FHE_Accelerator_Sim"),
               ("NTT RTL co-simulation", f"{GH}/RTL_CoSim_NTT")],
    ),
    dict(
        key="simeng", title="Simulation Engineering Toolkit",
        href=f"{PG}/SimEng_Hub_Toolkit/",
        text="The engineering around a hardware-architecture simulator: Rust and PyO3, SystemC "
             "TLM-2.0, DRAM/HBM modelling, a cocotb/Verilator verification bridge, Jenkins, "
             "specifications and test plans, PyTorch and ONNX front ends, measurement tools and "
             "power, performance and area.",
        fact_text="Fourteen decks, with five code repositories behind them.",
        links=[("Rust_DES_Kernel", f"{GH}/Rust_DES_Kernel"),
               ("SystemC_Accelerator_Model", f"{GH}/SystemC_Accelerator_Model"),
               ("Torch_Sim_Frontend", f"{GH}/Torch_Sim_Frontend")],
    ),
    dict(
        key="nss", title="DSP, neural sound synthesis and audio plugins",
        href=f"{PG}/Neural_Sound_Synthesis/",
        text="A twelve-part interactive series on how machine learning makes sound, an audio "
             "plugins hub with a JUCE tutorial and seven example plugins, and browser synthesisers, "
             "analysers and guides to the transforms. Every sound is synthesised live in the browser.",
        fact="dsp",
        links=[("Audio Plugins", f"{PG}/Audio_Plugins/"),
               ("DSP & Music index", f"{GH}/DSP_and_Music")],
    ),
    dict(
        key="cithub", title="Compute in Transit",
        href=f"{PG}/LLM_Hub_Compute_in_Transit/",
        text="Can useful work be done on LLM training and inference traffic while it crosses a "
             "link? Five decks on a photonic link module (arXiv:2608.21536), its operations-per-byte "
             "budget, frequency-domain gradient compression and a fixed-band experiment, with a "
             "results site.",
        fact_text="The answer at this scale is negative, and the series says so.",
        links=[("Results site", "https://compute-in-transit-results.vercel.app/")],
    ),
    dict(
        key="hardware", title="Hardware index: RTL, RISC-V, Arm and more",
        href=f"{PG}/Hardware/",
        text="Everything else in hardware: a RISC-V SoC built from separately verified subsystems, "
             "Arm Cortex-M, Cortex-A, Neoverse, AMBA and system IP series, dividers, CORDIC and NN "
             "number formats in SystemVerilog, Galois fields, optical technology and power electronics.",
        fact="hw",
        links=[("RISC-V SoC", f"{GH}/RISCV_SoC"), ("Optical technology", f"{PG}/Optical_Hub_Silicon_Photonics/")],
    ),
]

# Standout pieces outside the four tracks: live, presentable, link checked.
SHOWCASES = [
    dict(key="dse", title="HW Design-Space Agent", href="https://hw-design-space-agent.vercel.app/",
         img="cards/dse.webp",
         text="A LangGraph agent that explores hardware design trade-offs from one spec down a "
              "fidelity ladder to synthesis, with every number from a recorded run.",
         links=[("Agent code", f"{GH}/HW_Design_Space_Agent")]),
    dict(key="transit", title="Compute in Transit: results", href="https://compute-in-transit-results.vercel.app/",
         img="cards/transit.webp",
         text="Can a fixed frequency band replace DeMo's top-k? An experiment, emulated optics and a "
              "training-transit simulation, with an honest negative result.",
         links=[("Code", f"{GH}/compute-in-transit-results")]),
    dict(key="phatty", title="Phatty", href=f"{PG}/Phatty/", img="shots/phatty.webp",
         text="A browser groovebox: a 303-style bass line, 808/909 drums, a poly synth and effects, all "
              "synthesised live with Web Audio.",
         links=[("Code", f"{GH}/Phatty")]),
    dict(key="rc", title="RC Flight Line", href=f"{PG}/RC-Flight-Line/", img="shots/rc.webp",
         text="A radio-control flight simulator in hand-written WebGL with a blade-element flight "
              "model: stall, tip stall and ground effect emerge from the physics.",
         links=[("Code", f"{GH}/RC-Flight-Line")]),
    dict(key="class47", title="Class 47 Cab Simulator", href=f"{PG}/Class-47-Cab-Sim/",
         img="shots/class47.webp",
         text="A first-person diesel locomotive cab simulator in Three.js, built to run on a "
              "Raspberry Pi 5 with a game controller.",
         links=[("Code", f"{GH}/Class-47-Cab-Sim")]),
]

# The deck library: index hubs. Counts come from data/counts.json.
INDEXES = [
    dict(key="LLMs", title="LLMs", href=f"{PG}/LLMs/", repo=f"{GH}/LLMs",
         text="The main index: the interactive sites, then sub-hubs from transformer internals and GPU "
              "hardware to retrieval, agents, evaluations and safety."),
    dict(key="Hardware", title="Hardware", href=f"{PG}/Hardware/", repo=f"{GH}/Hardware",
         text="RTL, RISC-V and Arm, SoC design, arithmetic units, optical technology, signal integrity "
              "and power electronics."),
    dict(key="Signal_Integrity", title="Signal Integrity", href=f"{PG}/Signal_Integrity/",
         repo=f"{GH}/Signal_Integrity",
         text="One repository, five sections, a long-form PDF alongside."),
    dict(key="DSP_and_Music", title="DSP & Music", href=f"{GH}/DSP_and_Music", repo=None,
         text="Synthesisers, analysis and effects, audio plugins, signal-processing guides and neural "
              "audio synthesis."),
    dict(key="Software", title="Software", href=f"{PG}/Software/", repo=f"{GH}/Software",
         text="CI/CD, Jenkins and GitHub Actions, identity and authorisation, cloud, web, algorithms "
              "and tooling."),
    dict(key="Mathematics", title="Mathematics", href=f"{PG}/Mathematics/", repo=f"{GH}/Mathematics",
         text="Cryptography, coding theory, quantitative finance, mathematics for machine learning and "
              "historical mathematicians."),
    dict(key="Miscellaneous", title="Miscellaneous", href=f"{GH}/Miscellaneous", repo=None,
         text="Interview preparation, careers, psychology and philosophy, and music."),
]

DECODER_RESULTS = "https://github.com/BrendanJamesLynskey/transformer-explainer/blob/main/results.md"
DECODER_RESULTS_RAW = "https://raw.githubusercontent.com/BrendanJamesLynskey/transformer-explainer/main/results.md"

# Quotes on the checks page: (id, source page for the reader, page fetched to verify, quote)
QUOTES = {
    "rtl_array": ("https://systolic-arrays-explained.vercel.app/about#checked", None,
                  "compares every accumulator after every clock edge with the model: 613 values, 0 mismatches"),
    "rtl_mac": ("https://systolic-arrays-explained.vercel.app/about#checked", None,
                "compares every pipeline register after every edge: 11,079 values, 0 mismatches"),
    "lg_check": ("https://agent-orchestration-explained.vercel.app/about#langgraph", None,
                 "After each of the 71 operations"),
    "lg_sessions": ("https://agent-orchestration-explained.vercel.app/about#langgraph", None,
                    "every one of 39 sessions is built as a real StateGraph"),
    "lg_equal": ("https://agent-orchestration-explained.vercel.app/about#langgraph", None,
                 "the whole checkpoint history is compared with the engine's"),
    "lg_nondet": ("https://agent-orchestration-explained.vercel.app/about#langgraph", None,
                  "One LangGraph detail turned out not to be deterministic"),
    "mcp": ("https://agent-protocols-explained.vercel.app/about#sdk", None,
            "the engine must produce the same 160 messages, compared as JSON with request IDs renumbered"),
    "mcp_sessions": ("https://agent-protocols-explained.vercel.app/about#sdk", None,
                     "A small server written with the official MCP Python SDK (mcp 2.3.0) and the SDK's own client play 18 sessions over stdio while a tee records every line"),
    "a2a": ("https://agent-protocols-explained.vercel.app/about#sdk", None,
            "the engine's agent must send the same 56 messages once IDs and timestamps are normalised"),
    "pt_decoder": ("https://transformer-decoder-explained.vercel.app/about#checked", None,
                   "checked against PyTorch fixtures, operation by operation, to within 1e-5"),
    "pt_training": (DECODER_RESULTS, DECODER_RESULTS_RAW,
                    "Backward = PyTorch autograd, at initialisation | max err / (1 + max abs grad) 4.4e-17; loss diff 0.0e+00 | 1e-12"),
    "pt_adamw": (DECODER_RESULTS, DECODER_RESULTS_RAW,
                 "`adamw` = torch.optim over 25 steps | max abs err 1.1e-16 | 1e-12"),
    "acc_miss": ("https://ai-accelerators-explained.vercel.app/about#validation", None,
                 "The SRAM designs reached 0.13% to 8.2%. That miss is the model's main limit, and the chapters say so"),
    "acc_mlperf": ("https://ai-accelerators-explained.vercel.app/about#validation", None,
                   "MLPerf's eight H100s reached 19% of the compute ceiling"),
    "acc_band": ("https://ai-accelerators-explained.vercel.app/about#validation", None,
                 "The model is checked against 8 published figures it does not take as inputs"),
    "racks_band": ("https://ai-racks-explained.vercel.app/about#validation", None,
                   "Across 27 checks the model is between 0.9874 and 1.0368 of the published value."),
    "arch_band": ("https://llm-architectures-explained.vercel.app/about#checks", None,
                  "is within 0.5% of the number of parameters in those weights, at the pinned commit"),
    "arch_approx": ("https://llm-architectures-explained.vercel.app/about#checks", None,
                    "Some parts are approximated and say so on their model pages"),
    "kernels_exact": ("https://gpu-kernels-explained.vercel.app/about#checked", None,
                      "the unit tests require the port to reproduce all of them exactly, with no tolerance"),
    "kernels_stale": ("https://gpu-kernels-explained.vercel.app/about#checked", None,
                      "CI fails if the fixtures are out of date."),
    "numerics_ref": ("https://numerics-explained.vercel.app/about#checked", None,
                     "decodes every code of every format up to 16 bits and compares it with numpy (FP16) and ml_dtypes (BF16, FP8, FP6, FP4)"),
    "tradeoffs_350": ("https://inference-tradeoffs-explained.vercel.app/about#checks", None,
                      "For every one of the 350 points, the vendored engine on the recorded workload reproduces the point's TTFT, TPOT and ITL percentiles exactly"),
    "serving_bytes": ("https://llm-inference-explained.vercel.app/about#numbers", None,
                      "copied byte for byte from a pinned commit by a script that records the commit and the file’s SHA-256"),
    "evals_scipy": ("https://agent-evals-explained.vercel.app/about#engine", None,
                    "the TS port reproduces every fixture exactly, with no tolerance"),
    "si_verified": ("https://github.com/BrendanJamesLynskey/Signal_Integrity#verified",
                    "https://raw.githubusercontent.com/BrendanJamesLynskey/Signal_Integrity/main/README.md",
                    "A model that agrees only with itself is not worth much."),
    "si_droop": ("https://github.com/BrendanJamesLynskey/Signal_Integrity#verified",
                 "https://raw.githubusercontent.com/BrendanJamesLynskey/Signal_Integrity/main/README.md",
                 "| droop vs zpeak | 23.241 | 24.876 | -6.57 % |"),
    "sv_19": ("https://github.com/BrendanJamesLynskey/SystemVerilog_Simulators",
              "https://raw.githubusercontent.com/BrendanJamesLynskey/SystemVerilog_Simulators/main/README.md",
              "All nineteen pass (nine in Verilator, ten in xsim)"),
    "sv_broken": ("https://github.com/BrendanJamesLynskey/SystemVerilog_Simulators",
                  "https://raw.githubusercontent.com/BrendanJamesLynskey/SystemVerilog_Simulators/main/README.md",
                  "Nineteen challenges: six did not compile, eleven compiled but failed when first run"),
    "serdes_budget": ("https://github.com/BrendanJamesLynskey/Hardware",
                      "https://raw.githubusercontent.com/BrendanJamesLynskey/Hardware/main/README.md",
                      "a noise budget that lands 1.36 dB short of 10<sup>&minus;12</sup>, and seven remedies priced in dB"),
    "cit_neg": ("https://github.com/BrendanJamesLynskey/LLMs",
                "https://raw.githubusercontent.com/BrendanJamesLynskey/LLMs/main/README.md",
                "a fixed band, which the module could compute, ends more than a nat above DeMo's top-k, so it is no substitute at this scale"),
    "dse_runs": ("https://hw-design-space-agent.vercel.app/about#site", None,
                 "Every number here comes from HW_Design_Space_Agent at commit 80415c6"),
    "dse_25": ("https://hw-design-space-agent.vercel.app/about", None,
               "a staff-level engineer with more than 25 years in hardware, and I write the software too"),
}

# The Digital Twin card on the home page. While "url" is None the card says a new version is coming soon and
# links the earlier one (interim_url); set "url" to the new twin's address and rebuild to switch the card live.
DIGITAL_TWIN = {
    "url": None,
    "label": "Digital Twin",
    "interim_url": "https://huggingface.co/spaces/BrendanLynskey/CareerConversation",
    "text": "A chat agent, trained on my career, that answers questions about it. Built in Ed Donner's "
            "Proficient AI Engineer curriculum.",
}
