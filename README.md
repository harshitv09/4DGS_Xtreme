Building the front half of a 4DGS system — the spatio-temporal feature extraction and initialization stage — before feeding it into any Gaussian optimization. 
 
Extract 3D features from video voxel volumes (multi-view) → 
Match them temporally under time-instance constraints → 
Increment matching across camera pairs → 
Triangulate matched features (spatially & temporally) → 
Produce 4D sparse Gaussian initialization. 
