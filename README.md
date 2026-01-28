# CS:GO Strategic Positioning Analysis

## Project Overview
This project applies **computer vision** and **spatial analysis** techniques to analyze Counter-Strike: Global Offensive (CS:GO) map layouts. Using Python and OpenCV, the analysis computes tactical metrics for every playable position on CS:GO maps, enabling data-driven insights into optimal player positioning, strategic advantages, and map control dynamics.

**Analysis Type:** Computer Vision & Spatial Analytics  
**Game:** Counter-Strike: Global Offensive (CS:GO)  
**Primary Focus:** Tactical positioning optimization

## Research Objective

The primary goal of this project is to:

1. **Identify optimal positioning** for players by analyzing line-of-sight coverage and wall proximity
2. **Quantify tactical advantages** of different map positions using measurable metrics
3. **Generate heatmaps** visualizing strategic value across entire CS:GO maps
4. **Provide actionable insights** for competitive players and teams to improve map control

## Key Metrics Analyzed

### 1. Coverage Score
**Definition:** The amount of map area visible from a given position.

**Methodology:**
- Cast rays in 36 directions (360° coverage) from each pixel
- Trace each ray up to 200 steps until hitting a wall or boundary
- Count unique playable pixels reached
- Higher coverage = more map visibility = better information advantage

**Strategic Value:**
- High coverage positions are ideal for:
  - Holding angles and watching multiple approach paths
  - Gathering information on enemy movements
  - Providing team support with wide field of view
- Low coverage positions may be:
  - Safe from being spotted
  - Useful for surprise attacks or defensive holds

### 2. Distance from Wall
**Definition:** Euclidean distance from each playable pixel to the nearest wall or obstacle.

**Methodology:**
- Apply OpenCV's `distanceTransform` with L2 (Euclidean) distance metric
- Compute shortest distance to nearest non-playable (wall) pixel
- Results in continuous distance map across entire playable area

**Strategic Value:**
- Greater wall distance indicates:
  - Open, exposed positions vulnerable to crossfires
  - Center-map control points
  - Risky but high-value positioning
- Smaller wall distance indicates:
  - Cover availability for protection
  - Corner positions for defensive holds
  - Safe angles with limited exposure

## Technical Implementation

### Data Processing Pipeline

#### Step 1: Image Loading and Preprocessing
```python
# Load CS:GO map image
image = cv2.imread("Map2.png")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

#### Step 2: Playable Area Detection
- **Color Thresholding:** Identify playable vs non-playable pixels
- **White pixels** (RGB: 245-255) = walls/obstacles
- **Non-white pixels** = playable area
- Create binary mask: 1 for playable, 0 for walls

#### Step 3: Distance Transform
```python
dist_transform = cv2.distanceTransform(playable_mask, cv2.DIST_L2, 3)
```
Computes distance from each playable pixel to nearest wall using L2 norm.

#### Step 4: Coverage Calculation
**Ray Casting Algorithm:**
```python
def compute_coverage(x, y, mask, num_rays=36, max_steps=200):
    # Cast rays in 36 directions
    # Count unique pixels reached before hitting walls
    # Returns coverage score
