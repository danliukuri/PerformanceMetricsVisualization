# Test Scene 1

<div align="justify">
  Experiment scene feature a collection of 30 simple 3D sphere Signed Distance Functions (SDFs).
  The spheres are organized into groups of three, with smooth blending SDF Boolean operations applied within each group,
  utilizing Constructive Solid Geometry (CSG) techniques.
  The spheres are positioned closely together within each group to ensure visible blending effects.
</div>
<br>
<div align="justify">
  In case of bounding volumes we opted to use a Pentakis Dodecahedron,
  due to its efficiency in defining an accurate sphere shape with minimal vertices and triangles. 
</div>
<br>

![Experiment scene](https://github.com/user-attachments/assets/02e3a30f-9e8d-4469-9728-83395ab6e475)
<p align="center"><i>Figure 1.</i> Experiment scene (same rendering output for both approaches)</p>

![Experiment scene heatmap (screen rendering space)](https://github.com/user-attachments/assets/c5e5412a-166e-4416-88d5-3251bbe85069)
<p align="center"><i>Figure 2.</i> Experiment scene heatmap (screen rendering space)</p>

![TestScene1HeatMap_002_1920x1080_2024-03-29](https://github.com/user-attachments/assets/5f754d66-6a50-4bc8-9903-67af9e4d501c)
<p align="center"><i>Figure 3.</i> Experiment scene heatmap (bounding volumes rendering space)</p>