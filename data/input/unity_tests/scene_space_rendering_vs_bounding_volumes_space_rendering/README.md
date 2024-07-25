# Scene space rendering Vs Bounding volumes space rendering

## Scene space rendering
<div align="justify">
<p>Using scene space rendering during ray marching involves rendering the entire scene by processing all objects, lights, and effects within the scene.</p>
</div>

![image](https://github.com/user-attachments/assets/67b2c0b5-914b-40a2-92f5-021f0516c1b5)  
<p align="center"><i>Figure 1.</i> Process of ray marching using screen rendering space<br>
  (left: ray marching in rendering space, right: technical view of rendering result)</p>

## Bounding volumes space rendering
<div align="justify">
<p>Using bounding volumes as space rendering during ray marching involves utilizing simplified shapes (bounding volumes) to approximate the spatial extent of complex objects.</p>
</div>

![image](https://github.com/user-attachments/assets/8f174f95-e168-42a8-a823-bbe9f033565e)  
<p align="center"><i>Figure 2.</i> Process of ray marching using bounding volumes rendering space<br>
  (left: ray marching in rendering space, right: technical view of rendering result)</p>