```

- **36 rays** at 10° intervals provide comprehensive 360° analysis
- **200 steps** with 1-pixel increments trace sight lines
- **Set-based tracking** prevents double-counting visited pixels

#### Step 5: DataFrame Construction
For every playable pixel (x, y), compute:
- **X Value:** Horizontal coordinate
- **Y Value:** Vertical coordinate  
- **Coverage:** Number of pixels visible from this position
- **Distance from Wall:** Euclidean distance to nearest obstacle

Result: Comprehensive tactical database with thousands of analyzed positions.

### Visualization

#### Coverage Heatmap
- **Colormap:** Jet (blue = low, red = high)
- **Interpretation:** Red zones offer maximum visibility for information gathering
- **Use Case:** Identify power positions for holding sites or gathering intel

#### Distance-from-Wall Heatmap
- **Colormap:** Jet (blue = near walls, red = open areas)
- **Interpretation:** Blue zones provide cover, red zones are exposed
- **Use Case:** Balance risk vs reward when choosing engagement positions

## Project Structure
```
CSGO_Project/
├── code/
│   ├── CS_Step2.ipynb           # Main analysis notebook
│   ├── Correct Playing Field.py  # Map preprocessing utilities
│   ├── test.py                   # Unit tests
│   └── vis.py                    # Visualization functions
├── data/
│   └── Map2.png                  # CS:GO map image(s)
├── output/
│   ├── coverage_heatmap.png      # Coverage visualization
│   └── distance_heatmap.png      # Wall distance visualization
└── README.md
```

## Technologies Used

### Python Libraries
- **OpenCV (cv2):** Image processing, distance transforms, color thresholding
- **NumPy:** Numerical computations, array operations, binary masks
- **Pandas:** DataFrame construction, data organization, analysis
- **Matplotlib:** Heatmap generation, data visualization, plotting
- **Math:** Trigonometric functions for ray casting (sin, cos, radians)

### Algorithms
- **Distance Transform:** Efficient computation of distances to nearest obstacles
- **Ray Casting:** Line-of-sight analysis through iterative pixel traversal
- **Color Space Conversion:** BGR to RGB for accurate thresholding
- **Binary Masking:** Playable area segmentation

## Key Findings

### Tactical Insights

1. **Power Positions:**
   - High coverage + moderate wall distance = optimal control points
   - These positions dominate map control in competitive play
   - Often contested in professional matches

2. **Safe Positions:**
   - Low coverage + close wall distance = defensive strongholds
   - Useful for post-plant situations or retakes
   - Minimize exposure while maintaining defensive capability

3. **Risk-Reward Zones:**
   - High coverage + high wall distance = aggressive plays
   - Maximum information but maximum vulnerability
   - Requires strong aim and positioning fundamentals

4. **Corner Plays:**
   - Variable coverage + minimal wall distance = surprise angles
   - Effective for catching rotating opponents off-guard
   - One-and-done positions requiring team coordination

### Data-Driven Strategy

The analysis reveals:
- **Optimal default positions** for early round setups
- **Rotation paths** that maintain favorable distance-to-wall ratios
- **Information gathering spots** with maximum coverage values
- **Off-angle positions** with asymmetric coverage patterns

## Performance Considerations

### Computational Complexity
- **Coverage Calculation:** O(W × H × R × S) where:
  - W = image width
  - H = image height
  - R = number of rays (36)
  - S = max steps per ray (200)
- **Processing Time:** ~Minutes for full map analysis (depends on map size)

### Optimization Strategies
1. **Spatial Sampling:** Analyze every Nth pixel instead of all pixels
2. **Parallel Processing:** Use multiprocessing for independent position analysis
3. **Caching:** Pre-compute distance transforms once per map
4. **Resolution Reduction:** Downscale maps while preserving tactical features

## How to Run the Analysis

### Prerequisites
```bash
pip install opencv-python numpy pandas matplotlib
```

### Execution Steps

1. **Prepare Map Image:**
   ```python
   # Place CS:GO map screenshot in /data/ folder
   # Ensure white pixels represent walls/obstacles
   ```

2. **Run Analysis:**
   ```bash
   jupyter notebook code/CS_Step2.ipynb
   ```
   Or run cells sequentially:
   - Cell 1: Import libraries and load image
   - Cell 2: Compute distance transform
   - Cell 3: Define coverage functions
   - Cell 4: Build DataFrame
   - Cell 5: Generate heatmaps

3. **Output Files:**
   - `df`: Pandas DataFrame with all tactical data
   - `coverage_heatmap.png`: Coverage visualization
   - `distance_heatmap.png`: Wall distance visualization

### Alternative Execution
```python
python code/test.py  # Run unit tests
python code/vis.py   # Generate visualizations only
```

## Applications

### For Competitive Players
- **Pre-round Planning:** Identify strong default positions
- **Mid-round Adjustments:** Find optimal rotation paths
- **Post-plant Setups:** Locate defensible positions with good coverage
- **Practice Routines:** Train positioning fundamentals using data insights

### For Teams and Coaches
- **Strategy Development:** Design set plays around power positions
- **Demo Review:** Compare actual positioning vs optimal positions
- **Opponent Analysis:** Predict enemy setups based on tactical value
- **Map Pool Preparation:** Understand unique characteristics of each map

### For Game Designers
- **Map Balance:** Identify positions that may be too strong or weak
- **Gameplay Flow:** Ensure strategic diversity across map areas
- **Competitive Viability:** Validate tactical complexity and depth

## Limitations and Considerations

### Current Limitations
1. **2D Analysis Only:** Does not account for vertical positioning (elevation differences)
2. **Static Maps:** No dynamic elements (smoke grenades, molotovs, player models)
3. **Line-of-Sight Simplification:** Assumes perfect visibility without occlusion details
4. **Binary Playability:** Treats all non-wall pixels as equally playable
5. **No Player Mechanics:** Ignores movement speed, peeking, and peekers advantage

### Future Considerations
- Enemy positions and crossfire analysis
- Time-based positioning (early vs late round)
- Utility integration (smoke/flash coverage reduction)
- 3D map analysis with elevation data
- Machine learning for position classification

## Future Work

### Potential Extensions

1. **Multi-Map Analysis:**
   - Extend to all competitive CS:GO maps (Dust2, Mirage, Inferno, etc.)
   - Compare tactical characteristics across map pool
   - Identify universal vs map-specific positioning principles

2. **Dynamic Elements:**
   - Incorporate utility usage (smokes reduce coverage)
   - Model moving opponents and adjust coverage dynamically
   - Account for sound-based information gathering

3. **3D Map Modeling:**
   - Parse CS:GO map files for elevation data
   - Analyze vertical angles and height advantages
   - Compute 3D Euclidean distances and line-of-sight

4. **Machine Learning Integration:**
   - Train classifiers to predict position strength
   - Cluster similar tactical positions
   - Predict opponent likely positions based on game state

5. **Real-Time Integration:**
   - Connect to CS:GO game state API
   - Provide live tactical suggestions during matches
   - Overlay heatmaps on in-game radar

6. **Professional Play Analysis:**
   - Extract player positions from professional demo files
   - Compare pro positioning to computed optimal positions
   - Identify meta shifts and emerging strategies

## Sample Results

Based on the analysis of Map2.png:

**Sample Data (First 10 Playable Pixels):**
```
X Value  Y Value  Coverage  Distance from Wall
705      139      909       0.955
706      139      921       0.955
707      139      880       0.955
708      139      889       0.955
709      139      892       0.955
```

**Insights:**
- Positions around (705-714, 139) show high coverage (880-947 pixels visible)
- Very low wall distance (~0.96 pixels) indicates near-wall positioning
- These are likely safe angles with good information potential

## Academic Context

This project demonstrates practical applications of:
- **Computer Vision:** Image segmentation, distance transforms
- **Computational Geometry:** Ray casting, spatial queries
- **Data Science:** Large-scale spatial data analysis and visualization
- **Game Analytics:** Quantitative analysis of gameplay mechanics

## Contact and Contributions

This project is part of an academic portfolio demonstrating:
- Practical Python programming skills
- Computer vision and image processing expertise
- Data analysis and visualization capabilities
- Creative problem-solving in applied domains

---

**Note:** This analysis is for educational and strategic study purposes. It represents one approach to tactical positioning analysis and should be combined with gameplay experience, team coordination, and situational awareness for optimal results in competitive play.
