"""The hand-written parts of the home page: the hardware hubs, the showcases, the index hubs and the
quotes on the "How I check the numbers" page.

Every quote below is checked against its source page by tools/check_quotes.py (the quote must appear
in the page's text, whitespace normalised). Every link is checked by tools/check_links.py.
"""

import json
import os

GH = "https://github.com/BrendanJamesLynskey"
COUNTS = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "counts.json")))
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
]

# The deck library: index hubs. Counts come from data/counts.json.
INDEXES = [
    dict(key="LLMs", title="LLMs", href=f"{PG}/LLMs/", repo=f"{GH}/LLMs",
         text="The main index: the interactive sites, then deck series from transformer internals and GPU "
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
                   "eight H100s reached 33% of it and four GB200s (MLPerf v5.1, FP4) 31%"),
    "acc_band": ("https://ai-accelerators-explained.vercel.app/about#validation", None,
                 "The model is checked against 9 published figures it does not take as inputs"),
    "racks_band": ("https://ai-racks-explained.vercel.app/about#validation", None,
                   "Across these the model is between 0.9874 and 1.0368 of the published value."),
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
# The twin is its own Vercel project (BrendanJamesLynskey/Digital_Twin, private), served at /twin/ through the
# rewrite in vercel.json. The URL is absolute so the card also works on the GitHub Pages mirror.
DIGITAL_TWIN = {
    "url": "https://brendan-lynskey.vercel.app/twin/",
    "label": "Digital Twin",
    "interim_url": "https://huggingface.co/spaces/BrendanLynskey/CareerConversation",
    "text": "An AI twin that answers in my voice from my CV and public work. Ask about my experience, or paste a "
            "job description and it will say where I fit and where I don't. Built in Ed Donner's Proficient AI "
            "Engineer curriculum.",
}

# The library (brief 45): one row per subject index with its series hubs, used by the /library/ page and the
# "Browse the library" table of the GitHub profile README. (label, url, in_profile): the profile row shows the
# hubs marked True and links the index's own "Series in this index" list for the rest; /library/ shows them all.
LIBRARY = [
    # total: the LLMs index's series (data/counts.json, from its Sub-hub index; a series is one hub page that lists
    # its decks); this row shows 16 of them
    dict(key="LLMs", title="LLMs", href=f"{PG}/LLMs/", series_href=f"{PG}/LLMs/#series-in-this-index",
         total=COUNTS["LLMs"]["series"],
         text="The interactive sites, then the deck series from transformer internals and GPUs to agents, "
              "evaluations and safety.",
         series=[
             ("Transformer Architecture", f"{GH}/LLM_Hub_Transformer_Architecture", True),
             ("Transformer Training", f"{PG}/LLM_Hub_Transformer_Training/", True),
             ("Karpathy: Zero to Hero", f"{GH}/LLM_Hub_Karpathy_Zero_to_Hero", False),
             ("Modern Architectures", f"{GH}/LLM_Hub_Modern_Architectures", True),
             ("NVIDIA GPUs", f"{GH}/LLM_Hub_NVIDIA_GPUs", True),
             ("Google TPUs", f"{GH}/LLM_Hub_Google_TPUs", True),
             ("AI Accelerators", f"{GH}/LLM_Hub_AI_Accelerators", False),
             ("CUDA", f"{GH}/LLM_Hub_CUDA", False),
             ("Inference Simulators", f"{GH}/LLM_Hub_Inference_Simulators", True),
             ("Local LLM Hosting", f"{GH}/LLM_Hub_Local_LLM_Hosting", False),
             ("RAG & Retrieval", f"{GH}/LLM_Hub_RAG_Retrieval", False),
             ("Agents & Orchestration", f"{GH}/LLM_Hub_Agents", True),
             ("Model Context Protocol", f"{GH}/LLM_Hub_MCP", True),
             ("Coding Agents", f"{GH}/LLM_Hub_Coding_Agents", False),
             ("LLM Evaluations", f"{GH}/LLM_Hub_Evaluations", False),
             ("Key Publications", f"{GH}/LLM_Hub_Key_Publications", False),
         ], more=True),
    dict(key="Hardware", title="Hardware", href=f"{PG}/Hardware/", series_href=f"{GH}/Hardware#series-in-this-index",
         text="Signal integrity, optical technology, accelerator simulators, Arm and RISC-V, SoC design and RTL.",
         series=[
             ("Signal Integrity", f"{PG}/Signal_Integrity/", True),
             ("Silicon Photonics", f"{PG}/Optical_Hub_Silicon_Photonics/", True),
             ("Optics for Data Centres", f"{PG}/Optical_Hub_Data_Centres/", True),
             ("Optics for AI Processing", f"{PG}/Optical_Hub_AI_Processing/", False),
             ("Fourier Optics for Inference", f"{PG}/LLM_Hub_Fourier_Optics_Inference/", False),
             ("Fourier Optics for Training", f"{PG}/LLM_Hub_Fourier_Optics_Training/", False),
             ("Compute in Transit", f"{PG}/LLM_Hub_Compute_in_Transit/", False),
             ("FHE Accelerator Simulators", f"{PG}/FHE_Hub_Accelerator_Simulators/", True),
             ("Simulation Engineering Toolkit", f"{PG}/SimEng_Hub_Toolkit/", True),
             ("Arm Cortex-M", f"{PG}/Cortex_M/", True),
             ("Arm Cortex-A", f"{PG}/Cortex_A/", False),
             ("Arm Neoverse", f"{PG}/Neoverse/", False),
             ("Arm AMBA", f"{PG}/AMBA/", True),
             ("Arm System IP", f"{PG}/Arm_System_IP/", False),
             ("Modern SoC Design", f"{GH}/SoC", True),
         ], more=True),
    dict(key="Software", title="Software", href=f"{PG}/Software/", series_href=f"{PG}/Software/#series-in-this-index",
         text="Identity and authorisation, CI/CD and DevOps, web development, algorithms, compilers and cloud.",
         series=[
             ("Identity & Authorisation", f"{PG}/SW_Hub_Identity_Authorisation/", True),
             ("CI/CD & DevOps", f"{PG}/SW_Hub_CI_CD_DevOps/", True),
             ("Web Development", f"{PG}/SW_Hub_Web_Development/", True),
             ("Algorithms & Data Structures", f"{PG}/SW_Hub_Algorithms_Data_Structures/", True),
             ("Compilers", f"{PG}/Compilers/", True),
             ("Cloud *aaS", f"{GH}/Cloud_aaS_Hub", True),
             ("Simulation Engineering Toolkit", f"{PG}/SimEng_Hub_Toolkit/", False),
             ("Writing VS Code Extensions", f"{PG}/Writing_VSCode_Extensions/", False),
         ], more=True),
    dict(key="Mathematics", title="Mathematics", href=f"{PG}/Mathematics/",
         series_href=f"{GH}/Mathematics#series-in-this-index",
         text="Cryptography, coding theory, quantitative finance, mathematics for machine learning and the "
              "historical series.",
         series=[
             ("Cryptography", f"{PG}/Cryptography/", True),
             ("Coding Theory", f"{PG}/Coding/", True),
             ("Quantitative Finance", f"{PG}/Wilmott_QF_Hub/", True),
             ("Maths for ML", f"{PG}/MML_Hub/", True),
             ("Historical Mathematicians", f"{PG}/Historical_Mathematicians/", True),
             ("Historical Physicists", f"{PG}/Historical_Physicists/", True),
             ("Basic Training (Shankar)", f"{PG}/Mathematics/#basic-training", False),
         ], more=False),
    dict(key="DSP_and_Music", title="DSP & Music", href=f"{GH}/DSP_and_Music", series_href=None,
         text="Browser synthesisers, analysis and effects, audio plugins, signal-processing guides and neural "
              "audio synthesis.",
         series=[
             ("Neural Sound Synthesis", f"{PG}/Neural_Sound_Synthesis/", True),
             ("Audio Plugins", f"{PG}/Audio_Plugins/", True),
             ("J. O. Smith companions", f"{GH}/DSP_and_Music/blob/main/JOS_Companions.md", True),
         ], more=False),
    dict(key="Miscellaneous", title="Miscellaneous", href=f"{GH}/Miscellaneous", series_href=None,
         text="Interview preparation, psychology and philosophy, early music, and personal projects.",
         series=[
             ("Interview Preparation", f"{PG}/Interview_Prep_Hub/", True),
             ("Psychology & Philosophy", f"{PG}/Psychology_Philosophy/", True),
             ("Early Music", f"{PG}/Early_Music/", True),
         ], more=False),
]
