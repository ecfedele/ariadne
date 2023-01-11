# Ariadne
*Ariadne* is a tool for fast computation of preliminary design parameters for liquid-bipropellant rocket engines. Written in C# and using the Windows Presentation Framework (WPF) UI toolchain, Ariadne is designed to speed up the highly-iterative process of rocket engine design by providing a simplistic wizard-like interface to the design process. 

Under the hood, Ariadne employs a novel deep learning-based model to perform real-time, high-quality combustion thermodynamics predictions. Modeled and trained using data garnered from the venerable [NASA Chemical Equilibrium with Applications (CEA)](https://ntrs.nasa.gov/api/citations/19950013764/downloads/19950013764.pdf) code, the goal of the DNN model is to provide a robust estimation of relevant combustion parameters without spending a lifetime reinventing the wheel of mathematical combustion chemistry. This model is planned to be trained using [PyTorch](https://pytorch.org/), with the finalized models exported for C# use as [ONNX](https://github.com/onnx/onnx) exchange files.

While Ariadne is still in its infant stages, it is intended that it will provide a comprehensive treatment of the core elements of the preliminary rocket engine design process:

1. **Initial design planning**, such as thrust and mass flow rate determination, basic statistical estimates of physical parameters, operating point selection and more
2. **Thrust chamber geometry**, using a standard Rao convergent-divergent nozzle topology and information garnered from basic heat flux studies
3. **Basic heat transfer analysis**, particularly for expander-cycle engines, where maximizing working fluid heat recovery is paramount
4. **Basic operating cycle balancing**, with options for gas generator (GG), staged combustion (SC), expander and combustion tap-off (CTO) cycles and accounting for permanent, nonrecoverable pressure losses and losses associated with pumping hardware
5. **Overall performance estimation and off-design-point (ODP) characterization**, particularly useful in throttling or wideband-operation applications
