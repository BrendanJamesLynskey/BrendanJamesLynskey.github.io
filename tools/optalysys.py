"""The /optalysys/ page: a landing page for the work built while learning the areas Optalysys works in.

Every description below is a summary of the linked page's own text (its hub page, landing page or README), not
new claims. The linked pages name the hardware only as "a photonic link module (arXiv:2608.21536)".
"""

PG = "https://brendanjameslynskey.github.io"

SECTIONS = [
    {
        "key": "hardware", "n": "1", "title": "The hardware",
        "lede": "How light computes, from the device physics up to a whole module, modelled in enough detail to "
                "ask whether it pays.",
        "items": [
            {
                "key": "plm", "kind": "Interactive site", "size": "17 chapters, simulator in the page",
                "title": "Inside a Photonic Link Module",
                "href": "https://photonic-link-module-explained.vercel.app/",
                "what": "A simulator of a photonic link module (arXiv:2608.21536), explained chapter by chapter: "
                        "the modulators, the optical Fourier transform, homodyne detection, calibration, and how a "
                        "4-point kernel becomes an NTT inside a real FHE bootstrap. A TypeScript port of the "
                        "simulator runs in the page, checked against the Python reference. Part II models a "
                        "future chip with the photonics stacked on its logic.",
                "why": "To understand the hardware properly by modelling it, layer by layer, and to see with "
                       "numbers where it pays and where it falls short.",
                "links": [("Open the site", "https://photonic-link-module-explained.vercel.app/"),
                          ("Method", "https://photonic-link-module-explained.vercel.app/method")],
                "wide": True,
            },
            {
                "key": "siph", "kind": "Deck series", "size": "3 decks",
                "title": "Silicon Photonics Fundamentals",
                "href": f"{PG}/Optical_Hub_Silicon_Photonics/",
                "what": "The device physics under every optical link: how silicon guides, splits and filters "
                        "light; how modulators and germanium photodiodes put data on it and take it off; and where "
                        "the laser, the package and the picojoules per bit come from.",
                "why": "My background is electronics. This is the optics I needed underneath everything else.",
                "links": [("Open the hub", f"{PG}/Optical_Hub_Silicon_Photonics/")],
            },
        ],
    },
    {
        "key": "workloads", "n": "2", "title": "The workloads",
        "lede": "What the optics might be asked to do: encrypted computing, and moving and transforming data "
                "for AI.",
        "items": [
            {
                "key": "fhe", "kind": "Deck series and simulator", "size": "5 decks, tested code",
                "title": "FHE Accelerator Simulators",
                "href": f"{PG}/FHE_Hub_Accelerator_Simulators/",
                "what": "CKKS as a hardware workload, the anatomy of bootstrapping, a SimPy simulator of an FHE "
                        "accelerator (live in the browser), optical NTT engines, and the design space: is a design "
                        "bound by NTT throughput or by key traffic, and does an optical NTT engine win once "
                        "conversion energy and precision are counted?",
                "why": "To learn FHE from the hardware side: where an accelerator spends its time and energy, and "
                       "where optics could help.",
                "links": [("Open the hub", f"{PG}/FHE_Hub_Accelerator_Simulators/"),
                          ("The simulator", "https://github.com/BrendanJamesLynskey/FHE_Accelerator_Sim")],
            },
            {
                "key": "cithub", "kind": "Deck series and results site", "size": "5 decks, an experiment",
                "title": "Compute in Transit",
                "href": f"{PG}/LLM_Hub_Compute_in_Transit/",
                "what": "Which data movements in LLM training and serving a photonic link module could compute on "
                        "as the data crosses the link, how much work each needs per byte, and an experiment on the "
                        "strongest candidate: a fixed frequency band in place of DeMo's top-k for compressing "
                        "gradients. At this scale the answer is no, and the results site shows why.",
                "why": "To find out whether the module could help AI training, by experiment rather than by "
                       "argument.",
                "links": [("Open the hub", f"{PG}/LLM_Hub_Compute_in_Transit/"),
                          ("The results site", "https://compute-in-transit-results.vercel.app/")],
            },
            {
                "key": "foptinf", "kind": "Deck series", "size": "3 decks",
                "title": "Fourier Optics for Inference",
                "href": f"{PG}/LLM_Hub_Fourier_Optics_Inference/",
                "what": "Could a Fourier-optical engine accelerate LLM inference? The physics with its precision "
                        "and energy bill, where transforms appear in inference workloads, and a "
                        "disaggregated-serving simulator with an optical transform device in the prefill pool, "
                        "live in the browser.",
                "why": "To put numbers on where optical transforms could matter for serving AI models.",
                "links": [("Open the hub", f"{PG}/LLM_Hub_Fourier_Optics_Inference/")],
            },
            {
                "key": "fopttrn", "kind": "Deck series", "size": "3 decks",
                "title": "Fourier Optics for Training",
                "href": f"{PG}/LLM_Hub_Fourier_Optics_Training/",
                "what": "The companion question for training: transforms in the backward pass, optical "
                        "backpropagation and in-situ training, and optical engines inside a training cluster.",
                "why": "Training is a different problem: the weights change every step and the gradients need "
                       "their own precision.",
                "links": [("Open the hub", f"{PG}/LLM_Hub_Fourier_Optics_Training/")],
            },
        ],
    },
    {
        "key": "engineering", "n": "3", "title": "The simulation engineering",
        "lede": "The craft around a simulator: the code, tests, pipelines and measurements that make its answers "
                "trustworthy.",
        "items": [
            {
                "key": "simeng", "kind": "Deck series", "size": "14 decks, each with tested code",
                "title": "Simulation Engineering Toolkit",
                "href": f"{PG}/SimEng_Hub_Toolkit/",
                "what": "Rust and PyO3 fast paths, SystemC models, memory systems, cocotb against RTL, testing "
                        "frameworks, Jenkins, specifications, PyTorch and ONNX front ends, performance analysis, "
                        "measurement tools, power-performance-area trade-offs, and an accelerator model in SimPy "
                        "end to end. Every number in the decks comes from a recorded run.",
                "why": "These are the everyday tools of simulation and frameworks work. I built a deck and "
                       "working code for each to practise them.",
                "links": [("Open the hub", f"{PG}/SimEng_Hub_Toolkit/")],
            },
            {
                "key": "introsim", "kind": "Presentation", "size": "one interactive deck",
                "title": "Introduction to Simulation",
                "href": f"{PG}/Introduction_to_Simulation/",
                "what": "Six levels of simulation, from field solvers to cloud systems, the methods they share and "
                        "how to choose a level, with links at every level into working simulators and decks.",
                "why": "To place the module, the FHE accelerator and the rest within simulation as a whole.",
                "links": [("Open the deck", f"{PG}/Introduction_to_Simulation/")],
            },
        ],
    },
]
