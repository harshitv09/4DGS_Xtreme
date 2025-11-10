## 🧭 Root Level

### `README.md`

Describes the overall purpose, structure, and usage of the project.  
Acts as the main documentation page for setup instructions, pipeline overview, and example runs.

### `requirements.txt`

Lists all Python packages your project depends on (e.g., `numpy`, `open3d`, `pyyaml`).  
Allows anyone to install everything using:

```bash
pip install -r requirements.txt
```

### `.gitignore`

Specifies which files Git should ignore — e.g., large datasets, cache, compiled files, `.pyc`, or temporary outputs.

---

## ⚙️ Configurations — `configs/`

Configuration files are written in YAML format for **flexibility** and **reproducibility**.  
Each stage of the pipeline can be configured independently without modifying the code.

|File|Purpose|
|---|---|
|**`base.yaml`**|Central configuration file combining all stage parameters; imported by scripts as the default pipeline config.|
|**`feature_extraction.yaml`**|Defines parameters like voxel size, downsampling strategy, and normal estimation settings.|
|**`temporal_matching.yaml`**|Contains matching thresholds, temporal consistency radius, and filtering parameters for frame-to-frame feature matching.|
|**`triangulation.yaml`**|Specifies camera calibration files, reprojection thresholds, and numerical stability settings for 3D reconstruction.|
|**`initialization.yaml`**|Holds initialization parameters for converting sparse 3D points into 4D Gaussian primitives (e.g., σ₀, time-step granularity).|

---

## 📂 Data Organization — `data/`

Contains all input data needed for processing and experiments.

|Folder|Purpose|
|---|---|
|**`cameras/`**|Stores intrinsic and extrinsic parameters of each camera (e.g., JSON, TXT, or YAML files with `K`, `R`, `t`).|
|**`calibration/`**|Contains calibration patterns or results (e.g., checkerboard detections, transformation matrices).|
|**`video_voxels/`**|Holds voxelized 3D representations (PLY or NPZ files) extracted from synchronized multi-view videos for each frame or time instance.|

---

## 💾 Outputs — `outputs/`

This is where all generated data from the pipeline is saved.

|Folder|Purpose|
|---|---|
|**`features/`**|Saves extracted 3D keypoints and local descriptors for each frame (often `.npz` or `.pkl`).|
|**`matches/`**|Contains inter-frame and inter-camera feature correspondences after temporal and spatial filtering.|
|**`triangulated_points/`**|Stores reconstructed 3D coordinates obtained via multi-view triangulation (typically `.ply` or `.xyz`).|
|**`sparse_gaussians/`**|Contains initialized Gaussian parameter sets (means, covariances, timestamps) ready for further optimization or splatting.|

---

## 🧠 Source Code — `src/`

All the actual logic of your 4D Gaussian initialization pipeline lives here.  
Each subfolder corresponds to a **logical module** of your processing workflow.

---

### 📦 `src/dataio/`

Handles all input/output operations related to reading, parsing, and transforming raw data.

|File|Description|
|---|---|
|**`camera_loader.py`**|Loads intrinsic and extrinsic parameters from calibration files; returns projection matrices `P = K [R|
|**`voxel_volume_loader.py`**|Reads voxelized point clouds or volume representations from disk and converts them into Open3D point cloud objects.|
|**`video_reader.py`**|Manages multi-view video frame reading and synchronization (e.g., extracting frame sets for specific timestamps).|
|**`transforms.py`**|Implements geometric transformations such as coordinate frame conversions, scaling, and normalization.|

---

### 🧩 `src/features/`

Implements all steps for extracting, describing, and matching 3D features.

|File|Description|
|---|---|
|**`extractor.py`**|Performs 3D keypoint detection and descriptor computation (e.g., ISS, FPFH, SHOT). Uses Open3D for local geometry analysis.|
|**`descriptor.py`**|Handles custom or learned descriptor definitions (optional extension beyond Open3D’s built-ins).|
|**`matcher.py`**|Matches descriptors across frames or cameras using nearest-neighbor search, ratio tests, or geometric filtering.|
|**`temporal_constraints.py`**|Filters matches based on temporal consistency, e.g., motion constraints or displacement limits between consecutive frames.|

---

### 🧮 `src/geometry/`

Responsible for geometric reasoning and 3D point reconstruction.

|File|Description|
|---|---|
|**`triangulation.py`**|Implements linear or iterative triangulation using matched 2D points and camera projection matrices.|
|**`reprojection.py`**|Projects 3D points back to image planes to verify alignment and compute reprojection errors.|
|**`sparse_initializer.py`**|Converts reconstructed 3D (or 4D spatiotemporal) points into Gaussian primitives — initializing means, covariances, and timestamps.|

---

### 🧰 `src/utils/`

Utility functions that support all modules with common, reusable functionality.

|File|Description|
|---|---|
|**`io_utils.py`**|Helper functions for reading/writing `.ply`, `.npz`, `.yaml`, and JSON files.|
|**`math_utils.py`**|Linear algebra and geometry helper routines (vector normalization, rotation conversions, etc.).|
|**`config_parser.py`**|Loads and merges YAML configurations for flexible pipeline control.|
|**`visualization.py`**|Visualization helpers using Open3D or Matplotlib for displaying point clouds, correspondences, or Gaussian ellipsoids.|
|**`timer.py`**|Simple performance timer or decorator to measure runtime per stage.|

---

### 🧩 `src/scripts/`

Executable scripts that **run the pipeline in stages** or **end-to-end**.  
They combine modules from `features`, `geometry`, and `utils` to form complete workflows.

|Script|Description|
|---|---|
|**`run_feature_extraction.py`**|Runs the 3D feature extraction stage for all time instances; saves descriptors to `outputs/features/`.|
|**`run_temporal_matching.py`**|Performs temporal matching across frames or cameras using extracted descriptors; saves results to `outputs/matches/`.|
|**`run_triangulation.py`**|Loads camera parameters and matches, performs triangulation, and exports 3D sparse points.|
|**`run_initialization.py`**|Converts triangulated points into Gaussian primitives (mean, covariance, time) and stores them in `outputs/sparse_gaussians/`.|
|**`run_pipeline.py`**|Orchestrates the **entire pipeline** sequentially — from feature extraction to Gaussian initialization — using the base config file.|

---

### `__init__.py` Files

Each folder has its own `__init__.py` file, which:

- Marks it as a **Python package**.
    
- Optionally defines which functions/classes are exposed when you import that module (e.g., `from src.features import FeatureExtractor3D`).
    

Most will remain empty or just include simple import shortcuts.

---

## 🧩 Summary Table

|Folder|Function|
|---|---|
|`configs/`|Parameter settings for each pipeline stage|
|`data/`|Raw input data and calibration info|
|`outputs/`|Results generated by each module|
|`src/dataio/`|Input/output and preprocessing|
|`src/features/`|Feature extraction, matching, and temporal consistency|
|`src/geometry/`|Triangulation and sparse Gaussian initialization|
|`src/utils/`|Helper tools and math utilities|
|`src/scripts/`|Executable scripts to run the pipeline stages|
