
Building the front half of a 4DGS system — the spatio-temporal feature extraction and initialization stage — before feeding it into any Gaussian optimization. 

1. Extract 3D features from video voxel volumes (multi-view) → 
2. Match them temporally under time-instance constraints → 
3. Increment matching across camera pairs → 
4. Triangulate matched features (spatially & temporally) → 
5. Produce 4D sparse Gaussian initialization.
