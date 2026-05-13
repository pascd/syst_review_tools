# 🧾 Systematic Review Tools

A modular suite of Python scripts for **BibTeX management**, **DOI data retrieval**, and **bibliographic quality assurance**.
This toolkit is designed to process academic references efficiently—merging `.bib` files, validating required fields, auto-filling missing metadata from DOI information, replacing month strings with numbers, and flagging short papers.

---

## 📁 Repository Structure

```
.
├── bibtex_file_analysis.py
├── bibtex_file_parser.py
├── bibtex_from_doi.py
├── bibtex_replace_month.py
├── check_short_papers.py
├── get_data_from_doi.py
└── merge_bibtex_files.py
```

---

## ⚙️ Main Script Overview

### 🧩 `bibtex_file_analysis.py`

The **main entry point** for automated BibTeX analysis.
It orchestrates the following sequence:

1. **Merges** all `.bib` files in a given folder (`merge_bibtex_main`)
2. **Replaces** month names with numerical equivalents (`replace_month_main`)
3. **Parses and validates** BibTeX entries (`bib_parser_main`)
4. **Checks** for short papers below a minimum page threshold (`check_short_papers_main`)

#### **Usage**

```bash
python bibtex_file_analysis.py <input_folder> <required_args>
```

#### **Available argument sets**

- `set_1`: `["author", "title", "abstract", "year", "pages"]`
- `set_2`: `["author", "title", "year", "pages"]`
- `set_3`: `["author", "title", "year"]`

#### **Output**

- Merged `.bib` file
- Parsed `.bib` file with missing data auto-filled
- `short_papers.txt` report

---

### 🧮 `bibtex_file_parser.py`

Parses a `.bib` file and validates the presence of required fields.
If an entry is missing any of them (e.g., `abstract`, `pages`), it fetches missing metadata from **CrossRef** via DOI.

#### **Key Functions**

- `bib_load_file()` – Reads and parses a BibTeX file
- `bib_error_checking()` – Verifies structural integrity
- `bib_arg_checking()` – Validates required fields and fills missing data via `get_data_from_doi_main()`
- `bib_file_dump()` – Exports updated `.bib` file

#### **Usage**

```bash
python bibtex_file_parser.py <input_file> <required_args>
```

---

### 🌐 `get_data_from_doi.py`

Fetches article metadata from the **CrossRef API** using a DOI.
Extracts fields such as `title`, `author`, `year`, `journal`, `pages`, and `abstract`.

#### **Usage**

```bash
python get_data_from_doi.py <doi>
```

#### **Returns**

A Python dictionary with metadata fields (if available).

---

### 🧷 `merge_bibtex_files.py`

Merges multiple `.bib` files from a folder into a single file.
Duplicates are removed based on the full text of each entry.

#### **Usage**

```bash
python merge_bibtex_files.py <folder_path>
```

#### **Output**

A single `.bib` file named after the folder.

---

### 🗓️ `bibtex_replace_month.py`

Replaces string-formatted months (e.g., `jan`, `feb`, `mar`) with numerical values (`01`, `02`, `03`, etc.) for consistency.

#### **Usage**

```bash
python bibtex_replace_month.py <bib_file>
```

---

### 📏 `check_short_papers.py`

Identifies “short papers” by analyzing the page ranges in a BibTeX file.
Papers with fewer than a specified number of pages are logged in a `short_papers.txt` file.

#### **Usage**

```bash
python check_short_papers.py <bib_file> <min_pages>
```

#### **Output**

- `short_papers.txt` containing all titles below threshold length.

---

### 📚 `bibtex_from_doi.py`

Fetches BibTeX entries directly from CrossRef using DOIs in an Excel file.
It can automatically update an Excel sheet with BibTeX data and save all entries to a text file.

#### **Configuration**

Modify constants at the top of the file to match your environment:

```python
# ===== User Input Section =====
INPUT_XLSX = "EXCEL_FILE_PATH"   # ← Place your Excel file path here
SHEET_NAME = "SHEET_NAME"
DOI_COL = "DOI"
BIBTEX_COL = "BibTeX"
# ==============================
```

#### **Usage**

```bash
python bibtex_from_doi.py
```

#### **Output**

- `bibtex_all.txt` with all BibTeX entries
- Updated Excel sheet with new “BibTeX” column

---

## 🧰 Requirements

Install dependencies:

```bash
pip install bibtexparser requests pandas openpyxl
```

---

## 🧠 Example Workflow

```bash
# Step 1: Run the main analysis script
python bibtex_file_analysis.py ./bib_files set_1

# Step 2: Output files created
# - ./bib_files/bib_files.bib                → merged file
# - ./bib_files/bib_files_parsed.bib         → validated and completed file
# - ./bib_files/short_papers.txt             → short papers report
```

---

## 📊 Full Excel Table

This repository also comprises the full table resultant from a systematic review analysis of several works on disassembly.

This table refers to the information extracted from the works chosen for analysis:

| DE1 Title | DE2 Publisher | VENUE | DE3 Authors | DE4 Year | DE5 Domain | DE6 Robots (Qty) | DE7 Robot Model | DE8 DoF | DE9 Workcell | DE10 End-Effector | DE11 Tech Stack | DE12 Vision System | DE13 CAD Model | DE14 Learning Paradigm | DE15 Implementation | DE17 Autonomy | DE17 Mode | DE18 Sequence | DE19 Resilience | DE20 Feedback | DE21 Metrics | DE22 Objectives | DE23 Optimization Alg | DE24 Challenges | DE25 Knowledge Acq | DE26 Final Results |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VR Co-Lab: A Virtual Reality Platform for Human–Robot Disassembly Training and Synthetic Data Generation | MDPI | Machines | Y. Maddipatla et al. | 2025 | Hard disk (E-waste) | 1 | Niryo One | 6 | VR Station, Quest Pro HMD | Standard gripper | ROS Melodic, Unity, PyTorch | Inside-Out Body-Tracking (IOBT) | URDF files | LSTM with Monte Carlo dropout | Lab Prototype / VR Simulation | Semi-automatic/Collaborative | Non-destructive | Casing unscrewing, platter removal, head detachment | Monte Carlo dropout for motion uncertainty | Visual, auditory, haptic | Task completion time (TCT), error rate | Improve skill acquisition, trajectory planning | AdamW optimizer | Hand tracking occlusion, sensor jitter | Synthetic data generation pipeline | TCT: 4.2 min, Error rate: 10.8%, Trajectory alignment: 82% |
| Recognition and Evaluation of Cables for Automated Cutting in Dismantling Process | IEEE | 2025 IEEE International Conference on Mechatronics (ICM) | R. Matsushita et al. | 2025 | Condenser units | 1 | Not in source | 6 | RGB camera, power box | Cutting tool (pliers) | SOLOv2 model, COCO dataset | RGB camera; SOLOv2 instance segmentation | Model-free | Supervised Learning | Lab Prototype | Fully Automated | Destructive | Cable recognition, cutting point detection, cutting | Robust recognition of entangled cables | Visual feedback | Average Precision (AP), Average Recall (AR), NDCIR | Automate cable-cutting; Resource circulation | Dilation processing | Deformable objects, lighting variations | Custom cable image dataset | AP: 16.7%, AR: 29.6%; NDCIR achieved in 20/21 cases |
| The Challenges of Using Robots to Automate the Recycling of Electronic Devices | IEEE | IEEE Robotics & Automation Magazine | A. Ude et al. | 2025 | HCAs and smoke detectors | 2 | Franka Emika Panda | 7 | Modular workcell, cutters, vises, CNC milling | Soft robotics (SoftHand 2, qb SoftClaw) | ROS, YOLOv8, PDDL, CLIP | RGB-D; Vision-Language Models (VLM) | PDDL environment description | Few-shot learning (RAG); Tactile learning | Lab Prototype | Fully Automated | Destructive & Non-destructive | Pick-up, clamping, PCB levering, bond cutting | Success-checking routines; Virtual energy tanks | High-frequency tactile; Force-impedance | Grasping success rate, action accuracy | Safe battery removal; Hardware scalability | Parametric layout optimization | Infeasible VLM actions, non-standard designs | RAG database; Tactile skill data collection | 98% action accuracy; 84% success feedback |
| Human-robot interaction for extraction of robotic disassembly information | Taylor & Francis | International Journal of Computer Integrated Manufacturing | J. P. J. Prioli, J. L. Rickli | 2024 | LED box | 2 | UR5-e, UR10e, Fanuc LR Mate 200iD | 6 | Cobot training station, 3D-printed box | Robotic Hand-e gripper | Visual Components, RobotDK, Cobot Scripting | Not in source | CAD-based linearization | Learning from Demonstration (Hand-guidance) | Lab Prototype | Semi-automatic / Collaborative | Non-destructive | Unscrew screws, pick/place frame | Trajectory extraction despite human variability | TCP coordinate monitoring | Cycle time, trajectory angle deviation | Reprogram trajectories from human actions | Coordinate frame transformations | Core supply unpredictability, human variability | Hand-guidance recording (TCP/speed) | Cycle time 1:41; Low Z-axis deviation (0.07cm) |
| Robotic disassembly of screws for end-of-life product remanufacturing enabled by deep reinforcement learning | Elsevier | Journal of Cleaner Production | Y. Peng et al. | 2024 | Hexagon screws | 1 | UR5 | 6 | 6-D F/T sensor, 3D camera | Electric screwdriver | Not in source | 3D camera; YOLO-v3/v5 | Model-free | Deep Reinforcement Learning (PPO) | Lab Prototype | Fully Automated | Non-destructive | Approach, position, engagement, unscrewing | Force/torque-based fine-tuning | 6-D force/torque feedback | Disassembly time, success accuracy | Efficient screw removal | PPO (Proximal Policy Optimization) | Rusted/broken screws, uneven lighting | Markov Decision Process (MDP) | 100% success rate; Average time 1.9s-2.7s |
| Consumer electronic redesign for automated disassembly using general-purpose robots | Proc. Design Society | Proceedings of the Design Society | M. Akkawi et al. | 2025 | Remote control | 1 | Franka Emika Panda | 7 | RealSense D435i, recycling bins | Custom gripper for snap-fits | Computer vision, ML models | RealSense D435i | Redesigned CAD (snap-fits) | Not in source | Lab Prototype | Fully Automated | Non-destructive | Cover removal, enclosure detachment, PCB separation | Iterative refinement of failures | Real-time force/position feedback | Success rate per phase | Maximize efficiency, enable circular economy | Pugh Matrix | Screwing precision, intricate assemblies | 3D scanning of original product | 95% success for battery removal |
| Dynamic Balancing of U-Shaped Robotic Disassembly Lines Using an Effective Deep Reinforcement Learning Approach | IEEE | IEEE Transactions on Industrial Informatics | K. Wang et al. | 2024 | Laptops | Not in source | Not in source | Not in source | U-shaped line, conveyor | Not in source | DQN, CPLEX, CNN, TensorFlow | Data-driven system | Precedence matrix | Deep Reinforcement Learning (DQN) | Simulation | Fully Automated | Non-destructive | Dynamic task planning | Generalization for dynamic replanning | System reward function | Cycle Time (TC), Reward value | Minimize cycle time, improve utilization | DQN with heuristic rules | Uncertainty in disassembly time (corrosion) | Markov Decision Process (MDP) | Cycle time 60s; Replanning in 0.042s |
| Unsupervised Human Activity Recognition Learning for Disassembly Tasks | IEEE | IEEE Transactions on Industrial Informatics | X. Zhang et al. | 2023 | Hard Disk Drive (HDD) | Not in source | Not in source | Not in source | Camera (29.97 fps), workstation | Not in source | TensorFlow, Seq-VAE, GRU | Digital camera; Seq-VAE; HMM | Model-free | Unsupervised Learning | Lab Prototype | Semi-automatic / Collaborative | Non-destructive | Tool grab, loosen/remove screws, remove PCB | Robust to unseen scenarios | Visual data frames | Mean Square Error (MSE), Accuracy | Proactive robot assistance | Expectation-maximization | Operational variability and uncertainty | Representation learning from unlabeled video | Average recognition accuracy 91.52% |
| A Robust Robotic Disassembly Sequence Design Using Orthogonal Arrays and Task Allocation | MDPI | Robotics | M. Alshibli et al. | 2019 | Personal computer | Not in source | Not in source | Not in source | Distributed environment | Not in source | Simulated Annealing (SA) | Image recognition | BOM-based model | Simulated Annealing (SA) | Simulation | Semi-automatic/Collaborative | Destructive & Non-destructive | Cover, power supply, and card removal | Taguchi robustness testing | Dashboard monitoring | Runtime, load balancing, fitness | Optimal task allocation, minimize cost | SA, Taguchi's orthogonal arrays | Combinatorial complexity, BOM uncertainty | Taguchi array analysis | SA outperformed exhaustive search (t: -52.94) |
| Human–Robot Collaborative Disassembly Line Balancing Problem With Stochastic Operation Time | IEEE | IEEE Transactions on Automation Science and Engineering | X. Guo et al. | 2023 | Hammer drill, Copier | Not in source | Not in source | Not in source | Conveyor, manual/robotic stations | Not in source | Java JDK14 | Not in source | AND/OR graph based | Shuffled Frog Leaping (MSFLA) | Simulation | Semi-automatic / Collaborative | Non-destructive | Sequential task assignment | Stochastic simulation for uncertainty | Real-time stochastic simulation | Profit, energy consumption | Maximize profit, minimize energy | MSFLA | Uncertainty of operation duration | Monte Carlo simulation | MSFLA superior in convergence and profit |
| An Improved Q-Learning Algorithm for Optimizing Sustainable Remanufacturing Systems | MDPI | Sustainability | S. Qin et al. | 2024 | Copier, Rotor, Radio | Not in source | Not in source | Not in source | Two-sided disassembly line | Not in source | Python, CPLEX | Not in source | AND/OR graph based | Reinforcement Learning (Q-learning) | Simulation | Semi-automatic / Collaborative | Selective / Non-destructive | Product-specific task sequence | Agent exploration/mistake processing | Reward-based environmental feedback | Total disassembly time, convergence | Minimize total disassembly time | Improved Q-learning | Complexity of 3D problems, memory overflow | Q-table environmental interaction | Solved 46-task case in 0.61s (CPLEX failed) |
| Modeling and Optimization of Multiproduct Human–Robot Collaborative Hybrid Disassembly Line Balancing | IEEE | IEEE Transactions on Computational Social Systems | X. Guo et al. | 2025 | Washing machine, Rotor | Not in source | Not in source | Not in source | Resource-sharing area | Not in source | CPLEX, Java JDK 16 | Not in source | AND/OR Graph based | Discrete Aquila Optimizer (DAO) | Lab Prototype | Semi-automatic/Collaborative | Non-destructive | Selective disassembly | Stochastic simulation for conflicts | Not in source | Profit, resource utilization, time | Maximize profit, minimize redundancy | DAO | Resource crowding, worker fatigue | Spatiotemporal network diagram | DAO achieved results within 6% of CPLEX |
| Mixed-integer programming model and hybrid local search genetic algorithm for HRC disassembly | Taylor & Francis | International Journal of Production Research | T. Wu et al. | 2024 | Tesla battery, PC | Not in source | Not in source | Not in source | Auxiliary lifting equipment | Not in source | MATLAB, GUROBI | Image recognition | Part Precedence Diagram (PPD) | Genetic Algorithm (HLSGA) | Simulation | Collaborative | Non-destructive | Battery removal, unscrewing | Local search for error recovery | Not in source | Workstations, smoothness, cost | Minimize NW, minimize SI, minimize DC | HLSGA | Robot standby energy consumption | Not in source | HLSGA dominated FPA and NSGA-II solutions |
| Improved Brain-Storm Optimizer for Disassembly Line Balancing Problems | MDPI | Mathematics | Z. Zhao et al. | 2023 | Car battery, Radio | Not in source | Not in source | Not in source | Linear disassembly line | Not in source | Java, CPLEX | Not in source | AND/OR graph based | Brain-Storm Optimization (IBO) | Simulation | Fully or Semi-automatic | Non-destructive | Task-specific sequences | Hazard degree quantification | Similarity-based clustering | Total profit | Maximize overall profit | IBO | NP-hard nature, hazardous penalties | K-means-based clustering | IBO reached optimal profit (516) in Case 1 |
| An Improved Moth-Flame Algorithm for Human–Robot Collaborative Parallel Disassembly Line Balancing | MDPI | Mathematics | Q. Zhang et al. | 2024 | Refrigerator, Copier | Not in source | Not in source | Not in source | Parallel conveyors | Not in source | Intel IDEA, CPLEX | Not in source | AND/OR graphs | Moth-Flame Optimization (IMFO) | Simulation | Semi-automatic / Collaborative | Destructive & Non-destructive | Product-specific sequences | Safety-based division of labor | Not in source | Disassembly profit, solving time | Maximize profit, worker safety | IMFO with historical optimal mean | Mixing/mishandling of subassemblies | AND/OR graph modeling | IMFO solved large cases in 5.8s (CPLEX timed out) |
| Robotic disassembly line balancing and sequencing problem considering energy-saving and profit | Elsevier | Journal of Cleaner Production | Y. Zeng et al. | 2022 | Microwave oven | Not in source | Not in source | Not in source | Workstations, conveyor | Multiple tool types (O1-O3) | MATLAB | Not in source | Not in source | Genetic Simulated Annealing (IGSA) | Lab Prototype | Fully Automated | Non-destructive | Handle pin/cord/screw removal | Not in source | Tool replacement time feedback | Cycle time, profit, energy, smoothness | Maximize profit, minimize energy | IGSA | Tool replacement influence, NP-hard complexity | Not in source | Best cycle time 58s; best profit 25.56 |
| Mixed integer programming and multi-objective enhanced differential evolution for responsive HRC | Elsevier | Advanced Engineering Informatics | Z. Zhang et al. | 2024 | EoL printer | Not in source | Not in source | Not in source | Responsive workstations, conveyor | Not in source | MATLAB, GUROBI | Not in source | Disassembly information matrix | Differential Evolution (MEDE) | Simulation | Semi-automatic / Responsive | Non-destructive | Direction-turning operations | Not in source | Human-initiated triggers | Workstations, robots, idle time, energy | Minimize robots/workstations, balance workload | MEDE and MIP | Operator fatigue, product status uncertainty | Not in source | MEDE outperformed NSGA-II and AFSA |
| A Hybrid Evolutionary Algorithm for Stochastic Robot Disassembly Line Balancing Problem | Not in source | 2023 29th International Conference on Mechatronics and Machine Vision in Practice (M2VIP) | T. Wu et al. | Not in source | Printers | 3 | KUKA industrial robots | 6 | Disassembly line with conveyors | Not in source | MATLAB | Not in source | Not in source | Evolutionary Algorithm (HEA) | Simulation | Fully Automated | Non-destructive | Sequential priority assignment | Confidence-level based time calculation | Not in source | Workstations, balance index, energy | Optimize line length, minimize energy | HEA (NSGA-II and DE) | Stochastic times, workload balancing | Spatial interference matrix | HEA outperformed NSGA-II in stochasticity |
| Multiple Product Hybrid Disassembly Line Balancing Problem With Human–Robot Collaboration | IEEE | IEEE Transactions on Automation Science and Engineering | S. Qin et al. | 2024 | Washing Machine, Radio | Not in source | Not in source | Not in source | Linear and U-shaped hybrid line | Not in source | CPLEX | Not in source | AND/OR graph based | Mixed Integer Programming | Simulation | Semi-automatic / Collaborative | Non-destructive | Product-specific hybrid paths | Not in source | Not in source | Profit, cycle time, workstations | Maximize disassembly profit | CPLEX (MIP Solver) | Complexity of U-shaped vs Linear balancing | Not in source | Hybrid line increased profit (1594 in Case 1) |
| Hybrid evolutionary algorithm for stochastic HRC disassembly line balancing (carbon emission) | Elsevier | Environmental Science and Pollution Research | T. Wu et al. | 2024 | Printer | Not in source | Not in source | Not in source | Conveyor, ventilation, lighting | Not in source | MATLAB | Not in source | Not in source | Evolutionary Algorithm (HEA) | Simulation | Semi-automatic/Collaborative | Non-destructive | Unscrewing specific components | Robustness to time randomness | Not in source | Workstations, smoothing, carbon emissions | Carbon emission optimization | HEA (NSGA-II with DE) | Uncertainty of product/operator proficiency | Not in source | HEA outperformed seven other algorithms |
| Multi-objective human-robot collaborative disassembly line balancing: remanufacture demand | Elsevier | Computers &amp; Industrial Engineering | L. Zhu et al. | 2024 | CRT TV, Printer | Not in source | Not in source | Not in source | Not in source | Not in source | MATLAB, LINGO | Not in source | Not in source | Modified TLBO (MTLO) | Simulation | Semi-automatic/Collaborative | Non-destructive | Not in source | Not in source | Not in source | Workstations, idle index, hazard index | Maximize early hazardous part removal | MTLO | NP-hard complexity, operator variability | Not in source | MTLO outperformed LINGO and NSGA-II |
| RGB-X Classification for Electronics Sorting | Not in source | 2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) | FNU Abhimanyu, Tejas Zodage, Umesh Thillaivasan, et al. | 2022 | Smartphones (iPhone) | Not in source | Not in source | Not in source | Conveyor belt, Microsoft Azure Kinect | Not in source | PyTorch, VTK, Blender, 3D Slicer | RGB-D + X-ray; YOLOv3, InceptionNet-v3, iCAM | 3D CT scans to synthetic 2D X-ray | Domain Randomization (DR), Fast/Slow Fusion | Laboratory Prototype (Biorobotics Lab CMU) | Fully Automated | Non-destructive classification | Iterative Class Activation Mapping (iCAM) | Domain randomization for noise/variation | Visual/X-ray multi-modal fusion | Accuracy ( $98.6\%$ ), Inference time ( $62.4$  ms), Precision, Recall | Precise sorting for material recovery | Stochastic Gradient Descent (SGD) | Subtle external differences, lack of annotated X-ray data | Synthetic data generation from CT voxel data | Combined accuracy of  $98.6\%$ , saving 12 phones per hour vs single-mode. |
| Automatic Screw Detection and Tool Recommendation System for Robotic Disassembly | ASME | Journal of Manufacturing Science and Engineering | Xinyao Zhang, Kareem Eltouny, Xiao Liang, Sara Behdad | 2022 | Laptops (Dell, Mac), Hard drives | 1 | UR series | Not in source | Experimental workstation, Canon EOS M200 | Pentalobe, Phillips, Torx screwdrivers | YOLOv4, EfficientNetv2, LabelImg, Adam optimizer | RGB (4000x6000 pixels); YOLOv4, EfficientNetv2-S | Model-free (Vision-based detection) | Transfer Learning, Data Augmentation (Mosaic, Saturation) | Lab Prototype | Semi-automatic (Recommendation system) | Non-destructive disassembly | Detection  $\rightarrow$  Extraction  $\rightarrow$  Classification  $\rightarrow$  Tool Recommendation | Data augmentation for bounding box deviations | Visual feedback for tool selection | Precision ( $0.94$ ), Recall ( $0.95$ ), F1-score ( $99.28\%$ ), mAP | Improve efficiency, reduce human fatigue | Adam, PANet adjustment | Small object detection (average  $< 2 \times 2$  pixels), lighting variation | Manual annotation using LabelImg | Achieved F1-score of  $99.28\%$  for tool selection. |
| Multiobjective Human–Robot Collaborative Disassembly Sequence Planning Considering the Properties of Components | IEEE | IEEE Systems, Man, and Cybernetics Magazine | Shujin Qin, Chong Li, Jiacun Wang, et al. | 2024 | Washing machine, Steering gear, Hammer drill | 1 | Mobile operating robots | Not in source | Human-Robot Collaborative Station | Not in source | CPLEX, IntelliJ IDEA, Win10 | Not in source | AND/OR Graph based | Multi-objective Grey Wolf Optimization Algorithm (MGWOA) | Simulation | Semi-automatic/Collaborative | Non-destructive | Task order based on precedence and component type | Random probability mutation strategy | Not in source | Disassembly profit, completion time, Hypervolume, Epsilon | Maximize profit, minimize completion time | MGWOA, NSGA-III, MOEA/D-CRA, CPLEX | Dangerous/delicate components, large-scale complexity | AND/OR Graph analysis | MGWOA obtained higher profit ( $f1=191$ ) and lower time ( $f2=24$ ) than CPLEX. |
| Parallel Multi-objective Multi-type Robot Disassembly Line Balancing Problems | IEEE | 2023 International Conference on Cyber-Physical Social Intelligence (ICCSI) | Zhiwei Zhang, XiWang Guo, Jiacun Wang, et al. | 2023 | Flashlight, Radio | 3 | Multi-type (Screwdriver/Wrench equipped) | Not in source | Parallel production lines, Conveyors | Screwdriver, Wrench | Not in source | Not in source | AND/OR Graph based | Improved Multi-objective Multi-verse Optimization (IMMO) | Simulation | Fully Automated | Partial disassembly | Task intervals (plugboard method) | Wormhole crossover, Roulette wheel selection | Not in source | Profit, Carbon emissions, Smoothness index, HV-metric | Maximize profit, minimize carbon emissions | IMMO, NSGA-III, MOEA/D CRA, MOCGA | Multi-product scenarios, carbon constraints | Logical AND/OR diagrams | IMMO achieved highest HV ( $0.6012$ ) and lowest EI ( $0.0050$ ) at 80 iterations. |
| Multi-robotic partial disassembly line balancing optimization problem considering robotic efficiency difference | IEEE | 2025 16th International Conference on Reliability, Maintainability and Safety (ICRMS) | Tianyang Fang | 2025 | Computers | Not in source | Not in source | Not in source | Main conveyor, Parts cache conveyor, 3-4 Stations | Not in source | MATLAB 2014a, GUROBI, Win10 | Not in source | Not in source | Improved NSGA-II (INSGA-II) | Simulation | Fully Automated | Partial disassembly (Non-destructive) | Tasks 1-18 (optimized sequence) | Repair method for sequence constraints | Not in source | Cycle time, Energy consumption, Hazard index | Minimize cycle time, energy, and hazard index | INSGA-II, GUROBI | NP-hard problem, Heterogeneity of robotic efficiency | Literature precedence relationships | INSGA-II time  $115.03$  s; achieved Pareto solutions for 18 tasks. |
| EMMA: Earthworm Mimetic Manipulator Architecture for Access-Constrained Environments | IEEE | 2021 20th International Conference on Advanced Robotics (ICAR) | Preeti Kannapan, David Garmire, Robert Gregg | 2021 | E-waste (screws, press-fits, pegs) | 1 | EMMA (Custom Bio-inspired) | Hyper-redundant ( $2$  DOF per segment) | Fixed base, supporting surface | Not in source | Simulink, Simscape Multibody, DS SolidWorks | Not in source | SolidWorks model-based | Not in source | Simulation and Laboratory Prototype | Fully Automated (gait sequence controlled) | Non-destructive | Rectilinear manipulation, Heading propagation | Locking actuators/anchoring | Force/Feedback control | Actuator Force Required, Reachability, Accessibility | Minimize power usage, maximize reach | Grübler criterion, force analysis | Infinite DOFs in soft robots, sizing constraints | Bio-mimicry of earthworm states | EMMA force remains constant with segment quantity, unlike standard manipulators. |
| Towards robotic disassembly: A comparison of coarse-to-fine and multimodal fusion screw detection methods | Elsevier | Journal of Manufacturing Systems | Chuangchuang Zhou, et al. | 2024 | Laptops and HDDs | 1 | Gantry robot | 3 | Conveyor, pneumatic unscrewing tool, ring LED, bar light | Pneumatic screwdriver (DEPRAG) | ROS, Python, C++, PyTorch | Intel RealSense L515, Dalsa 2K, Gocator 2340; YOLOv8, Faster R-CNN | Not in source | Deep Learning (CNN), Multimodal Fusion | Lab Prototype | Fully Automated | Non-destructive | Imaging, screw detection, path generation, unscrewing | Error analysis of failed cases (broken/rusted screws) | Visual feedback (depth/intensity) | Success Rate (SR), Average Unscrewing Time (AUT) | Economic viability, efficiency, accuracy | Traveling Salesman Problem (TSP), PAlign | Small object detection, false positives, deep holes | Datasets from recycling facility | Success rate 84.5% (Coarse-to-Fine), speed 2.27s/screw (Multimodal) |
| An Application Study on Reconfigurable Robotic Workcells and Policy Adaptation for Electronic Waste Recycling | IEEE | 2024 IEEE International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE International Conference on Robotics, Automation and Mechatronics (RAM) | Mihael Simonič, et al. | 2024 | Heat cost allocators and smoke detectors | 2 | Franka Emika Panda | 7 (per arm) | Modular platforms, pneumatic vise, cutter, CNC machine | qb SoftHand, VSG, Vacuum suction, Three-finger gripper | ROS, FlexBE, G-code | RealSense D435; YOLOv8, instance segmentation | CAD/CAM for G-code generation | Programming by Demonstration (PbD), Kinesthetic teaching | Lab Prototype | Semi-automatic/Collaborative | Destructive and Non-destructive | Detection, vise fixation, pin/PCB extraction, cutting | Fault detection via graph changes; manual inspection | Force feedback, visual perception | Reconfiguration time, cycle time, battery removal success | Flexibility, adaptability, safety | Dynamic Movement Primitives (DMPs) | Variability of models, damaged components, fire risk | Kinesthetic teaching, augmented datasets | Battery removal success >95%; reconfiguration < 1 day; cycle time 65-75s |
| Towards Recycling E-Waste Using Vision and Robotic Manipulation | TUWS / UTS | Australasian Conference on Robotics and Automation, ACRA | Philipp Kranz, et al. | 2023 | PC components (GPU, RAM) and Task Board | 1 | UR5e | 6 | Custom PCB, oscilloscope, lighting source | Robotiq Hand-E, 3D-printed hook/plug tools | ROS Noetic, C++, Python | IDS U3-3800CP, RealSense D435i; YOLOv8 | Not in source | Deep Learning, Closed-loop visual servoing | Lab Prototype (TRL 4-5) | Fully Automated | Non-destructive | Localise board, press button, move slider/probe, open door | Spiral search for peg-in-hole, open-loop fallbacks | Force-torque sensing, visual feedback | Localisation accuracy, execution time, success rate | Economic viability, human-matching consistency | Perspective-n-Point (PnP) pose estimation | Deformable objects (cables), out-of-focus imagery | Robothon Grand Challenge trials, pilot user study | Automation time 57.5s; Localisation error 1.4mm; successful competition runs |
| Utilizing Hand-Eye Active Visual Servoing for Automated Bolt Removal | IEEE | 2024 IEEE 18th International Conference on Advanced Motion Control (AMC) | Kensei Tanaka, Shogo Arai | 2023 | E-waste (Monitors) | 1 | UR3 | 6 | Hand-eye system, Myutron Projector | Electric Screwdriver (Nittokhoki DLV45C) | Ubuntu 18.04, Python | Active Visual Servoing (AVS) with projected patterns | Model-free | Data-driven (Image Jacobian) | Lab Prototype | Fully Automated | Non-destructive | Positioning, bit insertion, rotation, removal | Robust to misalignment and texture-less surfaces | Real-time visual feedback (Luminance) | Positioning accuracy, RMSE decrease rate | Universal system without fixtures | Optimal projection pattern derivation | Disassembling products lacking distinct visual features | Hand-Eye dataset (500 samples) | Successfully removed M3 bolts with 0.5mm accuracy |
| Vision-Enhanced System For Human-Robot Disassembly Factory Cells: Introducing A New Screw Dataset | IEEE | 2022 4th International Conference on Robotics and Computer Vision (ICRCV) | Georgios Kalitsios, et al. | 2022 | PC Towers, Microwaves, Displays, Lamps | 1 | Generic Collaborative Robot | Not in source | Intel RealSense, Aruco markers | Grasping tools/Screwdriver | ROS, Docker, ZeroMQ, PCL | Mask R-CNN (ResNet-101 FPN); RealSense RGB-D | Model-free | Supervised Learning (Instance Segmentation) | Lab Prototype / Factory cell | Semi-automatic/Collaborative | Non-destructive | 2D Detection, 3D Deprojection, Manipulation | System-agnostic and dockerized | Visual (3D Point Cloud and RGB) | Mean Average Precision (mAP), Frame rate | Increase industrial productivity and flexibility | SGD with momentum | Small object recognition and component overlap | New large-scale screw dataset (945 images) | Average deprojection deviation < 1.8mm; mAP of 0.849 |
| MCCE-Net: Multi-Modal Fusion Component Condition Evaluation Network in Neurosymbolic-Guided Electronics Remanufacturing | IEEE | 2025 IEEE 21st International Conference on Automation Science and Engineering (CASE) | Yifan Wu, et al. | 2025 | Laptops | 1 | Stäubli RX-160 | Not in source | Mechmind LSR S camera, Aputure diffused lights | Not in source | Python, PyTorch, CUDA | Mechmind LSR S; YOLOv11, MCCE-Net | Model-free | Multi-modal Deep Learning (RGB+Depth) | Lab Prototype (TRL 4-5) | Semi-automatic/Collaborative | Non-destructive | Detection of screw, hole, battery, and cover state | Not in source | Visual (RGB+Depth) | mAP (85.0%), Inference speed | Detection accuracy in complex backgrounds | SGD optimizer | Complex backgrounds with similar textures/colors | Neurosymbolic computing (neural symbols) | 85.0% mAP, outperforming YOLOv11 by 14.8% |
| An Improved Multi-objective Multi-verse Optimization Algorithm for Multifunctional Robotic Parallel Disassembly Line Balancing Problems | IEEE | 2022 IEEE International Conference on Systems, Man, and Cybernetics (SMC) | Shancheng Zhang, et al. | 2022 | Flash-lights and Radios | 3 | Generic multifunctional robots | Not in source | Parallel disassembly lines, conveyors | Screwdriver, wrench, electric drills | IntelliJ IDEA | Not in source | AND/OR Graph representation | Metaheuristic Optimization | Simulation | Fully Automated | Non-destructive | Selective removal of subassemblies | Stochastic simulation for uncertainty | Not in source | Profit, Carbon emissions, Cycle time | Maximize profit and minimize carbon footprint | Improved Multi-objective Multi-verse Optimization (IMMO) | Balancing parallel lines with multifunctional robots | AND/OR graphs of EOL products | IMMO superior to NSGA-II and MOEA/D in IGD metrics |
| DCNN-Based Screw Detection for Automated Disassembly Processes | IEEE | 2019 15th International Conference on Signal-Image Technology & Internet-Based Systems (SITIS) | Erenus Yildiz, Florentin Wörgötter | 2019 | Computer Hard Drives | Not in source | Not in source | Not in source | Camera at 60cm distance, perpendicular setup | Not in source | ROS, Python/Keras | RGB camera, Hough Gradient, DCNN (Xception + InceptionV3) | Model-free | Supervised Learning (DCNN) | Lab Prototype | Fully Automated | Non-destructive | Preprocessing, candidate generation, classification | Robust to different backgrounds and illumination | Visual (RGB) | Average Precision (AP), Accuracy | Generalizable, device-independent detection | SGD/Adam | Variable screw shapes and appearance | User-collected datasets | AP of 80.23 (outperforming YOLOv3); 99.0% accuracy |
| Grey Wolf Algorithm for Human-Robot Collaborative Disassembly Line Balancing Problem Subject to Dangerous Components | IEEE | 2022 IEEE International Conference on Networking, Sensing and Control (ICNSC) | Chong Li, et al. | 2022 | Flashlights, Radios, Washing Machines, Pens | 1 | Generic industrial robot | Not in source | Linear workstation for HRC | Not in source | Not in source | Not in source | AND/OR Graph | Swarm Intelligence (GWO) | Simulation | Semi-automatic/Collaborative | Non-destructive | Robots (dangerous parts), Humans (delicate parts) | Search process simulates grey wolf hunting | Not in source | Disassembly profit, CPU running time | Maximize disassembly profit | Improved Grey Wolf Optimizer (GWO) | Balancing tasks based on component attributes | Relation matrix and conflict matrix | Faster convergence than MBO; maximum profit of 333 |
| A Visual Intelligence Scheme for Hard Drive Disassembly in Automated Recycling Routines | SCITEPRESS | ROBOVIS | Erenus Yildiz, Tobias Brinker, Erwan Renaudo, Jakob J. Hollenstein, Simon Haller-Seeber, Justus Piater, Florentin Wörgötter | 2020 | Computer hard drives (HDDs) | Not in source | Not in source | N/A | Tilting table, Basler acA4600-7gc monocular camera, Nerian Karmin2 stereo camera | N/A | TensorFlow 1.15.2, Python, Google Colaboratory | Basler acA4600-7gc (RGB), Nerian Karmin2 (Stereo/Depth), MobV1-RCNN, Hough Circle Transform, DBSCAN | CAD model-free approach | Supervised Learning (Deep Convolutional Neural Networks) | Lab Prototype | Fully Automated (Perception Pipeline) | Non-destructive disassembly | Part detection, screw detection, gap detection, 3D position estimation | Generalization to damaged hard drives and failed manipulation (occlusion) cases | Visual and point-cloud (depth) feedback | Accuracy (AP/IoU), Mean error in volume (%), Precision (%) | Recover rare earth materials (magnets) and hazardous element safety | DBSCAN, MobV1-RCNN, Hough Circle Finder | Shiny and reflective parts reducing point-cloud quality; non-distributed class data; intra-class variance | Taxonomy definition, supervised dataset collection (500 images, 10700 screw samples) | 75% accuracy in components; 80% AP for screw detection; 24.30% mean error in gap volume; 83.33% gap precision |